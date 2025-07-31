Firstly, I had to understand what OpenCV is, so I spent a good chunk of time to figure that out.

After setting up my Python Directory and Virtual Environment, I installed OpenCV using `pip install opencv-python numpy`. Then, knowing that GStreamer was a key part of the upcoming work, I installed its core libraries and a comprehensive set of plugins using Homebrew. This took a little while, as it compiles various components.

Then came PyGObject.

This was where I hit my first significant snag! When I tried to import `Gst` from `gi.repository` after installing `pygobject`, I encountered errors about `libglib-2.0.0.dylib` and `libgobject-2.0.0.dylib` not being found. The traceback showed warnings about `GLib-GIRepository-WARNING` and `gi._error.GError`.

Then, I learned that Homebrew installs libraries to `/opt/homebrew/lib`. My system's dynamic linker and Python's `gi` (PyGObject) needed to be explicitly told where to look. I fixed this by adding specific environment variables to my `~/.zprofile` file.

I opened `~/.zprofile` (using `code ~/.zprofile` for convenience in VS Code) and added these two lines at the end:

`export PKG_CONFIG_PATH="/opt/homebrew/lib/pkgconfig:$PKG_CONFIG_PATH"
export GI_TYPELIB_PATH="/opt/homebrew/lib/girepository-1.0:$GI_TYPELIB_PATH"`

Then, reinstalled PyGObject using pip install pygobject. 

Now, the environment setup was complete, and I began to work on the 4 problems given. 

1. Basic Drawing and Processing

Here, I first imported the necessary libraries, including `cv2` for all my computer vision tasks. I then loaded the `stuff.jpg` image from its path into a NumPy array, which is how OpenCV represents images. A key detail I learned is that OpenCV stores pixel values in **BGR** format (Blue, Green, Red) by default. 

After successfully loading the image, I retrieved its height and width. I then proceeded to use various drawing functions to perform the required operations on the image. I used `cv2.line`, `cv2.rectangle`, `cv2.circle`, and `cv2.putText` to define points, shapes, colors (in BGR format like `(0, 255, 0)` for green), and text overlays.

Next, I resized the image to half its original size using `cv2.resize()`. I used the `cv2.INTER_AREA` interpolation method, which is a good choice for shrinking images.

Finally, since the image is just a NumPy array, I was able to use array slicing to crop a specific portion. I took the top-left quarter of the resized image, and then saved this final processed image to its designated path in the `outputs/` folder.

2. Image Tiling

Here, I again began by importing the essential libraries. I loaded the `smarties.png` image and defined the dimensions I wanted for each tile.

To create the final tiled image, I first created a large, empty canvas using `np.zeros()`. This gave me a NumPy array filled with zeros, which appears as a black background i.e. black pixels. The canvas had the correct dimensions to hold a 2x2 grid of my resized tiles. 

The core of the tiling operation was then performed using NumPy slicing. I precisely assigned the resized `smarties` image to four different regions of the canvas. For example, `tiled_image[0:tile_size[1], 0:tile_size[0]]` assigned the image to the top-left quadrant of the canvas, and I repeated this for the other three quadrants with the correct slicing coordinates.

Once the tiling was complete, I saved the final composite image to my `outputs/` folder in `.jpg` format.

3. Video Overlaying

Here, I first imported the necessary libraries: `cv2` for video processing, `os` for managing file paths, and `datetime` to handle the video's timing information.

My first step was to open the video file, `vtest.avi`, using `cv2.VideoCapture()`. I also retrieved important video properties like frames per second (`fps`), total number of frames, and the total duration in milliseconds, which I'd need for my calculations later.

Next, I set up the `cv2.VideoWriter()` to prepare for saving the output video. I had to choose a codec, and I used `cv2.VideoWriter_fourcc(*'XVID')` as it's a reliable choice for `.avi` files. I specified the output path to be in my `outputs/` folder, ensuring the video would have the same FPS and dimensions as the original. I also decided to save only the first 10 seconds of the video, as asked, which meant I would only write a fixed number of frames.

I then started a `while True` loop to process the video frame by frame. Inside the loop, `cap.read()` would get the next frame and a boolean value (`ret`). The loop would break if `ret` were `False`, which happens when the video reaches its end.

Within the loop, I calculated the elapsed time and remaining time using `cap.get()` to find the video's current position. I used the `datetime` library to format these times into a clean, readable string (e.g., `0:00:05.123`).

After that, I used `cv2.putText()` to overlay this time information onto the current frame. I chose a specific color, font, and position for the text so it was clearly visible.

Finally, I added an `if` condition to check if I had processed the required number of frames (10 seconds worth). If so, the modified frame was written to my output video file using `out.write()`.

4. Side b Side Video Player

Here, I started by importing the necessary libraries: `cv2` and `numpy`. I also imported `os` for path managemt. 

The key to this exercise was opening the video file, `vtest.avi`, **twice**, using two separate `cv2.VideoCapture()` objects (`cap1` and `cap2`). This allowed me to process frames from two streams simultaneously, even though they were from the same source file.

I defined a target resolution of 1920x1080 (1080p) for my final video and calculated that each stream would need to be resized to 960x1080 to fit side-by-side.

Then, I set up the `cv2.VideoWriter()`, similar to the previous exercise. This time, I used `cv2.VideoWriter_fourcc(*'mp4v')` for a modern `.mp4` video format and specified my target resolution of 1920x1080.

I began my `while True` loop, where in each iteration, I read a frame from both `cap1` and `cap2`. The loop would break if either stream ran out of frames.

Inside the loop, I resized both frames (`frame1` and `frame2`) to my calculated dimensions (960x1080).

The most important part of this exercise was combining the two resized frames. I used the NumPy function `np.hstack()` (which stands for "horizontal stack") to concatenate the two frames side-by-side. This function is perfect for this task because it works directly on the NumPy array representation of the images.

Finally, I wrote this combined frame to my output video file using `out.write()`.

When the loop was complete, I made sure to release **all three** video objects: `cap1`, `cap2`, and `out`. This properly closes all streams and ensures the output file is saved correctly.
