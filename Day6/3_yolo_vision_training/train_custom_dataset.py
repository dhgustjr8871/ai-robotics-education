from ultralytics import YOLO

if __name__ == "__main__":
	# Load a pretrained YOLO11n model
	model = YOLO("YOLO11n-obb.yaml").load("YOLO11n-obb.pt")

	results = model.train(data=r"data_set_obb\data.yaml", epochs=250, imgsz=1024, device=0)
	metrics = model.val()

	results=model(source="image.png",save=True)
	results[0].show()  # Display results

	path = model.export(format="onnx")  # Returns the path to the exported model