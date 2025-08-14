# 1.2 여러 작업을 동시에 실행하기
import asyncio

# 비동기 작업 정의
async def task1():
    await asyncio.sleep(1)
    print("Task 1 Done")

async def task2():
    await asyncio.sleep(2)
    print("Task 2 Done")

async def main():
    t1 = asyncio.create_task(task1()) # t1 비동기 작업 시작
    t2 = asyncio.create_task(task2()) # t2 비동기 작업 시작
    await t1 # t1이 끝날 때까지 대기 (대기 중에도 t2는 계속 실행됨)
    await t2 # t2가 끝날 때까지 대기

if __name__ == "__main__":
    asyncio.run(main())