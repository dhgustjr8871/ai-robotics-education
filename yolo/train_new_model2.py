from ultralytics import YOLO

model = YOLO("yolo11n.yaml")#.load("yolo11n.pt")  # build from YAML and transfer weights

# Perform tracking with the model
results = model.train(data=r"guide_objects\guide_objects.yaml", epochs=50, imgsz=640, device=0)

results=model(source=r"11.jpg",save=True)