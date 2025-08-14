# 1.1 비동기 함수 정의와 호출
import asyncio # asyncio 모듈 import

# 비동기 함수 정의: 1초 후 인사 메시지 출력
async def greet():
    await asyncio.sleep(1)
    print("Hello Robot")

# 현재 파일이 직접 실행될 때만 아래 코드를 실행
if __name__ == "__main__":
    asyncio.run(greet())