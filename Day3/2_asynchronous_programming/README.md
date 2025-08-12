# Lecture 2: 로봇 원격 제어를 위한 비동기 프로그래밍 실습
본 강의에서는 로봇과 컴퓨터 간의 실시간 통신, 특히 카메라 데이터 수신과 로봇 명령 처리를 병렬로 처리해야 하는 상황을 위한 **Python 비동기 프로그래밍 기초와 실습 예제**를 학습합니다. 특히, `Event`, `Semaphore`와 같은 흐름 제어 기법은 명령 전송과 이미지 처리 간 충돌을 방지하고, 시스템 자원의 안전한 사용을 보장하는 데 필수적입니다.

예제를 통해 다음 핵심 개념을 실습합니다:
- 비동기 함수 정의와 실행 (`async`, `await`)
- 여러 작업 동시 실행 (`create_task`, `gather`)
- 흐름 제어를 위한 `Event`, `Semaphore` 사용법


## 1. Python asyncio 기본 구조
### 1.1 비동기 함수 정의와 호출
비동기 함수는 `async def`로 정의하며, 내부에서 `await`을 사용해 비동기적으로 동작할 수 있는 작업을 수행할 수 있습니다. 이는 긴 작업이 다른 작업을 막지 않도록 합니다.

#### 예제코드(1_greet.py):
```python
import asyncio # asyncio 모듈 import

# 비동기 함수 정의: 1초 후 인사 메시지 출력
async def greet():
    await asyncio.sleep(1)
    print("Hello Robot")

# 현재 파일이 직접 실행될 때만 아래 코드를 실행
if __name__ == "__main__":
    asyncio.run(greet())
```

* `if __name__ == "__main__":` 이 조건문은 현재 파일이 직접 실행됐을 때만 참이 되는 조건문입니다. 다른 파일에서 import 될 경우에는 실행하지 않도록 해줍니다. 앞으로 실습에 자주 등장할 예정이니 익숙해지면 좋겠습니다.


### 1.2 여러 작업을 동시에 실행하기 (`create_task`, `gather`)
`asyncio.create_task()`나 `asyncio.gather()`를 사용하면 여러 개의 비동기 작업을 동시에 실행할 수 있습니다. 이는 병렬 작업이 필요한 로봇 시스템에서 필수적인 개념입니다. 아래 예제코드에서 main 함수는 두 개의 비동기 작업을 실행하고, 각각의 작업이 완료될 때까지 기다리는 역할을 합니다.

#### 예제코드(2_concurrent_tasks.py):
```python
# 여러 작업을 동시에 실행하기 
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
```


## 2. 흐름 제어 도구 실습
### 2.1 asyncio.Event – 상태 변화에 따른 동작 제어
`asyncio.Event`는 이벤트가 발생할 때까지 대기하고, 특정 시점에 한 번만 모든 대기 중인 작업을 깨우는 용도로 사용됩니다. 상태 변화 기반의 동작 흐름을 설계할 때 유용합니다. `event`객체가 처음 생성되면 unset 상태이다가 `set()`호출 시에 모두 깨어나서 이후 로직을 실행합니다.

#### 예제코드(3_event_example.py):
```python
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
```

### 2.2 asyncio.Semaphore – 동시 접근 제한
`asyncio.Semaphore`는 동시에 접근할 수 있는 비동기 작업의 수를 제한할 수 있는 동기화 도구입니다. 로봇 시스템에서 자원을 동시에 사용하는 작업이 많을 때 충돌을 방지하는 데 활용됩니다. 아래 예제코드에서는 동시에 2개의 작업만 자원에 접근 가능한 세마포어 `sema`를 생성합니다. 따라서 `main()`에서 작업 A, B, C를 동시에 실행하지만 2개 제한으로 인해 A, B만 먼저 실행되고 C는 대기합니다.

#### 예제코드(4_semaphore_example.py):
```python
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
```


## 3. 예제: 로봇 제어와 카메라 데이터 수신을 병렬로 처리하기
이 예제는 실시간 로봇 제어 시나리오를 단순화한 비동기 처리 구조를 보여줍니다. 두 개의 작업을 동시에 실행하는 구조를 통해 병렬 처리 방식의 이해를 돕습니다.

- `robot_command()`는 사용자로부터 명령어를 입력받아 전송하는 흐름을 시뮬레이션합니다.
- `receive_camera()`는 카메라가 프레임을 실시간으로 수신하는 상황을 흉내냅니다.
- 이 두 작업은 `asyncio.gather()`로 동시에 실행되며, 실제 로봇 시스템에서 입력 처리와 센서 수신이 동시에 이루어지는 구조를 반영합니다.

이를 통해 병렬 처리, 흐름 제어, 이벤트 루프 실행 구조 등을 실습합니다.

### 3.1 로봇 명령 처리

#### 예제코드(5_robot_command.py):
```python
# 사용자 입력을 받아 로봇 명령을 전송하는 구조
async def robot_command():
    while True:
        cmd = input("Enter command: ") # 사용자로부터 명령 입력
        print(f"Sending command: {cmd}") # 명령 전송 시뮬레이션
        await asyncio.sleep(1)  # 네트워크 지연 상황 시뮬레이션
```

