# 1: 로봇 원격 제어를 위한 비동기 프로그래밍 실습

이 문서는 로봇과 컴퓨터 간의 실시간 통신, 특히 카메라 데이터 수신과 로봇 명령 처리를 병렬로 처리해야 하는 상황을 위한 **Python 비동기 프로그래밍 기초와 실습 예제**를 제공합니다. 특히, `Event`, `Semaphore`와 같은 흐름 제어 기법은 명령 전송과 이미지 처리 간 충돌을 방지하고, 시스템 자원의 안전한 사용을 보장하는 데 필수적입니다.

예제를 통해 다음과 같은 핵심 개념을 실습합니다:

- 비동기 함수 정의와 실행 (`async`, `await`)
- 여러 작업 동시 실행 (`create_task`, `gather`)
- 흐름 제어를 위한 `Event`, `Semaphore` 사용법

---

## 1. Python asyncio 기본 구조

### 1.1 비동기 함수 정의와 호출

비동기 함수는 `async def`로 정의하며, 내부에서 `await`을 사용해 비동기적으로 동작할 수 있는 작업을 수행할 수 있습니다. 이는 긴 작업이 다른 작업을 막지 않도록 합니다.

```python
# 비동기 함수 정의: 1초 후 인사 메시지 출력
import asyncio

async def greet():
    await asyncio.sleep(1)
    print("Hello Robot")

asyncio.run(greet())
```

### 1.2 여러 작업을 동시에 실행하기 (`create_task`, `gather`)

`asyncio.create_task()`나 `asyncio.gather()`를 사용하면 여러 개의 비동기 작업을 동시에 실행할 수 있습니다. 이는 병렬 작업이 필요한 로봇 시스템에서 필수적인 개념입니다.

```python
# 두 개의 작업을 동시에 실행하여 비동기 동작 이해하기
async def task1():
    await asyncio.sleep(1)
    print("Task 1 Done")

async def task2():
    await asyncio.sleep(2)
    print("Task 2 Done")

async def main():
    t1 = asyncio.create_task(task1())
    t2 = asyncio.create_task(task2())
    await t1
    await t2

asyncio.run(main())
```

---

## 2. 흐름 제어 도구 실습

### 2.1 asyncio.Event – 상태 변화에 따른 동작 제어

`asyncio.Event`는 이벤트가 발생할 때까지 대기하고, 특정 시점에 한 번만 모든 대기 중인 작업을 깨우는 용도로 사용됩니다. 상태 변화 기반의 동작 흐름을 설계할 때 유용합니다.

```python
# Event를 사용한 상태 변화 동기화 예제
event = asyncio.Event()

async def controller():
    print("Waiting for signal...")
    await event.wait()
    print("Received event!")

async def trigger():
    await asyncio.sleep(2)
    event.set()

async def main():
    await asyncio.gather(controller(), trigger())

asyncio.run(main())
```

### 2.2 asyncio.Semaphore – 동시 접근 제한

`asyncio.Semaphore`는 동시에 접근할 수 있는 비동기 작업의 수를 제한할 수 있는 동기화 도구입니다. 로봇 시스템에서 자원을 동시에 사용하는 작업이 많을 때 충돌을 방지하는 데 활용됩니다.

```python
# 동시에 2개 작업까지만 허용하는 세마포어 예제
sema = asyncio.Semaphore(2)

async def limited_worker(name):
    async with sema:
        print(f"{name} is running")
        await asyncio.sleep(2)
        print(f"{name} is done")

async def main():
    await asyncio.gather(
        limited_worker("A"),
        limited_worker("B"),
        limited_worker("C")
    )

asyncio.run(main())
```

---

## 3. 예제: 로봇 제어와 카메라 데이터 수신을 병렬로 처리하기

이 예제는 실시간 로봇 제어 시나리오를 단순화한 비동기 처리 구조를 보여줍니다. 두 개의 작업을 동시에 실행하는 구조를 통해 병렬 처리 방식의 이해를 돕습니다.

- `robot_command()`는 사용자로부터 명령어를 입력받아 전송하는 흐름을 시뮬레이션합니다.
- `receive_camera()`는 카메라가 프레임을 실시간으로 수신하는 상황을 흉내냅니다.
- 이 두 작업은 `asyncio.gather()`로 동시에 실행되며, 실제 로봇 시스템에서 입력 처리와 센서 수신이 동시에 이루어지는 구조를 반영합니다.

