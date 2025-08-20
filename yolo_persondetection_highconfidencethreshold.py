import cv2
import os
from ultralytics import YOLO

# Load the YOLOv11s model. 
model = YOLO('yolo11s.pt')

# Path to the input video and the output directory
input_video_path = 'vtest.avi'
output_dir = 'outputs'

# Ensuring that the output directory exists
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Open the video file for video Processing
cap = cv2.VideoCapture(input_video_path)

if not cap.isOpened():
    print(f"Error: Could not open video file {input_video_path}")
    exit()

# Get video properties for the output file
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)

# Setting up the VideoWriter to save the output video
output_video_path = os.path.join(output_dir, 'yolo_person_detection_highconfidence_threshold.mp4')
fourcc = cv2.VideoWriter_fourcc(*'mp4v') # Codec for MP4
out = cv2.VideoWriter(output_video_path, fourcc, fps, (frame_width, frame_height))

print("Starting base person detection pipeline...")

# Process video frame by frame
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Running theyolo inference using higher confidence threshold (0.7)
    results = model.predict(source=frame, imgsz=640, conf=0.7, classes=[0], verbose=False)

    # Process results and draw bounding boxes
    for result in results:
        boxes = result.boxes
        for box in boxes:
            # Get bounding box coordinates
            x1, y1, x2, y2 = map(int, box.xyxy[0])

            # Get confidence score and label
            conf = box.conf[0]
            label = f'Person: {conf:.2f}'

            # Draw the bounding box and label using OpenCV
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Write the processed frame to the output video
    out.write(frame)

# Release resources and finalize the output file
cap.release()
out.release()
cv2.destroyAllWindows()

print(f"Base detection complete. Output saved to: {output_video_path}")