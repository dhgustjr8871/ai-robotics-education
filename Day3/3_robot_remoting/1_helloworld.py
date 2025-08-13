# 2.1 파이썬 파일 실행하기
import socket

robot_ip = "192.168.1.6"  # 확인한 로봇의 IP 주소 입력

# 로봇에 보낼 URScript 코드 (팝업 메시지 표시 예제)
script = """
def helloworld():
    popup("Happy learning!")  # 로봇 teach pendant에 팝업 메시지 출력
end
"""

# 소켓 생성 (IPv4, TCP 프로토콜 사용)
socketPrimaryClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 로봇의 Primary Interface(30001번 포트)에 연결
socketPrimaryClient.connect((robot_ip, 30001))  

# URScript 코드 전송 (문자열 끝에 개행 문자 \n 필요)
socketPrimaryClient.send((script + "\n").encode())

# 소켓 연결 종료
socketPrimaryClient.close()