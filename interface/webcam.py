import cv2
import os
import streamlit as st
import numpy as np

class VideoRecorder:
    def __init__(self):
        self.recording = False
        self.frame_count = 0
        self.frames = []
        self.path = st.secrets['VIDEO_PATH']

    def recv(self, frame):
        if self.recording:
            self.frames.append(frame.to_ndarray(format="bgr24"))
            self.frame_count += 1

            # Update the progress bar
            st.progress_bar.progress(self.frame_count / 30)

        return frame

    def start_recording(self):
        self.recording = True
        self.frame_count = 0
        self.frames = []

    def stop_recording(self):
        self.recording = False
        if self.frame_count > 0:
            # Define the frame variable
            frame = self.frames[0]

            # Get the width and height of the frame
            width, height = frame.shape[:2]

            if os.path.isdir(self.path):
                output_video_name = os.path.join(self.path, "recorded_vid_stream.mp4")
            else:
                output_video_name = self.path

            # Save the recorded frames to a video file using OpenCV
            fourcc = cv2.VideoWriter_fourcc(*"mp4v")
            out = cv2.VideoWriter(output_video_name, fourcc, 30, (width, height))
            video_frames = self.frames
            for frame in video_frames:
                out.write(frame)
            out.release()

            # Get the video file path
            video_file_path = os.path.abspath("recorded_vid_stream.mp4")

            # Reset the frames list
            self.frames = []

            return video_file_path
