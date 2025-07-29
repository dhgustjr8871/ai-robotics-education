# Lecture 2: RealSense를 활용한 3차원 데이터 이해 실습

이 교육은 Intel RealSense 카메라를 활용하여 2D 이미지와 3D 거리 데이터를 실시간으로 수집하고, 이를 시각화 및 분석하는 과정을 단계적으로 학습합니다. 실습은 총 3개의 예제 코드로 구성되어 있으며, 각 단계마다 3차원 공간 인식의 핵심 개념과 함께 Python 코드 예제를 실행합니다.

## 1. RealSense란?

Intel에서 개발한 **RGB-D 카메라**로, RGB 영상과 Depth 영상(거리 정보를 담은 이미지)을 동시에 제공합니다.

- **주요 사용 분야**: 로봇 비전, 증강현실, 공간 인식, SLAM 등
- **핵심 출력**:
  - **RGB 이미지**: 640×480 해상도, 3채널 BGR 형식
  - **Depth 이미지**: 640×480 해상도, 1채널 거리값 (단위: meter)

---

### 준비 사항

- **하드웨어**: Intel RealSense (본 교육에서는 **D435F 모델** 사용)
- **소프트웨어 환경**: Python 3.8 이상

#### 설치해야 할 라이브러리

```bash
pip install pyrealsense2 opencv-python numpy
```

- **numpy**: 행렬 및 벡터 연산을 효율적으로 처리하기 위한 수치 계산용 라이브러리입니다.  
  RealSense에서 받은 Depth 데이터를 배열 형태로 다루는 데 필수적으로 사용됩니다.


## 2. 실시간 RGB + Depth 시각화 (`realsense.py`)

실시간으로 RGB와 Depth 영상을 수신하고 화면에 시각화하여 깊이 인식 감각을 형성합니다.

---

### 예제 코드 (`1_realsense.py`)

#### 주요 함수 및 역할

- `rs.pipeline()` / `cfg.enable_stream(...)`: 카메라 스트림 구성 및 시작  
- `wait_for_frames()`: 프레임 수신  
- `get_color_frame()`, `get_depth_frame()`: RGB / Depth 프레임 추출  
- `cv2.imshow(...)`: OpenCV 창에 영상 출력  
- `cv2.convertScaleAbs(...)` + `applyColorMap(...)`: Depth 데이터를 컬러맵으로 변환  
- `cv2.getWindowProperty(...)`: 창이 닫혔는지 감지하여 루프 종료  

---

### ▶ 실행 결과

- 실시간 컬러 영상과 컬러맵 처리된 깊이 영상이 두 개의 창으로 표시됨  
- 거리에 따라 색상이 달라지는 Depth Map을 통해 공간감 체험 가능


## 3. Intrinsics 파라미터 확인 및 중심 픽셀 3D 위치 추출 (`intrinsics_param.py`)

카메라 내부 파라미터 (`fx`, `fy`, `cx`, `cy`)를 확인하고 중심 픽셀의 3D 좌표를 추출합니다.

---

### ▶ 주요 함수 및 역할

- `profile.as_video_stream_profile().intrinsics`: 카메라 Intrinsics 객체 추출  
- `get_distance(x, y)`: 특정 픽셀의 거리값(m 단위) 추출  
- `rs.rs2_deproject_pixel_to_point(...)`: 2D 픽셀을 3D 월드 좌표로 변환  

---

### ▶ 출력 예시

```
Depth Camera Intrinsics:
  fx: 615.12, fy: 615.23
  cx: 320.00, cy: 240.00
  width: 640, height: 480

Pixel (320, 240)
 → Depth (Z): 0.833 m
 → 3D Position [X, Y, Z] (m): [0.0, 0.0, 0.833]
```


## 4. 마우스 클릭으로 픽셀 → 3D 좌표 변환 실습 (`click_to_3d.py`)

RGB 화면에서 사용자가 클릭한 픽셀의 3D 위치를 실시간으로 확인합니다.

---

### ▶ 주요 함수 및 역할

- `cv2.setMouseCallback(...)`: 마우스 클릭 이벤트 연결  
- `align = rs.align(rs.stream.color)`: RGB와 Depth 프레임 정렬  
- `get_distance(x, y)`: 클릭한 위치의 거리값 추출  
- `rs.rs2_deproject_pixel_to_point(...)`: 2D 픽셀을 3D 좌표로 변환  

---

### ▶ 실행 결과

- RGB 창에서 아무 위치나 클릭하면 해당 좌표의 깊이 및 3D 위치가 콘솔에 출력됨

```
Clicked Pixel: (312, 254)
 → Depth (Z): 0.782 m
 → 3D Position [X, Y, Z] (m): [0.017, -0.005, 0.782]
```


## 5. 자세 인식과 6DoF 개념 확장 (선택)

**6DoF**는 3차원 공간에서의 물체 자세(Pose)를 의미하며,  
3개의 위치 정보 (X, Y, Z)와 3개의 회전 정보 (Roll, Pitch, Yaw)를 포함합니다.  
이 개념은 로봇, 드론, 증강현실, 객체 추적 등 다양한 공간 기반 애플리케이션에서 핵심적으로 사용됩니다.

---

### 6자유도 (6 Degrees of Freedom, 6DoF)

3차원 공간에서 물체가 자유롭게 움직일 수 있는 여섯 가지 방향을 의미합니다.  
위치 이동 3가지와 회전 3가지를 포함하며, 다음과 같이 분류됩니다:

#### 위치 이동:
- **X축**: 좌우 이동  
- **Y축**: 상하 이동  
- **Z축**: 앞뒤 이동  

#### 회전 (Rotation):
- **Roll**: 앞을 기준으로 좌우로 기울기 *(비행기 날개처럼)*  
- **Pitch**: 옆을 기준으로 위아래 방향 회전  
- **Yaw**: 위에서 보는 방향 회전 *(방향 전환)*

(사진)

---

### 자세 추정 (Pose Estimation)

이러한 6DoF 정보를 추정하는 기술을 **자세 추정(Pose Estimation)**이라 하며,  
이 실습에서는 간단한 개념 소개와 대표 기술만 가볍게 다룹니다.  
자세 추정은 **RGB-D 카메라와 IMU**가 함께 사용될 때 더 정밀한 정보 획득이 가능합니다.

(사진)


## 마무리

이 실습을 통해 **RGB-D 카메라가 수집하는 데이터의 구조와 처리 방법**,  
그리고 **2D 이미지로부터 3D 공간 정보를 얻는 과정**을 이해할 수 있습니다.

추후에는 이 개념을 기반으로 다음과 같은 응용 분야로 확장할 수 있습니다:

- 로봇 비전 (Robot Vision)  
- SLAM (Simultaneous Localization and Mapping)  
- 3D Reconstruction (3차원 재구성)
