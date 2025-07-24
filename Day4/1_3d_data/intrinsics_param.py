import pyrealsense2 as rs
import numpy as np

# 파이프라인 설정
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
profile = pipeline.start(config)

# 프레임 1~2개 버리고 안정된 프레임 받기
for _ in range(5):
    frames = pipeline.wait_for_frames()

depth_frame = frames.get_depth_frame()

# 인트린직 파라미터 얻기
depth_intrin = depth_frame.profile.as_video_stream_profile().intrinsics

# 확인용 출력
print("Intrinsics:")
print(f"fx: {depth_intrin.fx}, fy: {depth_intrin.fy}")
print(f"cx: {depth_intrin.ppx}, cy: {depth_intrin.ppy}")

# 임의의 픽셀 좌표 선택 (예: 화면 중앙)
x, y = 320, 240

# 해당 픽셀의 깊이값 (단위: mm)
depth = depth_frame.get_distance(x, y)  # 단위: meter

# 픽셀 → 카메라 좌표계 3D로 변환
point_3d = rs.rs2_deproject_pixel_to_point(depth_intrin, [x, y], depth)

print(f"Pixel ({x}, {y}) → 3D Position (X, Y, Z): {point_3d}")

