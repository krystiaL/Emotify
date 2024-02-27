#---------------------------------------------------
#          LIBRARY AND MODULE IMPORTS
#---------------------------------------------------
import streamlit as st
# import numpy as np

import time
import os
# import base64
# import tempfile

from streamlit_webrtc import webrtc_streamer

import instructions
import regarding_spotify_interact
import about_us

from webcam import WebcamRecorder

from face_detect_module.face_emotion_detector import extract_emotion

from playlist_module.generate_playlist import process_emotion, tailor_df
from playlist_module.generate_playlist import generate_playlist, send_playlist_id

from alternative_input_preproc import is_image, image_to_video

#---------------------------------------------------
#          PATHS AND OTHER VARIABLES
#---------------------------------------------------
#not too sure about this

# Get the path of the downloads folder
# downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")

# # # Set the downloads_path as an environment variable
# # os.environ["DOWNLOADS_PATH"] = downloads_path

# temp_file = tempfile.NamedTemporaryFile()
# downloads_path = temp_file.name

output_video_path = "/root/code/Atsuto-T/Music_Selector_Project/interface/vid_recs"
duration = 10

#---------------------------------------------------
#            PLAYLIST GENERATION FUNCTION
#---------------------------------------------------

def gen_playlist_ui(mood_dict):
    #This function takes the extracted emotion dictionary and uses the generate_playlist
    #module for the playlist generation process of the application

    #------------emotions-------------------
    user_emotion = {
        'mood_Calm': "Serene",
        'mood_Energetic': "Dynamic",
        'mood_Happy': "Blissful",
        'mood_Sad': "Melancholic"
        }
#-------------------------------------------
    emotion_out = process_emotion(mood_dict)
    #variable storing the dominant emotion of the file;

    emotion_df = tailor_df(emotion_out)
    #variable storing the created emotion dataframe;

    account_name = "emo_play"

    playlist = generate_playlist(emotion_df=emotion_df, account_name=account_name)
    #variable storing the generated playlist;

    playlist_url = send_playlist_id(generated_playlist=playlist, account_name=account_name)
    #variable storing the playlist url from spotify api to be embedded in webpage

    dominant_emotion = playlist[3]
    emotion_title = user_emotion.get(dominant_emotion, "Unknown Emotion")
    st.subheader(f"Here's a {emotion_title} playlist for you!")
    #to do: change identified emotion to emotion returned from emotion_detect function

    #embedd to spotify interface; to do: check if there are other ways to do this
    st.write("Add this playlist to your Spotify library!")

    st.markdown(f'<iframe src={playlist_url} width="500" height="400"></iframe>',
    unsafe_allow_html=True)

    st.write(" ")

    #reset button for re-generation
    if 'reset_button' not in st.session_state:
        st.session_state['reset_button'] = False

    if st.button('Re-generate Playlist', key='reset'):
        reset_app()

#---------------------------------------------------
#               APP RESET FUNCTION
#---------------------------------------------------

