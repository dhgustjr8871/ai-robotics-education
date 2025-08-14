# 3. 스크립트 파일 전송하기
import socket

PORT_PRIMARY_CLIENT = 30001
PORT_SECONDARY_CLIENT = 30002

robot_ip = "192.168.1.6"
script_path = "scripts/helloworld.script"
# script_path = "scripts/slowmove.script"
# script_path = "scripts/freedrive.script"
# script_path = "scripts/io_control.script"

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
    sendScriptFile(robot_ip, script_path, PORT_PRIMARY_CLIENT)
    # sendScriptFile(robot_ip, script_path, PORT_SECONDARY_CLIENT)



