# 4.3 큐를 활용한 작업 분산 처리
import asyncio

# 생산자: 일정 시간 간격으로 데이터를 만들어 큐에 추가
async def producer(queue: asyncio.Queue):
    for i in range(5):
        await asyncio.sleep(1)               # 데이터 생성 지연 시뮬레이션
        item = f"item {i}"
        await queue.put(item)                # 큐에 데이터 삽입
        print(f"Produced {item}")
    await queue.put(None)                    # 종료 신호 전달

# 소비자: 큐에서 데이터를 꺼내 처리
async def consumer(queue: asyncio.Queue):
    while True:
        item = await queue.get()             # 큐에서 데이터 꺼내기
        if item is None:                     # 종료 신호 수신
            queue.task_done()
            break
        print(f"Consumed {item}")
        queue.task_done()                    # 해당 데이터 처리 완료 표시

# main: 생산자와 소비자를 비동기적으로 실행
async def main():
    queue = asyncio.Queue()

    producer_task = asyncio.create_task(producer(queue))
    consumer_task = asyncio.create_task(consumer(queue))

    await asyncio.gather(producer_task)          # 생산자 완료 대기
    await queue.join()                           # 큐가 모두 처리될 때까지 대기
    await consumer_task                          # 소비자 완료 대기

if __name__ == "__main__":
    asyncio.run(main())