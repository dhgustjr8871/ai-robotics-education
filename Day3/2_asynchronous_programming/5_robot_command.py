# 3.3 통합 실행 - 로봇 제어와 카메라 데이터 수신을 병렬 처리
import asyncio

# 사용자 입력을 받아 로봇 명령을 전송하는 구조
async def robot_command():
    while True:
        cmd = input("Enter command: ") # 사용자로부터 명령 입력
        print(f"Sending command: {cmd}") # 명령 전송 시뮬레이션
        await asyncio.sleep(1)  # 네트워크 지연 상황 시뮬레이션

# 주기적으로 프레임을 받아오는 구조
async def receive_camera():
    for i in range(5):
        print(f"[CAMERA] Frame {i} received") # 프레임 수신 출력
        await asyncio.sleep(0.5) # 다음 프레임까지 대기

# 두 작업을 병렬로 실행하여 로봇 제어와 데이터 수신을 동시에 처리
async def main():
    await asyncio.gather(
        robot_command(),
        receive_camera(),
    )

if __name__ == "__main__":
    asyncio.run(main())
