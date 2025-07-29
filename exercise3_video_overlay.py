import cv2
import os
import datetime

video_path = 'vtest.avi'
output_clip_path = os.path.join('outputs', 'output_video_overlay_clip.avi')
clip_duration_seconds = 10 # Save first 10 seconds

# 1. Open vtest.avi with OpenCV.
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print(f"Error: Could not open video file {video_path}.")
else:
    # Get video properties
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_duration_ms = frame_count / fps * 1000

    print(f"Video FPS: {fps:.2f}")
    print(f"Video Resolution: {width}x{height}")
    print(f"Total Frames: {frame_count}")
    print(f"Total Duration: {total_duration_ms / 1000:.2f} seconds")

    # Define the codec and create VideoWriter object for saving the clip
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    # Calculate the number of frames to save for the clip
    frames_to_save = int(clip_duration_seconds * fps)
    out = cv2.VideoWriter(output_clip_path, fourcc, fps, (width, height))

    frame_num = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Calculate elapsed and remaining time
        elapsed_time_ms = cap.get(cv2.CAP_PROP_POS_MSEC)
        remaining_time_ms = total_duration_ms - elapsed_time_ms

        elapsed_time_str = str(datetime.timedelta(milliseconds=int(elapsed_time_ms)))
        remaining_time_str = str(datetime.timedelta(milliseconds=int(remaining_time_ms)))

        # 2. On each frame, overlay text showing elapsed time vs. remaining time.
        text_elapsed = f"Elapsed: {elapsed_time_str}"
        text_remaining = f"Remaining: {remaining_time_str}"

        cv2.putText(frame, text_elapsed, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2, cv2.LINE_AA)
        cv2.putText(frame, text_remaining, (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2, cv2.LINE_AA)

        # 3. Save a short sample clip
        if frame_num < frames_to_save:
            out.write(frame)
        else:
            # Stop writing after the desired clip duration
            if frame_num == frames_to_save:
                print(f"Saved {clip_duration_seconds} seconds clip to: {output_clip_path}")
            pass

        frame_num += 1