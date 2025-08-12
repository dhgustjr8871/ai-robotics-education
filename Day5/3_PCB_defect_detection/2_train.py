from ultralytics import YOLO

if __name__ == '__main__':
    # Load a model
	model = YOLO("yolo11n.yaml").load("yolo11n.pt")  # build from YAML and transfer weights
	# Train the model
	results = model.train(data="datasets/data.yaml", epochs=50, imgsz=640, device=0)
	results[0].show()