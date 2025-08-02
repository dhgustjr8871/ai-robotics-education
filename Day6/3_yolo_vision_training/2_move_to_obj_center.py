import pyrealsense2 as rs
import numpy as np
import cv2
from ultralytics import YOLO
import asyncio
import socket
import struct

class Color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

def print2(str, color=Color.YELLOW):
    print(color, str, Color.END)

PORT_PRIMARY_CLIENT = 30001
PORT_SECONDARY_CLIENT = 30002

server_ip = "192.168.1.5"
robot_ip = "192.168.1.4"
script_path = "scripts/socket_set_position.script"

async def handle_client(reader, writer):
    global pos_3d
    addr = writer.get_extra_info('peername')
    print(f"Connected by {addr}")
    
    try:
        while True:
            data = await reader.read(1024)
            if not data:
                break
            message = data.decode('utf-8').rstrip()  # Remove trailing newline

            print(f"Received from {addr}: {message}")

            if message == "current_pos":
                print("Received position data request")
                p_ = await handle_pos_data(reader)
                print2(f"p_: {p_}", Color.GREEN)
                q_ = await handle_pos_data(reader)
                print2(f"q_: {q_}", Color.GREEN)
            elif message == "req_data":
                print("Received data request")
                p_rel = np.array([-pos_3d[0], -pos_3d[1], 0.0, 0.0, 0.0, 0.0])
                p_cam = ([-0.015, -0.06, 0.0, 0.0, 0.0, 0.0])
                arr = p_rel#+p_cam
                print(arr)
                float_string = "({})\n".format(','.join(map(str, arr)))
                writer.write(float_string.encode())
            
    except asyncio.CancelledError:
        pass
    except ConnectionResetError:
        print(f"Connection with {addr} reset")

    finally:
        print(f"Connection with {addr} closed")
        writer.close()


async def handle_pos_data(reader):
    integers_data = []
    # Receive 24 bytes (6 integers = 6 * 4 bytes = 24 bytes) 
    data = await reader.readexactly(24)
    # Unpack the 6 short integers from the received data
    print("position data:", data)
    integers_data = struct.unpack('>iiiiii', data)
    actual_pos_data = [x/10000 for x in integers_data]

    return actual_pos_data

async def main(host='0.0.0.0', port=12345):
    server = await asyncio.start_server(handle_client, host, port)
    addr = server.sockets[0].getsockname()
    print(f"Server listening on {addr}")
    print("Sending script to the robot...")

    await asyncio.sleep(0.1)
    sendScriptFile(robot_ip, script_path, PORT_PRIMARY_CLIENT)

    async with server:
        await server.serve_forever()

def getScriptFromPath(script_path):
    with open(script_path, 'r') as file:
        script = file.read()
    return script

def sendScript(robot_url, script, port=PORT_PRIMARY_CLIENT):
    socketClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socketClient.connect((robot_url, port))
    socketClient.send((script + "\n").encode())
    socketClient.close()

def sendScriptFile(robot_url, script_path, port=PORT_PRIMARY_CLIENT):
    script = getScriptFromPath(script_path)
    sendScript(robot_url, script, port)


# 사용할 객체 이름 목록
objects = ['circle', 'ring', 'square', 'rectangle', 'hexagon', 'oval']

def get_3d_position(x, y, depth_frame, intrinsics):
    depth = depth_frame.get_distance(x, y)
    if depth == 0:
        return None
    point = rs.rs2_deproject_pixel_to_point(intrinsics, [x, y], depth)
    return point  # [X, Y, Z] in meters

if __name__ == "__main__":
    global pos_3d
    # YOLO 모델 로딩
    model = YOLO("runs/detect/train/weights/best.pt")

    # RealSense 파이프라인 설정
    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
    pipeline.start(config)

    align = rs.align(rs.stream.color)  # Depth-Color 정렬용

    try:
        print("촬영 중... (1초 후 프레임 캡처)")
        for _ in range(30):  # warm-up
            frames = pipeline.wait_for_frames()
        aligned_frames = align.process(frames)
        color_frame = aligned_frames.get_color_frame()
        depth_frame = aligned_frames.get_depth_frame()

        # numpy array 변환
        color_image = np.asanyarray(color_frame.get_data())

        # YOLO 탐지
        results = model(source=color_image, verbose=False)
        results[0].show()
        boxes = results[0].boxes
        box_dict = {}

        for box in boxes:
            cls_id = int(box.cls[0])
            print(box)
            if cls_id in box_dict:
                if box_dict[cls_id].conf < box.conf:
                    box_dict[cls_id] = box
            else:
                box_dict[cls_id] = box

        # 사용자 입력
        print("감지된 클래스 목록:")
        for i in box_dict:
            print(f"- {objects[i]}")
        while(True):
            target_name = input("찾고자 하는 객체 이름을 입력하세요: ").strip().lower()

            if target_name not in objects:
               print("지원되지 않는 객체입니다.")
            else:
                break

            cls_id = objects.index(target_name)
            if cls_id not in box_dict:
                print(f"{target_name} 감지되지 않음.")
            else:
                break

        box = box_dict[cls_id]
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        cx = (x1 + x2) // 2
        cy = (y1 + y2) // 2

        # 3D 위치 계산
        intrinsics = depth_frame.profile.as_video_stream_profile().intrinsics
        pos_3d = get_3d_position(cx, cy, depth_frame, intrinsics)

        if pos_3d is None:
            print("해당 위치의 Depth 정보 없음.")
        else:
            print(f"{target_name} 중심의 3D 위치 (X, Y, Z): {np.round(pos_3d, 4)} [m]")
            pos_3d *= 1000



    finally:
        pipeline.stop()
    
    try:
        asyncio.run(main(host=server_ip))
    except KeyboardInterrupt:
        print("\nServer is shutting down...")