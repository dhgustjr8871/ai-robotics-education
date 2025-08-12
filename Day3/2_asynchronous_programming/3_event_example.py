# 2.1 asyncio.Event – 상태 변화에 따른 동작 제어
import asyncio

event = asyncio.Event() # event 객체 생성 (처음에는 'unset' 상태)

async def controller():
    print("Waiting for signal...")
    await event.wait() # event가 set()될 때까지 대기
    print("Received event!") # set() 호출 후 실행됨

async def trigger():
    await asyncio.sleep(2) # 2초 후 이벤트 발생
    event.set() # event 상태를 'set'으로 변경 → controller()가 깨어남

async def main():
    # controller와 trigger를 함께 실행
    await asyncio.gather(controller(), trigger()) 

if __name__ == "__main__":
    asyncio.run(main())