### 3.2 카메라 데이터 수신 시뮬레이션

실시간 카메라 프레임 수신을 흉내 내는 함수로, 실제 이미지 수신과 유사한 주기로 동작하는 구조입니다.

#### 예제코드(5_robot_command.py):
```python
# 주기적으로 프레임을 받아오는 구조
async def receive_camera():
    for i in range(5):
        print(f"[CAMERA] Frame {i} received") # 프레임 수신 출력
        await asyncio.sleep(0.5) # 다음 프레임까지 대기
```

### 3.3 통합 실행

앞서 정의한 두 비동기 함수를 동시에 실행하여 병렬 처리가 실제로 어떻게 작동하는지 보여주는 메인 루프입니다.

#### 예제코드(5_robot_command.py):
```python
# 두 작업을 병렬로 실행하여 로봇 제어와 데이터 수신을 동시에 처리
async def main():
    await asyncio.gather(
        robot_command(),
        receive_camera()
    )

asyncio.run(main())
```


## 4. 실전: 로봇 통신을 위한 비동기 프로그래밍

로봇과 주변기기들 간의 통신 시스템을 구축할 때, 각 기기의 독립적인 동작 과정에서 비동기성이 발생할 수 있습니다. 이를 처리하기 위해 비동기 프로그래밍을 적용하고, 발생할 수 있는 다양한 오류를 예외처리로 다루며, 프로세스 병목현상을 줄이기 위해 큐(queue)를 사용할 수 있습니다.

### 4.1 비동기 서버 구성 예제
이 예제는 asyncio를 사용해 간단한 TCP 서버를 구현하는 코드입니다. `handle_robot()` 함수는 클라이언트로부터 데이터를 수신하고 응답을 보내는 역할을 합니다. `asyncio.start_server()`로 서버를 생성하고, 지정된 `IP(127.0.0.1)`와 `포트(8888)`에서 연결 요청을 기다립니다. 비동기 방식이므로 여러 클라이언트가 접속해도 병렬로 처리할 수 있습니다.

#### 예제코드(6_async_server.py):
```python
# 4.1 비동기 서버 구성 예제
import asyncio

# 클라이언트 연결이 발생할 때 실행되는 핸들러
# reader: 클라이언트에서 오는 데이터를 읽는 스트림
# writer: 클라이언트로 데이터를 보내는 스트림
async def handle_robot(reader, writer):
   
    # 클라이언트로부터 최대 100바이트 데이터를 읽음 (비동기)
    data = await reader.read(100)
    message = data.decode()
    print(f"Received: {message}")

    # 클라이언트에게 응답 전송
    response = "Message received"
    writer.write(response.encode())
    await writer.drain()

    print("Closing the connection")
    writer.close()                  # 연결 종료 요청
    await writer.wait_closed()      # 실제 종료까지 대기

async def main():
    # 127.0.0.1:8888에서 handle_robot()을 호출하는 서버 생성
    server = await asyncio.start_server(handle_robot, '127.0.0.1', 8888)
    
    # 서버를 비동기 컨텍스트로 실행 (Ctrl+C로 종료)
    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())
```

### 4.2 예외처리 예제

비동기 프로그래밍 환경에서는 네트워크 지연, 연결 끊김, 잘못된 데이터 등 다양한 오류가 발생할 수 있습니다.  
이 예제는 **`try` / `except` / `else` / `finally`** 구문을 사용해 예외를 처리하고, 오류 여부와 관계없이 자원 정리를 수행하는 방법을 보여줍니다.

- **`try` 블록**: 예외가 발생할 가능성이 있는 코드를 실행  
- **`except` 블록**: 특정 예외를 잡아 처리  
- **`else` 블록**: 예외가 발생하지 않았을 때만 실행  
- **`finally` 블록**: 예외 발생 여부와 관계없이 항상 실행 (자원 해제, 연결 종료 등에 사용)  

#### 예제코드(7_exception_handling.py):
```python
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
```

### 4.3 큐를 활용한 작업 분산 처리

여러 비동기 작업이 동시에 실행될 때, 작업 간 병목 현상을 줄이기 위해 **큐(queue)** 를 사용하면 유용합니다. 큐는 **생산자-소비자 모델**에서 자주 사용되며, 각 작업 간 데이터 흐름을 안전하게 조절할 수 있습니다.

- **`asyncio.Queue`**: 비동기 환경에서 안전하게 데이터를 주고받을 수 있는 큐
- **생산자(Producer)**: 데이터를 생성하여 큐에 넣음
- **소비자(Consumer)**: 큐에서 데이터를 꺼내 처리
- **종료 신호(None)**: 소비자에게 더 이상 처리할 데이터가 없음을 알림

#### 예제코드(8_queue_producer_consumer.py)
```python
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
```

## 5. 마무리
이번 실습에서는 `asyncio`를 사용해 **로봇 제어와 데이터 수신을 병렬로 처리**하는 방법을 익혔습니다. `Event`와 `Semaphore`로 흐름을 제어하고, 큐를 이용해 작업을 안전하게 분산하는 패턴도 실습했습니다. 이제 이를 네트워크, 센서, 영상 처리와 결합하면 **실시간 제어 시스템**에 적용할 수 있습니다.