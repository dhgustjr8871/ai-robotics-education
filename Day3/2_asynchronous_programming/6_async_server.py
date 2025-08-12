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