from ultralytics import YOLO

if __name__ == "__main__":
	#epochs중 가장 뛰어난 성능의 가중치 불러오기
	model = YOLO("runs/detect/train/weights/best.pt")
	results=model(source="eval_image_2.png",save=True)
	results[0].show()  # Display results