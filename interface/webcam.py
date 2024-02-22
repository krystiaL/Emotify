import cv2

class WebcamRecorder:
    def __init__(self):
        self.recording = False
        self.frames = []
        self.output_file = "recorded_video.avi"
        self.out = None

    def start_recording(self):
        self.recording = True
        self.frames = []
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        self.out = cv2.VideoWriter(self.output_file, fourcc, 20.0, (640, 480))

    def stop_recording(self):
        self.recording = False
        if self.out is not None:
            self.out.release()

    def record(self, frame):
        if self.recording:
            self.frames.append(frame)
            self.out.write(cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
