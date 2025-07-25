from ultralytics import YOLO

if __name__ == "__main__":
	# Load a pretrained YOLO11n model
	model = YOLO("yolo11n.yaml").load("yolo11n.pt")

	results = model.train(data=r"datasets\guide_objects.yaml", epochs=100, imgsz=640, device=0)
	metrics = model.val()

	results=model(source="eval_image_1.jpg",save=True)
	results[0].show()  # Display results

	path = model.export(format="onnx")  # Returns the path to the exported model