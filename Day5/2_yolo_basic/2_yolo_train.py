from ultralytics import YOLO

if __name__ == "__main__":
	# Load a YOLO11n model
	model = YOLO("yolo11n.yaml")

	# Train the model on the COCO8 example dataset for 100 epochs
	results = model.train(data="coco8.yaml", epochs=100, imgsz=640, device='cuda')

	# Run inference with the YOLO11n model on the 'dog.png' image
	results = model("image/dog.png", save=True)
