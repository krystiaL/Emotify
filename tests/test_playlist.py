from face_detect_module.face_emotion_detector import extract_emotion
from playlist_module.generate_playlist import process_emotion, tailor_df, generate_playlist, send_playlist_id
import os

if __name__ == "__main__":
    input_file = "interface/vid_recs/output_video.mp4"

    emotion = extract_emotion(input_file=input_file)
    print(emotion)

    emotion_out = process_emotion(emotion=emotion)
    #variable storing the dominant emotion of the file;
    print(emotion_out)

    emotion_df = tailor_df(emotion_out)
    #variable storing the created emotion dataframe;
    print(emotion_df)

    account_name = os.environ.get("ACCOUNT_NAME")
    playlist = generate_playlist(emotion_df=emotion_df, account_name=account_name)
    #variable storing the generated playlist;

    playlist_url = send_playlist_id(generated_playlist=playlist, account_name=account_name)
    #variable storing the playlist url from spotify api to be embedded in webpage
    print(playlist_url)