이를 통해 병렬 처리, 흐름 제어, 이벤트 루프 실행 구조 등을 실습합니다.

### 3.1 로봇 명령 처리

```python
# 사용자 입력을 받아 로봇 명령을 보내는 루틴
async def robot_command():
    while True:
        cmd = input("Enter command: ")
        print(f"Sending command: {cmd}")
        await asyncio.sleep(1)  # 네트워크 지연 상황을 시뮬레이션
```

### 3.2 카메라 데이터 수신 시뮬레이션

실시간 카메라 프레임 수신을 흉내 내는 함수로, 실제 이미지 수신과 유사한 주기로 동작하는 구조를 확인할 수 있습니다.

```python
# 카메라에서 프레임을 주기적으로 수신하는 시뮬레이션
async def receive_camera():
    for i in range(5):
        print(f"[CAMERA] Frame {i} received")
        await asyncio.sleep(0.5)
```

### 3.3 통합 실행

앞서 정의한 두 비동기 함수를 동시에 실행하여 병렬 처리가 실제로 어떻게 작동하는지 보여주는 메인 루프입니다.

```python
# 두 작업을 병렬로 실행하여 로봇 제어와 데이터 수신을 동시에 처리
async def main():
    await asyncio.gather(
        robot_command(),
        receive_camera()
    )

asyncio.run(main())
```

---

## 4. 실전: 로봇 통신을 위한 비동기 프로그래밍

로봇과 주변기기들 간의 통신 시스템을 구축할 때, 각 기기의 독립적인 동작 과정에서 비동기성이 발생할 수 있습니다. 이를 처리하기 위해 비동기 프로그래밍을 적용하고, 발생할 수 있는 다양한 오류를 예외처리로 다루며, 프로세스 병목현상을 줄이기 위해 큐(queue)를 사용할 수 있습니다.

### 4.1 비동기 서버 구성 예제

```python
import asyncio

async def handle_robot(reader, writer):
    data = await reader.read(100)
    message = data.decode()
    print(f"Received: {message}")

    response = "Message received"
    writer.write(response.encode())
    await writer.drain()

    print("Closing the connection")
    writer.close()
    await writer.wait_closed()

async def main():
    server = await asyncio.start_server(handle_robot, '127.0.0.1', 8888)
    async with server:
        await server.serve_forever()

asyncio.run(main())
```

### 4.2 예외처리 예제

비동기 프로그래밍에서는 다양한 오류가 발생할 수 있으므로, 이를 적절히 처리하여 시스템의 안정성을 유지하는 것이 중요합니다.

```python
import asyncio

async def risky_operation():
    try:
        # 위험한 작업 수행
        result = 1 / 0
    except ZeroDivisionError as e:
        print(f"Error occurred: {e}")
    else:
        print("Operation succeeded")
    finally:
        print("Cleaning up resources")

asyncio.run(risky_operation())
```

### 4.3 큐를 활용한 작업 분산 처리

여러 비동기 작업이 동시에 실행될 때, 작업 간 병목 현상을 줄이기 위해 큐(queue)를 사용하면 유용합니다. 큐는 생산자-소비자 모델에서 자주 사용되며, 각 작업 간 흐름을 안전하게 조절할 수 있습니다.

```python
import asyncio

async def producer(queue):
    for i in range(5):
        await asyncio.sleep(1)
        item = f"item {i}"
        await queue.put(item)
        print(f"Produced {item}")

async def consumer(queue):
    while True:
        item = await queue.get()
        if item is None:
            break
        print(f"Consumed {item}")
        queue.task_done()

async def main():
    queue = asyncio.Queue()

    producer_task = asyncio.create_task(producer(queue))
    consumer_task = asyncio.create_task(consumer(queue))

    await producer_task
    await queue.put(None)  # 소비자에게 작업 종료를 알림
    await consumer_task

asyncio.run(main())
```

이 예시들은 비동기 프로그래밍을 활용해 로봇과 컴퓨터 간 통신을 처리하고, 발생할 수 있는 오류를 예외처리로 다루며, 큐를 사용하여 작업을 효율적으로 분산하는 방식을 보여줍니다.

---

## 5. 마무리 및 다음 단계

- 로봇 제어 중 입력과 감지 데이터를 병렬로 처리하는 데 `asyncio`는 매우 유용
- 흐름 제어를 위한 `Event`, `Semaphore`는 실제 시스템에서 자주 사용됨
- 다음 단계: 영상 처리 모델과 연결된 실시간 제어 예제 실습
