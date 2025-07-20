import socket

HOST = "192.168.1.8"  # 모든 인터페이스에서 접속 수락
PORT = 12345

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)

print("Waiting for UR robot to connect...")
conn, addr = s.accept()
print(f"Connected by {addr}")

try:
    while True:
        cmd = input("Enter command (start_freedrive / stop_freedrive / finish): ")
        conn.sendall((cmd + "\n").encode())
        if cmd == "finish":
            break
finally:
    conn.close()
    s.close()
