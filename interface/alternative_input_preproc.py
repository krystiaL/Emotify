import cv2
import io
import os
import numpy as np
from PIL import Image
import tempfile

def is_image(file):
    try:
        #read image as byte file
        image_bytes = file.read()
        image_pil = Image.open(io.BytesIO(image_bytes))
        return image_pil
    except IOError as e:
        print("Error reading image file:", e)
        return None


def image_to_video(image, output_video_path, duration_seconds):
    # Convert PIL image to NumPy array
    try:
        image_np = np.array(image)
    except Exception as e:
        print("Error converting image to NumPy array:", e)
        return None

    # Check if image_np is empty or has no shape information
    if len(image_np.shape) != 3 or image_np.shape[0] == 0 or image_np.shape[1] == 0:
        print(image_np)
        print("Invalid image dimensions")
        return None

    # Get the dimensions of the image
    height, width, channels = image_np.shape

    if os.path.isdir(output_video_path):
        output_video_name = os.path.join(output_video_path, "output_video.mp4")
    else:
        output_video_name = output_video_path

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_video_name, fourcc, duration_seconds, (width, height))

    if not out.isOpened():
        print("Error opening VideoWriter")
        return None

    for _ in range(int(duration_seconds * duration_seconds)):
        out.write(image_np)

    out.release()

    if os.path.exists(output_video_name):
        return output_video_name
    else:
        print("Error creating video file")
        return None

def save_uploaded_file(uploaded_file):
    if uploaded_file is not None:
        # Create a directory to store uploaded files if it doesn't exist
        os.makedirs('uploads', exist_ok=True)
        # Save the file to the uploads directory
        with open(os.path.join("uploads", uploaded_file.name), "wb") as f:
            f.write(uploaded_file.getbuffer())
        return os.path.join("uploads", uploaded_file.name)
    return None
