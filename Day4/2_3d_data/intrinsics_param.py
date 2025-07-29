import pyrealsense2 as rs
import numpy as np

# 1. 파이프라인 및 스트림 설정
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

# 2. 스트리밍 시작
profile = pipeline.start(config)

try:
    # 3. 안정된 프레임을 위해 몇 개 버림
    for _ in range(5):
        frames = pipeline.wait_for_frames()

    # 4. 프레임에서 depth 추출
    depth_frame = frames.get_depth_frame()
    if not depth_frame:
        raise RuntimeError("Depth frame is not available.")

    # 5. Intrinsics 파라미터 얻기
    depth_intrin = depth_frame.profile.as_video_stream_profile().intrinsics

    print("🔍 Depth Camera Intrinsics:")
    print(f"  fx (focal length x): {depth_intrin.fx:.2f}")
    print(f"  fy (focal length y): {depth_intrin.fy:.2f}")
    print(f"  cx (principal point x): {depth_intrin.ppx:.2f}")
    print(f"  cy (principal point y): {depth_intrin.ppy:.2f}")
    print(f"  width: {depth_intrin.width}, height: {depth_intrin.height}")

    # 6. 화면 중앙 픽셀 지정
    center_x = int(depth_intrin.width / 2)
    center_y = int(depth_intrin.height / 2)

    # 7. 중심 픽셀의 깊이 값 (단위: meter)
    depth = depth_frame.get_distance(center_x, center_y)  # 단위: meter

    # 8. 픽셀 좌표 → 카메라 좌표계로 변환
    point_3d = rs.rs2_deproject_pixel_to_point(
        depth_intrin, [center_x, center_y], depth
    )

    print(f"\n📌 Pixel ({center_x}, {center_y})")
    print(f" → Depth (Z): {depth:.3f} m")
    print(f" → 3D Position [X, Y, Z] (m): {point_3d}")
    print("    X: right(+), Y: down(+), Z: forward(+)")

finally:
    pipeline.stop()
