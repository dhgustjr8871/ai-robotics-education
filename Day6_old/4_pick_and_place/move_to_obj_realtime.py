import pyrealsense2 as rs
import numpy as np
import cv2
from ultralytics import YOLO
import asyncio
import socket
import struct

# ------------------------ 설정 ------------------------
PORT_PRIMARY_CLIENT = 30001
PORT_SECONDARY_CLIENT = 30002
server_ip = "192.168.1.4"
robot_ip = "192.168.1.2"
script_path = "scripts/realtime.script"
objects = ['circle', 'ring', 'square', 'rectangle', 'hexagon', 'oval']

# ------------------------ 출력 색상 ------------------------
class Color:
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    END = '\033[0m'

def print2(msg, color=Color.YELLOW):
    print(color + str(msg) + Color.END)

# ------------------------ 유틸리티 ------------------------
def getScriptFromPath(script_path):
    with open(script_path, 'r') as file:
        return file.read()

def sendScript(robot_url, script, port=PORT_PRIMARY_CLIENT):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((robot_url, port))
    sock.send((script + "\n").encode())
    sock.close()

def sendScriptFile(robot_url, script_path, port=PORT_PRIMARY_CLIENT):
    sendScript(robot_url, getScriptFromPath(script_path), port)

# ------------------------ 실시간 위치 계산 ------------------------
def get_3d_position(x, y, depth_frame, intrinsics):
    depth = depth_frame.get_distance(x, y)
    if depth == 0:
        return None
    point = rs.rs2_deproject_pixel_to_point(intrinsics, [x, y], depth)
    return point

# ------------------------ 전역 변수 ------------------------
model = YOLO("weights/obb/best.pt")
pipeline = rs.pipeline()
align = rs.align(rs.stream.color)
target_cls_id = None
angle = 0.0
pos_3d = [0, 0, 0]

# ------------------------ 추적 루프 ------------------------
async def main_loop(writer):
    global pos_3d, angle

    while True:
        await asyncio.sleep(0.1)
        try:
            reader, _ = await asyncio.open_connection(server_ip, 12345)
            data = await reader.read(1024)
            message = data.decode('utf-8').strip()

            if message == "req_data":
                frames = pipeline.wait_for_frames()
                aligned_frames = align.process(frames)
                color_frame = aligned_frames.get_color_frame()
                depth_frame = aligned_frames.get_depth_frame()
                color_image = np.asanyarray(color_frame.get_data())

                results = model(source=color_image, verbose=False)
                boxes = results[0].obb

                best = None
                for i in range(len(boxes)):
                    cls_id = int(boxes.cls[i])
                    if cls_id == target_cls_id:
                        if best is None or boxes.conf[i] > best['conf']:
                            best = {'conf': boxes.conf[i], 'xywhr': boxes.xywhr[i], 'xyxy': boxes.xyxy[i]}

                if best:
                    angle = best['xywhr'][4]
                    cx=best['xyxy'][0] + best['xyxy'][2]
                    cy=best['xyxy'][1] + best['xyxy'][3]
                    cx = int(cx/2)
                    cy = int(cy/2)

                    intrinsics = depth_frame.profile.as_video_stream_profile().intrinsics
                    pos_3d = get_3d_position(cx, cy, depth_frame, intrinsics)

                    if pos_3d:
                        print2(f"Moving to {pos_3d} with angle {angle}", Color.CYAN)
                        dist_ratio = 0.5/(pos_3d[0]*pos_3d[0] + pos_3d[1]*pos_3d[1] + pos_3d[2]*pos_3d[2])
                        if dist_ratio > 1:
                            dist_ratio = 1
                        elif dist_ratio > 20:
                            writer.write("exit\n".encode())
                            await writer.drain()
                            exit()
                        p_rel = np.array([pos_3d[0]*dist_ratio, pos_3d[1]*dist_ratio, pos_3d[2]*dist_ratio, 0.0, 0.0, angle])
                        p_cam = np.array([-0.015, -0.060, 0.0, 0.0, 0.0, 0.0])
                        final_pose = p_rel + p_cam
                        float_string = "({})\n".format(','.join(map(str, final_pose)))

                        writer.write("new_move\n".encode())
                        await writer.drain()
                        writer.write(float_string.encode())
                        await writer.drain()

        except Exception as e:
            print("[ERROR]", e)

# ------------------------ 클라이언트 처리 ------------------------
async def handle_client(reader, writer):
    global target_cls_id
    addr = writer.get_extra_info('peername')
    print(f"Connected by {addr}")

    if target_cls_id is None:
        print("객체를 탐지 중입니다...")
        for _ in range(30): pipeline.wait_for_frames()  # warm-up
        frames = pipeline.wait_for_frames()
        aligned_frames = align.process(frames)
        color_image = np.asanyarray(aligned_frames.get_color_frame().get_data())

        results = model(source=color_image, verbose=False)
        boxes = results[0].obb

        box_dict = {}
        for i in range(len(boxes)):
            cls_id = int(boxes.cls[i])
            if cls_id in box_dict:
                if box_dict[cls_id]['conf'] < boxes.conf[i]:
                    box_dict[cls_id] = {'conf': boxes.conf[i], 'xywhr': boxes.xywhr[i], 'xyxy': boxes.xyxy[i]}
            else:
                box_dict[cls_id] = {'conf': boxes.conf[i], 'xywhr': boxes.xywhr[i], 'xyxy': boxes.xyxy[i]}

        print("감지된 클래스 목록:")
        for i in box_dict:
            print(f"- {objects[i]}")

        target_name = input("추적할 객체 이름을 입력하세요: ").strip().lower()
        if target_name not in objects:
            print("지원되지 않는 객체입니다.")
            return

        target_cls_id = objects.index(target_name)

    await main_loop(writer)

# ------------------------ 메인 서버 실행 ------------------------
async def main():
    config = rs.config()
    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
    pipeline.start(config)

    print("서버 실행 중...")
    sendScriptFile(robot_ip, script_path)
    server = await asyncio.start_server(handle_client, server_ip, 12345)

    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n서버 종료 중...")
        pipeline.stop()
