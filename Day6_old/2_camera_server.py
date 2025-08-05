# camera_server.py
import asyncio
import pyrealsense2 as rs
import numpy as np
import cv2

pipe = rs.pipeline()
cfg = rs.config()
cfg.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

async def camera_handler(reader, writer):
    addr = writer.get_extra_info('peername')
    print(f"[CameraServer] Connected from {addr}")

    try:
        while True:
            frames = pipe.wait_for_frames()
            color_frame = frames.get_color_frame()
            if not color_frame:
                continue

            color_image = np.asanyarray(color_frame.get_data())
            _, jpeg = cv2.imencode('.jpg', color_image)

            # 먼저 이미지 크기 전송 (4바이트)
            img_bytes = jpeg.tobytes()
            img_len = len(img_bytes)
            writer.write(img_len.to_bytes(4, 'big'))  # 길이 헤더 전송
            writer.write(img_bytes)  # 본문 전송
            await writer.drain()

            await asyncio.sleep(0.03)  # 약 30fps
    except asyncio.CancelledError:
        pass
    except Exception as e:
        print("Camera handler error:", e)
    finally:
        print(f"[CameraServer] Connection closed: {addr}")
        writer.close()

async def main(host='0.0.0.0', port=12346):
    pipe.start(cfg)
    server = await asyncio.start_server(camera_handler, host, port)
    print(f"[CameraServer] Listening on {host}:{port}")
    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Shutting down camera server...")
        pipe.stop()
        cv2.destroyAllWindows()
