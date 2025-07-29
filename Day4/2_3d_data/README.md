# Lecture 2: RealSense를 활용한 3차원 데이터 이해 실습

이 교육은 Intel RealSense 카메라를 활용하여 2D 이미지와 3D 거리 데이터를 실시간으로 수집하고, 이를 시각화 및 분석하는 과정을 단계적으로 학습합니다. 실습을 통해 realsense의 영상을 받아오는 방법, 3D data를 처리하는 방법 등을 학습합니다. 

## 0. RealSense란?

Intel에서 개발한 **RGB-D 카메라**로, RGB 영상과 Depth 영상(거리 정보를 담은 이미지)을 동시에 제공합니다. RealSense 시리즈는 컴퓨터 비전 기반의 3D 인식 기능을 필요로 하는 다양한 애플리케이션(로봇, 드론, 증강현실, 사람 인식 등)에 널리 사용됩니다.

### RealSense 카메라의 원리와 종류

RealSense 카메라는 **스테레오 기반 깊이 측정**을 사용합니다. 본 교육에서 사용될 모델은 D435F이며 간략한 스펙은 다음과 같습니다. 

- Range: 0.3 - 3m
- Depth Accuracy: <2% at 2m
- Depth Filter: IR Pass
- RGB Frame: 1920x1080, 30fps
- Depth Frame: 1280x720, 90fps    

대표적인 RealSense 모델군:
  - **D415**: 정밀한 깊이 측정, 좁은 시야각
  - **D435/D435i/D435F**: 넓은 시야각, 빠른 움직임에 적합, IR 패턴 포함
  - **L515**: 라이다 기반 거리 측정 방식 사용 (ToF)
  - **T265**: IMU가 포함된 자세 추정 전용 모델 (6DoF 추정 가능)

