from ultralytics import YOLO
import os

def run_perception():
    print("Loading PyTorch & YOLOv8 model for Autonomous Perception...")
    # Load the official pre-trained YOLOv8 model. 
    # It will automatically download 'yolov8n.pt' (nano version) which is fast and lightweight.
    model = YOLO("yolov8n.pt") 

    # We will use one of ultralytics' default built-in images of a street/bus
    # In a real project, this would be a frame from the KITTI dataset or your webcam.
    image_path = "https://ultralytics.com/images/bus.jpg"
    
    print(f"Running Inference on {image_path}...")
    
    # Run the model on the image
    results = model(image_path)
    
    # Process the results
    for result in results:
        # Save the image with bounding boxes drawn
        output_dir = "data"
        os.makedirs(output_dir, exist_ok=True)
        save_path = os.path.join(output_dir, "perception_output.jpg")
        
        result.save(filename=save_path)
        
        # Print the bounding boxes simulating data we would send to ROS 2
        print("\n--- DETECTED OBJECTS TO SEND TO C++ ROS NODE ---")
        boxes = result.boxes
        for box in boxes:
            # Class ID (e.g., 0 = person, 2 = car, 5 = bus)
            class_id = int(box.cls[0])
            class_name = model.names[class_id]
            
            # Confidence score
            confidence = float(box.conf[0])
            
            # Bounding box coordinates (xyxy)
            x1, y1, x2, y2 = box.xyxy[0].tolist()
            
            print(f"Detected: {class_name:10} | Confidence: {confidence:.2f} | Bounding Box: [{x1:.1f}, {y1:.1f}, {x2:.1f}, {y2:.1f}]")
            
        print(f"\nSaved visualization to: {save_path}")

if __name__ == "__main__":
    run_perception()