def reset_app():
    # Clear Streamlit cache
    st.session_state.clear()

    # Remove the saved file
    if os.path.exists(output_video_path):
        for file in os.listdir(output_video_path):
            file_path = os.path.join(output_video_path, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
        st.write("Successful Session Restart")
    else:
        st.write("Session Not Restarted")

#---------------------------------------------------
#          PAGE CONFIGURATIONS ETC.
#---------------------------------------------------

st.set_page_config(page_title="<Music Selector Name>", page_icon=":musical_note:", layout="wide")

#----------------------------------
#       SIDEBAR
#----------------------------------

with st.sidebar:
    st.title("About <Music Selector>") #change to official name
    st.image("interface/images/Music-cuate.png")
    #attribute: <a href="https://storyset.com/app">App illustrations by Storyset</a>

    st.subheader("For questions about application usage:")
    page = st.selectbox("choose a query", ["How to generate your playlist?",
                                                  "How to add playlist to your Spotify library?",
                                                 ])
    #drop down option for Q&As

    if page == "How to generate your playlist?":
        instructions.instructions_page()
    if page == "How to add playlist to your Spotify library?":
        regarding_spotify_interact.spotify_page()
    #link selectbox to indiv .py file (==individual page)
    st.subheader("Know more about the creators:")
    about_us_page = st.button("About Us")
    #link page button to the individual .py file (==individual page)
    if about_us_page:
        about_us.about_us()

#------------------------------------
#      HEADER AND DESCRIPTION
#------------------------------------
#custom title page using html for bigger font size
st.markdown("""
<h1 style="font-size: 80px; color: #E9FBFF; text-align: center; font-family: Trebuchet MS">
Music Selector Project &#9835
</h1>
""", unsafe_allow_html=True) #official name still hasn't been decided

st.write(" ")
st.markdown("""
    <h1 style="font-size: 40px; text-align: center">
    🤗😭😌🤩  ➫  💽
    </h1>
    """, unsafe_allow_html=True)
    # st.title("🤗😭😌🤩  ➫  💽🎧")
st.markdown("""
    <h1 style="font-size: 30px; text-align: center; color: #faaa0b; font-family: Trebuchet MS">
    Tune in your Emotions, Transform out your Playlist!
    </h1>
    """, unsafe_allow_html=True)
st.subheader(" ")

#--------------------------------------------------------------
#    CREATE TABS SEPARATING IMAGE AND VIDEO INPUT INTERFACE
#--------------------------------------------------------------

image_tab, video_tab = st.tabs(["📸 Face Capture", "🎥 Face Recording"])

#--------------------##----------------------
#    SPLIT TAB LAYOUT FOR CAMERA CAPTURE
#--------------------------------------------

col1, col2,  col3 = image_tab.columns([2.8, 0.3, 3])
col1.write(" ") #line break

#--------------------------------------------
#       IMAGE TAB, COLUMN 1 ELEMENTS
#--------------------------------------------

with col1:

    st.subheader("Take a selfie!")
    #user input panel subheader

    #--------------Camera Image---------------#
    with st.form("image_input"):
        #form submission for image input

        image_captured = st.camera_input("Take a picture of your face showing your current emotion")
        # camera widget; will return a jpeg file once image is taken.
        # st.session_state["image_captured"] = None
        # # Initialized camera state variable

        uploaded_image = st.file_uploader("or upload an image of your face:", type=["png", "jpeg", "jpg"])
        #image_upload function using file_uploader widget
        # st.session_state["uploaded_image"] = None
        # # Initialized file uploader state variable

        submit_button = st.form_submit_button("Generate Playlist", args=[image_captured, uploaded_image])
        #submit button as entry for file extraction to image/video model pipe

        #to do: add a buttton to clear all images

    if submit_button:
        if image_captured:
            # st.session_state["image_captured"] = image_captured
            st.write("Reading emotion from selfie...")

        elif uploaded_image:
            # st.session_state["uploaded_image"] = uploaded_image
            st.write("Reading emotion from uploaded image file...")

        else:
            st.write("No input detected 😵")
            st.write("Please choose one of the designated image extraction methods above (📸 or 📥). ")
            #default message when submit button was pressed but no file was fed.

col1.caption("Application Accuracy: <80.56%>")
#to do: change metric to appropriate score result

#--------------------------------------------
#       IMAGE TAB, COLUMN 3 ELEMENTS
#--------------------------------------------
with col3:
    st.subheader(" ")
# Display generated playlist
    if image_captured or uploaded_image:
        # Assuming some functions like image_to_video and extract_emotion exist
        user_image = image_captured if image_captured else uploaded_image
        #transform jpeg file into byte file
        byte_image = is_image(user_image)
        #entry point for model input;
        input_file = image_to_video(image=byte_image,
                                    output_video_path=output_video_path,
                                    duration_seconds=duration)

        if input_file:
            st.subheader(" ")
            st.write("Image converted into video file...")
            time.sleep(2)
            emotion = extract_emotion(input_file=input_file)

            if emotion:
                emo_key = next(iter(emotion[0]))
                st.write(f"Emotion Extracted: {emo_key}")

            #playlist generation function
            with st.spinner("Transforming Emotions into Melodies..."):
                # to improve: change into progress bar/ specify state after merging other functions
                time.sleep(3)  # simulate playlist generation time
                gen_playlist_ui(emotion)


    else:
        st.subheader(" ")
        st.image("interface/images/Playlist-amico (1).png")
        #image attribute: <a href="https://storyset.com/app">App illustrations by Storyset</a>

        st.markdown("""
        <h1 style="font-size: 20px; text-align: center; color: #faaa0b">
        Just chillin' for now...
        </h1>
        """, unsafe_allow_html=True)


#--------------------##----------------------
#    SPLIT TAB LAYOUT FOR VIDEO RECORDING
#--------------------------------------------

col1_vid, col2_vid, col3_vid = video_tab.columns([2.8, 0.3, 3])
col1.write(" ") #line break

#-------------------##-----------------------
#       VIDEO TAB, COLUMN 1 ELEMENTS
#--------------------------------------------
with col1_vid:

    st.subheader("Take a face recording!")
    #user input panel subheader

    #------------Camera Recoding-------------#
    st.caption("Record a short video of your face showing your current emotion")

    # output_file_name = "recorded_video.avi"
    # # Define the output file name; modify to accomodate emotion playlist name
    recorder = WebcamRecorder()

    st.write("## Webcam Recording with WebRTC")

    ctx = webrtc_streamer(key="example")

    #create start and stop buttons in seprate colums
    start = st.button('🟢 Start Face Recording',
                                   use_container_width=True)
    stop = st.button('🔴 Stop Face Recording',
                                  use_container_width=True)

    #progress bar to show start and stop of video recording
    progress_bar = st.progress(0)

    #--------------------------------------#
    #           RECORDING LOOP
    #--------------------------------------#
    if ctx.video_transformer:
        video_transformer = ctx.video_transformer

    if start:
        recorder.start_recording()

    if stop:
        recorder.stop_recording()

    if recorder.frames:
        st.write("## Recorded Frames")
        for i, frame in enumerate(recorder.frames):
            st.write(f"Frame {i}")
            st.image(frame, channels="BGR")

    #------------video file submission-------------#
    with st.form("video_input"):
        uploaded_video = st.file_uploader("Choose a video:", type=["mp4", "avi"])
        st.session_state["uploaded_video"] = None

        submit_button = st.form_submit_button("Generate Playlist", args=[uploaded_video])
        #submit button as entry for file extraction to image/video model pipe
        #to do: figure out the return file for webcam face recording function
        if submit_button:
            # if webcam:
            #     st.write("Reading emotion from face recording...")

            if uploaded_video:
                st.write("Reading emotion from video file...")
                st.session_state["uploaded_video"] = uploaded_video

#--------------------------------------------
#       VIDEO TAB, COLUMN 3 ELEMENTS
#--------------------------------------------
# Display generated playlist
with col3_vid:
    st.write(" ")
    if st.session_state.get("recorder"):
        st.session_state.recorder = recorder
        st.write("Emotion Extracted...")
        #playlist generation for camera capture
        with st.spinner("Transforming Emotions into Melodies..."):
            # to improve: change into progress bar/ specify state after merging other functions
            time.sleep(5)  # simulate playlist generation time
        # gen_playlist_ui()

    elif st.session_state.get("uploaded_video"):
        uploaded_video = st.session_state["uploaded_video"]
        st.write("Emotion Extracted...")
        with st.spinner("Transforming Emotions into Melodies..."):
            time.sleep(5)  # simulate playlist generation time
        # gen_playlist_ui()

    else:
        st.subheader(" ")
        col3_vid.image("interface/images/Playlist-amico (1).png")
        #image attribute: <a href="https://storyset.com/app">App illustrations by Storyset</a>

        col3_vid.markdown("""
        <h1 style="font-size: 20px; text-align: center; color: #faaa0b">
        Just chillin' for now...
        </h1>
        """, unsafe_allow_html=True)


############################################
#------------------------------------------#
############################################

# #video stuff
# st.title("Play Uploaded File")

# uploaded_file = st.file_uploader("Choose a video...", type=["mp4"])
# temporary_location = False

# if uploaded_file is not None:
#     temporary_location = write_to_disk(uploaded_file)

# if temporary_location:
#     video_stream = cv2.VideoCapture(temporary_location)
#     # Check if camera opened successfully
#     if (video_stream.isOpened() == False):
#         print("Error opening video  file")
#     else:
#         # Read until video is completed
#         while (video_stream.isOpened()):
#             # Capture frame-by-frame
#             ret, image = video_stream.read()
#             if ret:
#                 # Display the resulting frame
#                 st.image(image, channels="BGR", use_column_width=True)
#             else:
#                 break
#         video_stream.release()
#         cv2.destroyAllWindows()

# def write_to_disk(uploaded_file):
#     """Writes an uploaded video file to disk and returns the file path."""
#     with tempfile.NamedTemporaryFile(delete=False) as out:
#         out.write(uploaded_file.read())
#         return out.name
