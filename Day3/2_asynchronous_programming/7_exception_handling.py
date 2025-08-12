# 4.2 예외처리 예제
import asyncio

async def risky_operation():
    try:
        # 예외 발생 가능 구간 (ZeroDivisionError 발생)
        result = 1 / 0
    except ZeroDivisionError as e:
        # 예외 발생 시 처리 로직
        print(f"Error occurred: {e}")
    else:
        # 예외가 발생하지 않았을 경우 실행
        print("Operation succeeded")
    finally:
        # 예외 여부와 관계없이 항상 실행 (자원 정리 등)
        print("Cleaning up resources")

if __name__ == "__main__":
    asyncio.run(risky_operation())