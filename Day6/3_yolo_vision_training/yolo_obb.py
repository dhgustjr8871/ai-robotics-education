from ultralytics import YOLO

if __name__ == "__main__":
    # Load a model
    #model = YOLO("yolo11n-obb.yaml")  # build a new model from YAML
    #model = YOLO("yolo11n-obb.pt")  # load a pretrained model (recommended for training)
    model = YOLO("yolo11n-obb.yaml").load("yolo11n.pt")  # build from YAML and transfer weights

    # Train the model
    results = model.train(data="dota8.yaml", epochs=50, imgsz=640, device=0)
    results = model(source="eval_image_2.png",save=True)
    results[0].show()  # Display results