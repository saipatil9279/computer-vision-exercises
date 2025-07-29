import cv2
import numpy as np
import os

# 1. Read a single sample image.
image_path = 'smarties.png'
img = cv2.imread(image_path)

if img is None:
    print(f"Error: Could not read image {image_path}. Please check the path and file existence.")
else:
    # Get image dimensions
    height, width, _ = img.shape

    tile_size = (400, 400)
    resized_img = cv2.resize(img, tile_size, interpolation=cv2.INTER_AREA)

    # 2. Tile it into a 2x2 grid.
    # Create an empty canvas for the tiled image
    tiled_height = tile_size[1] * 2
    tiled_width = tile_size[0] * 2
    tiled_image = np.zeros((tiled_height, tiled_width, 3), dtype=np.uint8)

    # Place the resized image into each quadrant
    tiled_image[0:tile_size[1], 0:tile_size[0]] = resized_img       # Top-left
    tiled_image[0:tile_size[1], tile_size[0]:tiled_width] = resized_img # Top-right
    tiled_image[tile_size[1]:tiled_height, 0:tile_size[0]] = resized_img # Bottom-left
    tiled_image[tile_size[1]:tiled_height, tile_size[0]:tiled_width] = resized_img # Bottom-right

    # 3. Save the tiled image under outputs/.
    output_path = os.path.join('outputs', 'output_tiled_image.jpg')
    cv2.imwrite(output_path, tiled_image)
    print(f"Tiled image saved to: {output_path}")