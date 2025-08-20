This week's focus was on a core computer vision task: real-time object detection. I implemented a video processing pipeline using the state-of-the-art Ultralytics YOLOv11 model to detect people in a video stream.

For this, I had to set my environment for YOLO11 again. For this, I first installed the ultralytics library using pip: pip install ultralytics. 
For this, we were required to download yolo11s.pt, but here I faced a silly error. In the code, I had entered model = YOLO('yolov11s.pt') instead of model = YOLO('yolo11s.pt'), which was giving me some trouble getting the file. 

After rectifying this error, I began with my first task. 

My first task was to build a Python script that loads the YOLOv11s model, processes video frames, and draws bounding boxes around detected persons. The script, yolo_person_detection_base.py, functions as my core pipeline.

We first load the YOLO model from the local yolov11s.pt file.
It uses cv2.VideoCapture to read the input video frame by frame.
The model.predict() function is called on each frame to perform inference. I used the classes=[0] argument to specifically filter for the person class, as its ID in the COCO dataset is 0.
The script then iterates through the detection results and uses cv2.rectangle and cv2.putText to draw a green bounding box and a confidence score label on each detected person.
Finally, it writes the annotated frames to an output video file using cv2.VideoWriter.

To understand the impact of different model settings, I conducted a series of experiments by adjusting the imgsz (image size) and conf (confidence threshold) arguments in the model.predict() function.

For the base file, we used  imgsz 640 and conf 0.25. The observations for this were: The accuracy was good. It detected most people properly. Whilst the processing was at a moderate speed. 

For the yolo_persondetection_smallerspeedmod.py, we used  imgsz 320 and conf 0.25. The observations for this were: The processing speed was significantly faster compared to the base. In some instances, small and distant people were missed due to the lower resolution. 

For the yolo_persondetection_higherconfidencethreshold.py, we used  imgsz 640 and conf 0.70. The observations for this were: Overall, it had fewer detections. It did eliminate some false positives, but also missed a few people with lower confidence scores.
