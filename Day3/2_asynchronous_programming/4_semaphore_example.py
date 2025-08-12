# 2.2 asyncio.Semaphore – 동시 접근 제한
import asyncio

# 세마포어 생성 (동시에 2개의 작업만 자원에 접근 가능)
sema = asyncio.Semaphore(2)

async def limited_worker(name: str):
    async with sema: # 세마포어 잠금 획득 (허용 개수 초과 시 여기서 대기)
        print(f"{name} is running")
        await asyncio.sleep(2)
        print(f"{name} is done")

async def main():
    # 작업 A, B, C를 동시에 실행
    # 세마포어 제한(2) 때문에 A, B는 먼저 실행되고 C는 대기
    await asyncio.gather(
        limited_worker("A"),
        limited_worker("B"),
        limited_worker("C"),
    )

if __name__ == "__main__":
    asyncio.run(main())
