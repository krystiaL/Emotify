import streamlit as st
import av
import numpy as np
import threading

from streamlit_webrtc import VideoTransformerBase, webrtc_streamer

class VideoTransformer(VideoTransformerBase):
    def __init__(self):
        self.recording = False
        self.start_button_pressed = st.button("🟢 Start Face Recording",
                                              use_container_width=True,
                                              on_click=self.record)
        self.stop_button_pressed = st.button("🔴 Stop Face Recording",
                                             use_container_width=True,
                                             on_click=self.stop)
        self.output_file_name = None
        self.frames = []

    def transform(self, frame: av.VideoFrame) -> np.ndarray:
        if self.recording:
            self.frames.append(frame.to_ndarray(format="bgr24"))
        return frame.to_ndarray(format="bgr24")

    def start_recording(self):
        self.recording = True


    def stop_recording(self):
        self.recording = False
        self.frames = []


def main():
    st.write("## Webcam Recording")
    ctx = webrtc_streamer(key="recorder", video_transformer_factory=VideoTransformer)

    if ctx.video_transformer:
        video_transformer = ctx.video_transformer

        if st.button("Start Recording"):
            video_transformer.start_recording()

        if st.button("Stop Recording"):
            video_transformer.stop_recording()

        if video_transformer.frames:
            st.write("## Recorded Frames")
            for i, frame in enumerate(video_transformer.frames):
                st.write(f"Frame {i}")
                st.image(frame, channels="BGR")


    def record(self):
        self.record_button_pressed = True
        self.start()

    def on_new_sample(self, appsink):
        sample = appsink.emit("pull-sample")
        buf = sample.get_buffer()
        caps = sample.get_caps()
        width = caps.get_structure(0).get_value("width")
        height = caps.get_structure(0).get_value("height")
        numpy_array = np.ndarray(
            (height, width, 3),
            buffer=buf.extract_dup

if __name__ == "__main__":
    main()
