# OpenCV 이미지 전처리 실습 가이드

이 문서는 YOLO와 같은 딥러닝 모델에 이미지를 입력하기 전, OpenCV를 활용하여 전처리를 수행하는 주요 기법들을 정리한 실습 가이드입니다. 각 기법에 대한 개념과 예제 코드를 단계적으로 소개합니다.

---

## OpenCV란?

OpenCV(Open Source Computer Vision Library)는 실시간 컴퓨터 비전 및 이미지 처리에 사용되는 오픈소스 라이브러리입니다. Python, C++, Java 등 다양한 언어를 지원하며, 객체 인식, 얼굴 검출, 이미지 필터링, 윤곽선 추출 등의 작업에 활용됩니다.

- 공식 사이트: [https://opencv.org](https://opencv.org)
- Python에서 주로 사용하는 모듈 이름: `cv2`

## 설치 방법

OpenCV와 matplotlib은 Python 환경에서 이미지 전처리와 시각화를 위한 필수 라이브러리입니다. 아래의 단계에 따라 설치할 수 있습니다.

### 1단계: 터미널(명령 프롬프트) 열기

운영체제에 따라 아래 방법으로 명령어 입력창을 엽니다:

- **Windows**: 시작 메뉴에서 "명령 프롬프트" 또는 "cmd" 검색 후 실행
- **macOS**: Spotlight에서 "Terminal" 검색 후 실행
- **Linux**: Ctrl + Alt + T 또는 애플리케이션 메뉴에서 "터미널" 실행

### 2단계: pip로 OpenCV 설치하기

```bash
pip install opencv-python
```

OpenCV를 사용하려면 Python 파일 가장 위에 다음과 같이 cv2 모듈을 import해야 합니다:

```python
import cv2
```
이 줄이 빠지면 OpenCV 함수들을 사용할 수 없습니다.


## matplotlib이란?
matplotlib은 Python에서 이미지나 그래프를 시각화할 때 사용하는 라이브러리입니다.
OpenCV는 기본적으로 `cv2.imshow()`로 GUI 창을 띄우지만, 여러 이미지의 결과를 비교하기 위해서는 `matplotlib.pyplot`을 사용하는 것이 더 유용합니다.