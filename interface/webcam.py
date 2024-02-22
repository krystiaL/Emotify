import streamlit as st
import cv2
from threading import Thread

class WebcamRecorder:
    def __init__(self):
        self.recording = False
        self.frames = []

    def start_recording(self):
        self.recording = True
        self.frames = []

    def stop_recording(self):
        self.recording = False

    def record(self):
        cap = cv2.VideoCapture(0)
        while self.recording:
            ret, frame = cap.read()
            if not ret:
                st.write("Error: Unable to capture frame")
                break
            self.frames.append(frame)
            # Display the frame (optional)
            cv2.imshow('Webcam Recording', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()

class webcam_thread:
    global frame
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
