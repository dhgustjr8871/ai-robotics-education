from ultralytics import YOLO

if __name__ == "__main__":
	# Load a pretrained YOLO11n model
	model = YOLO("yolo11n-obb.yaml").load("weights/obb/best.pt")

	results = model.train(data="datasets/obb/data.yaml", epochs=1000, imgsz=1024, device=0)
	metrics = model.val()

	results=model(source="eval_image.png",save=True)
	results[0].show()  # Display results

	path = model.export(format="onnx")  # Returns the path to the exported model