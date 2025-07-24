# OpenCV를 활용한 이미지 전처리 기법

본 자료는 YOLO 등 딥러닝 기반 객체 탐지 이전 단계에서의 전처리 기법들을 설명하고, 각 기법별 예제를 통해 OpenCV 사용법을 학습하는 것을 목표로 합니다.

## 목차
1. 이미지 불러오기 및 기본 처리
2. 블러링 기법 (Gaussian, Median, Blur)
3. 엣지 검출 (Canny, Sobel)
4. 컨투어 추출 및 윤곽선 그리기
5. 바운딩 박스 그리기 (Bounding Box)
6. 종합 예제

---

## 1. 이미지 불러오기 및 기본 처리

```python
import cv2

# 이미지 불러오기
img = cv2.imread("sample.jpg")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
