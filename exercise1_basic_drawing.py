import cv2
import numpy as np
import os

# Creating an output directory
if not os.path.exists('outputs'):
    os.makedirs('outputs')

# 1. Read the image
image_path = 'stuff.jpg'
img = cv2.imread(image_path)

if img is None:
    print(f"Error: Could not read image {image_path}. Please check the path and file existence.")
else:
    # Get image dimensions for drawing
    height, width, _ = img.shape

    # 2. Draw one line, one rectangle, one circle, and overlay some text.
    # Line (top-left to bottom-right)
    cv2.line(img, (0, 0), (width, height), (0, 255, 0), 2) # Green line

    # Rectangle (top-left quarter)
    cv2.rectangle(img, (50, 50), (width // 2, height // 2), (255, 0, 0), 3) # Blue rectangle

    # Circle (center)
    center_x, center_y = width // 2, height // 2
    radius = min(center_x, center_y) // 4
    cv2.circle(img, (center_x, center_y), radius, (0, 0, 255), -1) # Red filled circle

    # Text overlay
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(img, 'Welcome Aboard!', (50, height - 50), font, 1, (255, 255, 255), 2, cv2.LINE_AA)

    # 3. Resize and crop the result.
    # Resize to half width and half height
    resized_img = cv2.resize(img, (width // 2, height // 2), interpolation=cv2.INTER_AREA)

    # Crop the top-left quarter of the resized image
    cropped_img = resized_img[0:resized_img.shape[0] // 2, 0:resized_img.shape[1] // 2]

    
    if len(cropped_img.shape) == 3 and cropped_img.shape[2] == 3:
        gray_cropped_img = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2GRAY)
        
        final_image_to_save = cropped_img
    else:
        final_image_to_save = cropped_img


    # 4. Saving the final image under an outputs/ folder.
    output_path = os.path.join('outputs', 'output_drawing_and_processing.jpg')
    cv2.imwrite(output_path, final_image_to_save)
    print(f"Processed image saved to: {output_path}")