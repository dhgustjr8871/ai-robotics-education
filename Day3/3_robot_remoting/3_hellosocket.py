import asyncio
import socket

PORT_PRIMARY_CLIENT = 30001
PORT_SECONDARY_CLIENT = 30002

server_ip = "192.168.1.8"
robot_ip = "192.168.1.6"
script_path = "scripts/hellosocket.script"

async def handle_client(reader, writer):
    addr = writer.get_extra_info('peername')
    print(f"Connected by {addr}")
    
    try:
        while True:
            data = await reader.read(1024)      # 클라이언트로부터 데이터 수신
            if not data:
                break
            print(f"Received from {addr}: {data.decode()}")
            writer.write(data)                  # 받은 데이터를 그대로 되돌려줌
            await writer.drain()                # 전송 버퍼가 비워질 때까지 대기
    except asyncio.CancelledError:
        pass
    finally:
        print(f"Connection with {addr} closed")
        writer.close()                          # 연결 종료

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

if __name__ == "__main__":
    try:
        asyncio.run(main(host=server_ip))
    except KeyboardInterrupt:
        print("\nServer is shutting down...")