from face_detect_module.face_emotion_detector import extract_emotion

if __name__ == "__main__":
    input_file = "interface/vid_recs/output_video.mp4"

    emotion = extract_emotion(input_file=input_file)

    emotion
