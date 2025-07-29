import cv2
import numpy as np
import os

video_path = 'vtest.avi'
output_combined_video_path = os.path.join('outputs', 'output_side_by_side_1080p.mp4') # Use MP4 for better compatibility

# Target resolution for the combined video
target_width = 1920
target_height = 1080

# 1. Use the vtest.avi stream twice and duplicate the capture.
cap1 = cv2.VideoCapture(video_path)
cap2 = cv2.VideoCapture(video_path) # Duplicate capture

if not cap1.isOpened() or not cap2.isOpened():
    print(f"Error: Could not open one or both video files {video_path}.")
else:
    # Get properties from the first capture
    fps = cap1.get(cv2.CAP_PROP_FPS)
    original_width = int(cap1.get(cv2.CAP_PROP_FRAME_WIDTH))
    original_height = int(cap1.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Calculate desired width and height for each individual stream to fit 1080p
    # For side-by-side, each stream will take half of the target_width
    individual_stream_width = target_width // 2
    individual_stream_height = target_height

    # Define the codec and create VideoWriter object for saving the combined video
    fourcc = cv2.VideoWriter_fourcc(*'mp4v') 
    out = cv2.VideoWriter(output_combined_video_path, fourcc, fps, (target_width, target_height))

    if not out.isOpened():
        print(f"Error: Could not open video writer for {output_combined_video_path}. Check codec or permissions.")
    else:
        frame_num = 0
        while True:
            ret1, frame1 = cap1.read()
            ret2, frame2 = cap2.read()

            if not ret1 or not ret2:
                break # Break if either stream ends

            # Resize each frame to fit the target resolution for individual streams
            resized_frame1 = cv2.resize(frame1, (individual_stream_width, individual_stream_height), interpolation=cv2.INTER_AREA)
            resized_frame2 = cv2.resize(frame2, (individual_stream_width, individual_stream_height), interpolation=cv2.INTER_AREA)

            # 2. Display both streams side by side, synchronized.
            # Concatenate frames horizontally
            combined_frame = np.hstack((resized_frame1, resized_frame2))

            # 3. Save the resulting combined video at 1080p (1920x1080) under outputs/.
            out.write(combined_frame)

            frame_num += 1
            # Break if 'q' is pressed (optional, for live viewing)
            # if cv2.waitKey(1) & 0xFF == ord('q'):
            #     break

        print(f"Combined video saved to: {output_combined_video_path}")

    cap1.release()
    out.release()
    print("Side-by-side video processing finished.") 