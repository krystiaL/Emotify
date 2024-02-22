import streamlit as st
import cv2

class WebcamRecorder:
    def __init__(self, output_file):
        self.recording = False
        self.frames = []
        self.output_file = output_file
        self.frame_width = 640
        self.frame_height = 480
        self.fourcc = cv2.VideoWriter_fourcc(*'XVID')
        self.out = None

    def start_recording(self):
        self.recording = True
        self.frames = []
        self.out = cv2.VideoWriter(self.output_file, self.fourcc, 20.0, (self.frame_width, self.frame_height))

    def stop_recording(self):
        self.recording = False
        if self.out is not None:
            self.out.release()
            self.out = None

    def record(self, frame):
        if self.recording:
            self.frames.append(frame)
            if self.out is not None:
                self.out.write(frame)
