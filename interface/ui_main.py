#---------------------------------------------------
#          LIBRARY AND MODULE IMPORTS
#---------------------------------------------------
import streamlit as st
# import numpy as np

import time
# import base64
# import os
# import tempfile

from streamlit_webrtc import webrtc_streamer

import instructions
import regarding_spotify_interact
import about_us

from webcam import WebcamRecorder

from face_detect_module.face_emotion_detector import extract_emotion
# from playlist_module.generate_playlist import send_playlist_id
# from playlist_module.generate_playlist import process_emotion, tailor_df
# from playlist_module.generate_playlist import generate_playlist, send_playlist_id

from alternative_input_preproc import is_image, process_media_file, image_to_video
#---------------------------------------------------
#           PLAYLIST ELEMENT
#---------------------------------------------------

moods = {"Emotion": {'Sadness': [0.2,1],
                    'Surprise': [0.19, 0.2, 0.21, 0.21, 0.2, 0.21, 0.24, 0.23, 0.24, 0.24, 0.24, 0.25, 0.24, 0.22, 0.2,\
                        0.24, 0.26, 0.29, 0.27, 0.27, 0.27, 0.25, 0.28, 0.32, 0.36, 0.4, 0.43, 0.44, 0.45, 0.43, 0.42, 0.38, 0.34, 0.31, 0.27, 0.24, 0.23, 0.23],
                    'Anger': [0.21,1,1,1,1],
                    'Neutral': [0.19,1,1,1,1,1,1,1,1,1,1,1,1]}
    }

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
#             PLAYLIST FUNCTIONS
#---------------------------------------------------

def gen_playlist_ui(mood_dict):
    #This function takes the extracted emotion dictionary and uses the generate_playlist
    #module for the playlist generation process of the application

    st.subheader(f"Here's a <identified emotion> playlist for you!")
    #to do: change identified emotion to emotion returned from emotion_detect function

    #embedd to spotify interface; to do: check if there are other ways to do this
    st.write("Add this playlist to your Spotify library!")

    # emotion_out = process_emotion(mood_dict)
    # #variable storing the dominant emotion of the file;
    # st.write(emotion_out)

    # emotion_df = tailor_df(emotion_out)
    # #variable storing the created emotion dataframe;
    # st.write(emotion_df)

    # playlist = generate_playlist(emotion_df=emotion_df, account_name="test")
    # #variable storing the generated playlist;

    # playlist_url = send_playlist_id(generated_playlist=playlist, account_name='test')
    # #variable storing the playlist url from spotify api to be embedded in webpage
    # st.write(playlist_url)

    st.markdown('<iframe src="https://open.spotify.com/embed/playlist/0HI7czcgdxj4bPu3eRlc2C?utm_source=generator"\
    width="500" height="400"></iframe>',
    unsafe_allow_html=True)




#------------------------------------
#      HEADER AND DESCRIPTION
#------------------------------------
#custom title page using html for bigger font size
st.markdown("""
<h1 style="font-size: 80px; color: #E9FBFF; text-align: center">
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
    <h1 style="font-size: 30px; text-align: center; color: #faaa0b">
    Tune in your Emotions, Transform out your Playlist!
    </h1>
    """, unsafe_allow_html=True)
st.subheader(" ")

#--------------------------------------------------------------
#    CREATE TABS SEPARATING IMAGE AND VIDEO INPUT INTERFACE
#--------------------------------------------------------------

image_tab, video_tab, text_tab = st.tabs(["📸 Face Capture", "🎥 Face Recording", "Text Tab"])

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
# Display generated playlist
    if image_captured or uploaded_image:
        # Assuming some functions like image_to_video and extract_emotion exist
        user_image = image_captured if image_captured else uploaded_image
        st.image(user_image)
        byte_image = is_image(user_image)
        #entry point for model input;
        input_file = image_to_video(image=byte_image,
                                    output_video_path=output_video_path,
                                    duration_seconds=duration)

        st.write(input_file)

        # video_file = process_media_file(input_file=input_file,
        #                                 output_directory=output_video_path,
        #                                 duration_seconds=duration)

        if input_file:
            st.write("image converted into video file...")
            time.sleep(2)
            # emotion = extract_emotion(input_file=input_file)

            # if emotion:
            #     st.write("Emotion Extracted...")

            #playlist generation for camera capture
            with st.spinner("Transforming Emotions into Melodies..."):
                # to improve: change into progress bar/ specify state after merging other functions
                time.sleep(3)  # simulate playlist generation time
                # gen_playlist_ui()

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

#--------------------##----------------------
#    SPLIT TAB LAYOUT FOR DROP DOWN
#--------------------------------------------

col1_text, col2_text, col3_text = text_tab.columns([2.8, 0.3, 3])
col1.write(" ") #line break


#--------------------------------------------
#   DUMMY TAB FOR MODULE CONNECTION CHECK
#--------------------------------------------
with col1_text:
    # text input form
    st.subheader("Select your current mood")
    with st.form("text_input"):
        mood = st.selectbox("Choose an emotion:", list(moods.keys()))
        st.session_state["mood"] = None
        submit_button= st.form_submit_button("Submit Emotion")
        if submit_button:
            st.write("Emotion selected")
            st.session_state["mood"] = moods["Emotion"]



# Display generated playlist
with col3_text:
    st.write(" ")
    if st.session_state.get("mood"):
        st.session_state["mood"] = mood
        mood_dict = moods["Emotion"]
        st.write(f"Selected emotion: {mood}")
        with st.spinner("Transforming Emotions into Melodies..."):
            time.sleep(5)  # simulate playlist generation time
        # gen_playlist_ui(mood_dict=mood_dict) #playlist generation



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