> 더 많은 기술적 정보와 API 문서는 Intel 공식 GitHub 저장소 [IntelRealSense/librealsense](https://github.com/IntelRealSense/librealsense)에서 확인할 수 있습니다.

---

### 준비 사항

- **하드웨어**: Intel RealSense (본 교육에서는 **D435F 모델** 사용)
- **소프트웨어 환경**: Python 3.8 이상

#### 설치해야 할 라이브러리

```bash
pip install pyrealsense2 opencv-python numpy
```

**numpy**: 행렬 및 벡터 연산을 효율적으로 처리하기 위한 수치 계산용 라이브러리입니다. RealSense에서 받은 Depth 데이터를 배열 형태로 다루는 데 필수적으로 사용됩니다.


## 1. 실시간 RGB + Depth 시각화

실시간으로 RGB와 Depth 영상을 수신하고 화면에 시각화하여 깊이 인식 감각을 형성합니다.

**예제 코드 (`1_realsense.py`):**

### 주요 함수 및 역할

- `rs.pipeline()` / `cfg.enable_stream(...)`: 카메라 스트림 구성 및 시작  
- `wait_for_frames()`: 프레임 수신  
- `get_color_frame()`, `get_depth_frame()`: RGB / Depth 프레임 추출  
- `cv2.imshow(...)`: OpenCV 창에 영상 출력  
- `cv2.convertScaleAbs(...)` + `applyColorMap(...)`: Depth 데이터를 컬러맵으로 변환  
- `cv2.getWindowProperty(...)`: 창이 닫혔는지 감지하여 루프 종료  


### 실행 결과
- 실시간 컬러 영상과 컬러맵 처리된 깊이 영상이 두 개의 창으로 표시됨  
- 거리에 따라 색상이 달라지는 Depth Map을 통해 공간감 체험 가능


## 2. Intrinsics 파라미터 확인 및 중심 픽셀 3D 위치 추출

RGB-D 카메라는 2D 이미지에서 각 픽셀이 실제 3D 공간상 어디에 위치하는지를 계산하기 위해 **카메라 내부 파라미터 (intrinsic parameters)**를 사용합니다. 이 파라미터들은 RealSense SDK를 통해 자동으로 제공되며, 일반적으로 다음과 같은 항목들로 구성됩니다:

- `fx`, `fy`: 이미지 축(`x`, `y`) 방향의 **초점 거리 (focal length)**
- `cx`, `cy`: 이미지의 **중심점 (principal point)**  
- `width`, `height`: 이미지 해상도  
- `distortion_coeffs`: **렌즈 왜곡 계수**  
  - RealSense는 Brown-Conrady 모델을 기본 사용하며, 경우에 따라 계수가 모두 0으로 설정되어 있기도 합니다.

이 Intrinsics 정보는 다음과 같은 작업에 필수적으로 사용됩니다:

- 2D 이미지에서 3D 포인트 복원
- 외부 캘리브레이션 매트릭스 계산
- SLAM, Visual Odometry, 포인트 클라우드 생성
- PnP 문제 해결을 통한 자세 추정 등

RealSense에서는 별도의 외부 캘리브레이션 없이도 위 정보를 API를 통해 기본적으로 제공하므로, 실습이나 프로토타이핑 단계에서는 즉시 활용할 수 있습니다.

**예제 코드 (`2_camera_intrinsics.py`):**

### 주요 함수 및 역할
`profile.as_video_stream_profile().intrinsics`: 카메라의 내부 파라미터 추출  
`get_distance(x, y)`: 특정 픽셀의 깊이값(depth)을 **미터 단위**로 반환  
`rs.rs2_deproject_pixel_to_point(...)`: 2D 픽셀 좌표 + depth → **3D 공간 좌표**로 변환  

### 출력 예시

```
Depth Camera Intrinsics:
  fx: 615.12, fy: 615.23
  cx: 320.00, cy: 240.00
  width: 640, height: 480

Pixel (320, 240)
 → Depth (Z): 0.833 m
 → 3D Position [X, Y, Z] (m): [0.0, 0.0, 0.833]
    X: right(+), Y: down(+), Z: forward(+)
```


## 3. 마우스 클릭으로 픽셀 → 3D 좌표 변환 실습  
RGB 화면에서 사용자가 클릭한 픽셀의 3D 위치를 실시간으로 확인합니다. 이를 위해서는 RGB 영상과 depth 영상의 픽셀 좌표를 일치시켜야 합니다. 이 과정으로 정렬(align)이라고 부릅니다. 

> **RGB-Depth 정렬 (`align`)**: RealSense는 Color 센서와 Depth 센서가 서로 다른 위치에 장착되어 있기 때문에, 두 이미지의 픽셀 좌표가 일치하지 않을 수 있습니다. `rs.align(rs.stream.color)`을 사용하면 Depth 프레임을 RGB 프레임 기준으로 정렬하여, 동일한 픽셀 좌표계에서 처리할 수 있습니다.

또한, realsense는 다음과 같은 카메라 좌표계를 가집니다. 

> **3D 좌표계 기준 (카메라 좌표계)**  
  `rs.rs2_deproject_pixel_to_point()`로 얻은 3D 좌표는 RealSense 카메라 좌표계를 따릅니다:  
 X: 오른쪽으로 갈수록 +  
 Y: 아래로 갈수록 +  
 Z: 카메라에서 멀어질수록 + (정면 방향)  


**예제 코드 (`3_click_to_3d.py`):**


### 주요 함수 및 역할

- `cv2.setMouseCallback(...)`: 마우스 클릭 이벤트 연결  
- `align = rs.align(rs.stream.color)`: RGB와 Depth 프레임 정렬  
- `get_distance(x, y)`: 클릭한 위치의 거리값 추출  
- `rs.rs2_deproject_pixel_to_point(...)`: 2D 픽셀을 3D 좌표로 변환  


### 실행 결과

RGB 창에서 아무 위치나 클릭하면 해당 좌표의 깊이 및 3D 위치가 콘솔에 출력됨

```
Clicked Pixel: (312, 254)
 → Depth (Z): 0.782 m
 → 3D Position [X, Y, Z] (m): [0.017, -0.005, 0.782]
```

**참고:**  
일부 픽셀에서는 적외선 센서가 거리 정보를 인식하지 못할 수 있습니다. 이 경우 `get_distance(x, y)`가 `0,0`을 반환하며, 3D 좌표 계산 결과도 `[0.0, 0.0, 0.0]`처럼 **의미 없는 값**이 됩니다. 따라서 클릭 좌표의 깊이값이 0인 경우는 반드시 **예외 처리**가 필요합니다.


## 4. 자세 인식과 6DoF 개념 확장 (선택)

**6DoF**는 3차원 공간에서의 물체 자세(Pose)를 의미하며,  
3개의 위치 정보 (X, Y, Z)와 3개의 회전 정보 (Roll, Pitch, Yaw)를 포함합니다.  
이 개념은 로봇, 드론, 증강현실, 객체 추적 등 다양한 공간 기반 애플리케이션에서 핵심적으로 사용됩니다.


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
