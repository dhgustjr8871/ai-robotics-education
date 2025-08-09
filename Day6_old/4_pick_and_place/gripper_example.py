import asyncio
import socket

PORT_PRIMARY_CLIENT = 30001
PORT_SECONDARY_CLIENT = 30002

server_ip = "192.168.1.7"
robot_ip = "192.168.1.6"
script_path = "scripts/2fg7_example.script"
twofg_script_path = "scripts/twofg.script"
set_abs_pose_script_path = "scripts/set_abs_pose.script"

async def handle_client(reader, writer):
    addr = writer.get_extra_info('peername')
    print(f"Connected by {addr}")
    
    try:
        # await asyncio.sleep(0.1)
        # sendScriptFile(robot_ip, twofg_script_path, PORT_PRIMARY_CLIENT)

        data = await reader.read(1024)
        message = data.decode('utf-8').rstrip()  # Remove trailing newline
        if message == "req_width":
            print("Received gripper width request")
            gripper_width = 70.0
            float_string = "({})\n".format(gripper_width)
            writer.write(float_string.encode())

        sendScriptFile(robot_ip, set_abs_pose_script_path, PORT_PRIMARY_CLIENT)
        data = await reader.read(1024)
        message = data.decode('utf-8').rstrip()  # Remove trailing newline
        if message == "req_abs_pose":
            print("Received abs pose request")
            p_rel = [1.57, -1.57, 1.57, -1.57, -1.57, 0.0]
            float_string = "({})\n".format(','.join(map(str, p_rel)))
            writer.write(float_string.encode())
            await writer.drain()
        
    except asyncio.CancelledError:
        pass
    finally:
        print(f"Connection with {addr} closed")
        writer.close()

async def main(host='0.0.0.0', port=12345):
    server = await asyncio.start_server(handle_client, host, port)
    addr = server.sockets[0].getsockname()
    print(f"Server listening on {addr}")
    print("Sending script to the robot...")

    await asyncio.sleep(0.1)
    sendScriptFile(robot_ip, twofg_script_path, PORT_PRIMARY_CLIENT)

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

if __name__ == "__main__":
    try:
        asyncio.run(main(host=server_ip))
    except KeyboardInterrupt:
        print("\nServer is shutting down...")