import asyncio
import socket
import struct
from math import pi
import pyrealsense2 as rs
import numpy as np
import cv2


async def update_camera():
    pipe = rs.pipeline()
    cfg  = rs.config()

    cfg.enable_stream(rs.stream.color, 640,480, rs.format.bgr8, 30)
    cfg.enable_stream(rs.stream.depth, 640,480, rs.format.z16, 30)

    pipe.start(cfg)

    print("Camera Initialized")
    try:
        while True:
            frame = pipe.wait_for_frames()
            depth_frame = frame.get_depth_frame()
            color_frame = frame.get_color_frame()

            depth_image = np.asanyarray(depth_frame.get_data())
            color_image = np.asanyarray(color_frame.get_data())
            depth_cm = cv2.applyColorMap(cv2.convertScaleAbs(depth_image,
                                            alpha = 0.5), cv2.COLORMAP_JET)

            gray_image = cv2.cvtColor(color_image, cv2.COLOR_BGR2GRAY)

            cv2.imshow('rgb', color_image)
            cv2.imshow('depth', depth_cm)

            if cv2.waitKey(1) == ord('q'):
                break
    except Exception as e:
        print("Camera error:", e)



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
script_path = "scripts/socket_collect_data.script"

async def handle_client(reader, writer):
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
            elif message == "initialize":
                print("Received initialization request")
                p_init = [90.000/180*pi, -90.000/180*pi, 90.000/180*pi, -90.000/180*pi, -90.000/180*pi, 0.000]
                float_string = "({})\n".format(','.join(map(str, p_init)))
                writer.write(float_string.encode())
                await writer.drain()
            elif message == "req_data":
                print("Received data request")
                print('1: move x axis')
                print('2: move y axis')
                print('3: take photo')
                print('4: exit')
                cmd = int(input())
                if cmd == 1:
                    print('movement value: ')
                    val = float(input())
                    float_string = "({},)\n".format(val)
                    writer.write("movex\n".encode())
                    writer.write(float_string.encode())
                    await writer.drain()
                    
                elif cmd == 2:
                    print('movement value: ')
                    val = float(input())
                    float_string = "({},)\n".format(val)
                    writer.write("movey\n".encode())
                    writer.write(float_string.encode())
                    await writer.drain()

                elif cmd == 3:
                    writer.write("camera\n".encode())
                    await writer.drain()
                    print('number of shots: ')
                    val = float(input())
                    float_string = "({})\n".format(val)
                    writer.write(float_string.encode())
                    await writer.drain()
                else:
                    writer.write("exit\n".encode())
                    await writer.drain()

    except asyncio.CancelledError:
        pass
    except ConnectionResetError:
        print(f"Connection with {addr} reset")
    # except Exception as e:
    #     print("Error:", e)
    finally:
        print(f"Connection with {addr} closed")
        pipe.stop()
        writer.close()
        # await writer.wait_closed()


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
    #camera_task = asyncio.create_task(update_camera())

    async with server:
        await server.serve_forever()
        #await camera_task

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

if __name__ == "__main__":
    try:
        asyncio.run(camera_server_main(host='0.0.0.0', port=12346))
        asyncio.run(main(host=server_ip))
    except KeyboardInterrupt:
        print("\nServer is shutting down...")
