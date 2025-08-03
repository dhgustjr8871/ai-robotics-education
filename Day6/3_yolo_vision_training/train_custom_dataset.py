from ultralytics import YOLO

if __name__ == "__main__":
	# Load a pretrained YOLO11n model
	model = YOLO("yolo11n-obb.yaml").load("weights/obb/best.pt")

	results = model.train(data=r"data_set_obb\data.yaml", epochs=150, imgsz=640, device=0)
	metrics = model.val()

	results=model(source="eval_image_1.jpg",save=True)
	results[0].show()  # Display results

	path = model.export(format="onnx")  # Returns the path to the exported model