#---------------------------------------------------
#          LIBRARY AND MODULE IMPORTS
#---------------------------------------------------
import streamlit as st
# import threading
import time
import os
from PIL import Image
import base64
# import tempfile

# from streamlit_webrtc import webrtc_streamer, WebRtcMode, WebRtcStreamerContext

from interface import instructions
from interface import regarding_spotify_interact
from interface import about_us

# from webcam import VideoRecorder

from face_detect_module.face_emotion_detector_DIY import extract_emotion

from playlist_module.generate_playlist import process_emotion, tailor_df
from playlist_module.generate_playlist import generate_playlist, send_playlist_id

from interface.alternative_input_preproc import is_image, image_to_video, save_uploaded_file

#---------------------------------------------------
#          PATHS AND OTHER VARIABLES
#---------------------------------------------------

# Get the path of the downloads folder
# downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")

# # # Set the downloads_path as an environment variable
# # os.environ["DOWNLOADS_PATH"] = downloads_path

# temp_file = tempfile.NamedTemporaryFile()
# downloads_path = temp_file.name

#OUTPUT_VIDEO_PATH = os.environ.get("VIDEO_PATH")
OUTPUT_VIDEO_PATH = st.secret['VIDEO_PATH']
duration = 10

# lock = threading.Lock()
# img_container = {"img": None}

# MEDIA_STREAM_CONSTRAINTS = {
#     "video": True,  # Capture video
#     "audio": False,  # Disable audio
# }

emotion_emoji = {
    'Neutral': "https://giphy.com/embed/WtUJnCSEWWCAdHb90r/giphy.gif",
    'Happiness': "https://media.giphy.com/media/DIgT73ICZOOZqNCNs7/giphy.gif",
    'Sadness': "https://giphy.com/embed/jTwn7gnUDBLf84cKdn/giphy.gif",
    'Surprise': "https://giphy.com/embed/JIFYGMimGZhbxMh6J5/giphy.gif",
    'Fear': "https://giphy.com/embed/cURhR2qbi437KbcuuP/giphy.gif",
    'Disgust': "https://giphy.com/embed/0xslhbGyYaBudd8Ke9/giphy.gif",
    'Anger': "https://giphy.com/embed/On3RvLqXiRIxW/giphy.gif"
    }

#---------------------------------------------------
#gif embedding:

#Neutral: <iframe src="https://giphy.com/embed/WtUJnCSEWWCAdHb90r" width="480" height="480" frameBorder="0" class="giphy-embed" allowFullScreen></iframe><p><a href="https://giphy.com/gifs/SportsManias-emoji-sportsmanias-animated-emojis-WtUJnCSEWWCAdHb90r">via GIPHY</a></p>
#Happy: <iframe src="https://giphy.com/embed/DIgT73ICZOOZqNCNs7" width="480" height="480" frameBorder="0" class="giphy-embed" allowFullScreen></iframe><p><a href="https://giphy.com/gifs/smile-smiling-smiley-DIgT73ICZOOZqNCNs7">via GIPHY</a></p>
#Sadness: <iframe src="https://giphy.com/embed/jTwn7gnUDBLf84cKdn" width="480" height="480" frameBorder="0" class="giphy-embed" allowFullScreen></iframe><p><a href="https://giphy.com/gifs/sad-face-cute-grumpy-jTwn7gnUDBLf84cKdn">via GIPHY</a></p>
#Surprise: <iframe src="https://giphy.com/embed/JIFYGMimGZhbxMh6J5" width="480" height="480" frameBorder="0" class="giphy-embed" allowFullScreen></iframe><p><a href="https://giphy.com/gifs/SAZKA-loterie-lotery-sportkamicek-JIFYGMimGZhbxMh6J5">via GIPHY</a></p>
#Fear: <iframe src="https://giphy.com/embed/cURhR2qbi437KbcuuP" width="480" height="480" frameBorder="0" class="giphy-embed" allowFullScreen></iframe><p><a href="https://giphy.com/gifs/smiley-peur-cURhR2qbi437KbcuuP">via GIPHY</a></p>
#Disgust: <iframe src="https://giphy.com/embed/0xslhbGyYaBudd8Ke9" width="480" height="480" frameBorder="0" class="giphy-embed" allowFullScreen></iframe><p><a href="https://giphy.com/gifs/vomit-barf-spew-0xslhbGyYaBudd8Ke9">via GIPHY</a></p>
#Anger: <iframe src="https://giphy.com/embed/On3RvLqXiRIxW" width="480" height="480" frameBorder="0" class="giphy-embed" allowFullScreen></iframe><p><a href="https://giphy.com/gifs/fire-mad-anger-On3RvLqXiRIxW">via GIPHY</a></p>

#---------------------------------------------------
#            PLAYLIST GENERATION FUNCTION
#---------------------------------------------------

def gen_playlist_ui(mood_dict):
    #This function takes the extracted emotion dictionary and uses the generate_playlist
    #module for the playlist generation process of the application

    emotion_out = process_emotion(mood_dict)
    #variable storing the dominant emotion of the file;

    emotion_df = tailor_df(emotion_out)
    #variable storing the created emotion dataframe;

    account_name = "emo_play"

    playlist = generate_playlist(emotion_df=emotion_df, account_name=account_name)
    #variable storing the generated playlist;

    playlist_url = send_playlist_id(generated_playlist=playlist, account_name=account_name)
    #variable storing the playlist url from spotify api to be embedded in webpage

    return playlist, playlist_url

def show_playlist(playlist_url):
    #shows the embedded playlist preview from spotify
#-------------------------------------------
    st.subheader(f"Here's your playlist!")
    #to do: change identified emotion to emotion returned from emotion_detect function

    #embedd to spotify interface; to do: check if there are other ways to do this
    st.write("Click \"...\" to redirect to your Spotify library!")

    # Create HTML to display the iframe with centered alignment
    embedd_playlist = f'''
    <div style="display: flex; justify-content: center;">
        <iframe src="{playlist_url}" width="850" height="400"></iframe>
    </div>
    '''

    # Display the HTML using st.markdown()
    st.markdown(embedd_playlist, unsafe_allow_html=True)

    st.write(" ")

    # col_regen, col_blank1, col_reset = st.columns([2,1,3])

    # with col_regen:
    #     #regenerate playlist using the same image
    #     if st.button("🔂 Regenerate Playlist",
    #                  key="regenerate",
    #                  use_container_width=True):
    #         regen_playlist()

    # with col_reset:
    #     #reset entire playlist generation process
    #     if st.button('⌛ Reset Entire Generation Process',
    #                  key='reset',
    #                  use_container_width=True):
    #         # revert session state variables to none
    #         st.session_state["playlist"] = None
    #         st.session_state["playlist_url"] = None
    #         st.session_state["emotion"] = None
    #         st.session_state["input_file"] = None
    #         st.session_state["byte_image"] = None
    #         reset_app()
    #         clear_vidrec_folder()
        #---------------------------------------------------
#           APP RESET AND REGEN FUNCTIONS
#---------------------------------------------------

# def regen_playlist():
#     # Clear Streamlit cache
#     st.session_state.clear()
#     st.write("generated a new playlist")

def reset_img():
    # Reset uploaded image
    st.session_state["image_captured"] = None
    st.session_state["uploaded_image"] = None

    # Remove the saved image and media files
    clear_uploads_folder()
    clear_vidrec_folder()

    #clear all session states
    st.session_state.clear()

    # Execute JavaScript to reload the page
    st.write(
        "<script>window.location.reload(true);</script>",
        unsafe_allow_html=True
    )


def clear_vidrec_folder():
    #check of the vid_recs folder exist
    if os.path.exists(OUTPUT_VIDEO_PATH):
        # Iterate over stored file/s and remove it
        for file in os.listdir(OUTPUT_VIDEO_PATH):
            file_path = os.path.join(OUTPUT_VIDEO_PATH, file)
            if os.path.isfile(file_path):
                os.remove(file_path)

def clear_uploads_folder():
    # Check if the uploads folder exists
    if os.path.exists("uploads"):
        # Get a list of all files in the uploads folder
        files = os.listdir("uploads")
        # Iterate over each file and remove it
        for file in files:
            file_path = os.path.join("uploads", file)
            os.remove(file_path)
        # Optionally, remove the uploads folder itself
        os.rmdir("uploads")

def reset_app():
    # clear image uploaded/taken and reset session states
    reset_img()

    #clear all session states
    st.session_state.clear()

    # Reload the entire page
    st.experimental_rerun()

#---------------------------------------------------
#           CAMERA CAPTURE FUNCTIONS
#---------------------------------------------------
#function to flip the camera image
# def flip_image(image):
#     return image.rotate(180)


#---------------------------------------------------
#           VIDEO RECORDING FUNCTIONS
#---------------------------------------------------
# def video_frame_callback(frame):
#     img = frame.to_ndarray(format="bgr24")
#     with lock:
#         img_container["img"] = img

#     return frame

#---------------------------------------------------
#           FORM SUBMIT FUNCTIONS
#---------------------------------------------------

def reset_img_form(image_captured, uploaded_image):
    reset_img()

#---------------------------------------------------
#          PAGE CONFIGURATIONS ETC.
#---------------------------------------------------

#this is seen in the tab bar of the webpage
st.set_page_config(page_title="<Music Selector Name>", page_icon=":musical_note:", layout="wide")

#----------------------------------
#       SIDEBAR
#----------------------------------

with st.sidebar:
    st.title("About <Music Selector>") #change to official name
    st.image("interface/images/Music-cuate.png")
    #attribute: <a href="https://storyset.com/app">App illustrations by Storyset</a>

    st.subheader("For questions about application usage:")
    page = st.selectbox("choose a query", ["How to use this application?",
                                            "Is the playlist saved immediately in Spotify library?",
                                                 ])
    #drop down option for Q&As

    if page == "How to use this application?":
        instructions.instructions_page()
    if page == "How to add playlist to your Spotify library?":
        regarding_spotify_interact.spotify_page()
    #link selectbox to indiv .py file (==individual page)
    st.subheader("Know more about the creators:")
    about_us_page = st.button("About Us", use_container_width=True)
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

# image_tab, video_tab = st.tabs(["📸 Face Capture", "🎥 Face Recording"])

#--------------------##----------------------
#    SPLIT TAB LAYOUT FOR CAMERA CAPTURE
#--------------------------------------------

col1, col2,  col3 = st.columns([2.8, 0.3, 3])
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
        st.session_state["image_captured"] = None

        uploaded_image = st.file_uploader("or upload an image of your face:", type=["png", "jpeg", "jpg"])
        #image_upload function using file_uploader widget
        st.session_state["upload_image"] = None

        col_submit, col_blank, col_reset_img = st.columns([2, 2, 1.2])

        submit_button = col_submit.form_submit_button("▶ Generate Playlist",
                                                      args=[image_captured, uploaded_image],
                                                      )
        #submit button as entry for file extraction to image/video model pipe

        reset_button = col_reset_img.form_submit_button("↺ Reset",
                                                        args=[image_captured, uploaded_image],
                                                        on_click=reset_img_form,
                                                        use_container_width=True
                                                        )
        #buttton to clear all images

    if submit_button:
        if image_captured:
            # st.session_state["image_captured"] = image_captured
            st.write("Reading emotion from selfie...")

        elif uploaded_image:
            uploaded_file = save_uploaded_file(uploaded_image)
            st.write("Reading emotion from uploaded image file...")

        else:
            st.write("No input detected 😵")
            st.write("Please choose one of the designated image extraction methods above (📸 or 📥). ")
            #default message when submit button was pressed but no file was fed.

    if reset_button:
            st.write("✅ Reset image objects successful")
            st.write("Take a photo 📸 or upload an image 📥 and click \" ▶️ Generate Playlist \".")


col1.caption("Application Accuracy: <80.56%>")
#to do: change metric to appropriate score result

#--------------------------------------------
#       IMAGE TAB, COLUMN 3 ELEMENTS
#--------------------------------------------
with col3:
    st.subheader(" ")
# Display generated playlist
    # if submit_button is True:
    if image_captured or uploaded_image:
        user_image = image_captured if image_captured else uploaded_image

        #transform jpeg file into byte file
        byte_image = is_image(user_image)
        #entry point for model input;
        input_file = image_to_video(image=byte_image,
                                    output_video_path=OUTPUT_VIDEO_PATH,
                                    duration_seconds=duration)

        if input_file:
            st.subheader(" ")
            with st.spinner("Extracting emotion from image..."):
                time.sleep(2)
                emotion = extract_emotion(input_file=input_file)

            if emotion:
                emo_key = next(iter(emotion[0]))
                for gif in emotion_emoji:
                    if emo_key == gif:
                        st.markdown(f"""
                        <h1 style="font-size: 30px; text-align: center; color: #faaa0b; font-family: Trebuchet MS">
                        Emotion Extracted: {emo_key}
                        </h1>
                        """, unsafe_allow_html=True)
                        st.write(" ")

                        img_col, emo_col = col3.columns(2)

                        show_gif = emo_col.container(height=250, border=True)
                        show_gif.markdown(f"""
                        <div style="display: flex; justify-content: center;">
                            <img src="{emotion_emoji[gif]}" alt="GIF" style="width: 55%;">
                        </div>
                        """, unsafe_allow_html=True)
                        show_img = img_col.container(border=True)
                        show_img.image(user_image)



            #playlist generation function
                st.subheader(" ")
                with st.spinner("Transforming Emotions into Melodies..."):
                    # to improve: change into progress bar/ specify state after merging other functions
                    time.sleep(1)  # simulate playlist generation time
                    playlist, playlist_url = gen_playlist_ui(emotion)
                    show_playlist(playlist_url=playlist_url)


    else:
        st.subheader(" ")
        st.image("interface/images/Playlist-amico (1).png")
        #image attribute: <a href="https://storyset.com/app">App illustrations by Storyset</a>

        st.markdown("""
        <h1 style="font-size: 20px; text-align: center; color: #faaa0b">
        Just chillin' for now...
        </h1>
        """, unsafe_allow_html=True)


# #--------------------##----------------------
# #    SPLIT TAB LAYOUT FOR VIDEO RECORDING
# #--------------------------------------------

# # col1_vid, col2_vid, col3_vid = video_tab.columns([2.8, 0.3, 3])
# # col1.write(" ") #line break

# #-------------------##-----------------------
# #       VIDEO TAB, COLUMN 1 ELEMENTS
# #--------------------------------------------
# # with col1_vid:
# #     #might need to add a container

# #     st.subheader("Upload a face recording!")
# #     #user input panel subheader

#     #------------Camera Recoding-------------#
#     st.write("Choose a pre-recorded video of your face showing your current emotion and upload it below!")

#     #initialize video recording
#     # video_recorder = VideoRecorder()

#     # video_recorder = VideoRecorder()

#     # ctx = webrtc_streamer(key="sendonly-video",
#     #                     video_frame_callback=video_recorder.recv,
#     #                     video_processor_factory=lambda: video_recorder)
#     # #to do: check ctx object if its returning an openable video
#     # # >>> modify webcam.py module

#     # #create start and stop buttons in seprate colums
#     # start = st.button('🔴 Start Face Recording',
#     #                                use_container_width=True)
#     # stop = st.button('🟢 Stop Face Recording',
#     #                               use_container_width=True)

#     # #progress bar to show start and stop of video recording
#     # progress_bar = st.progress(0)

#     #--------------------------------------#
#     #            RECORDING
#     #--------------------------------------#
#     # while ctx.state.playing:
#     #     with lock:
#     #         img = img_container["img"]
#     #     if img is None:
#     #         continue

#     #define video recording variable
#     # video_cap = None

#     # if start:
#     #     video_recorder.start_recording()
#     #     st.write("🎥 Recording in Session...")

#     # if stop:
#     #     video_file_path = video_recorder.stop_recording()
#     #     if video_file_path:
#     #         st.write("💾 Recording Saved!")  # Indicate successful saving
#     #     else:
#     #         st.write("Recording is not started!")  # Indicate no recording started

#     # while True:
#     #     if video_recorder.recording:
#     #         time.sleep(1)
#     #         progress_bar.progress(video_recorder.frame_count / 30)
#     #     else:
#     #         break

#     # # Reset the progress bar
#     # progress_bar.progress(0)

#     #------------video file submission-------------#
# #     with st.form("video_input"):
# #         uploaded_video = st.file_uploader("or upload a video showing your face:", type=["mp4", "avi"])
# #         st.session_state["uploaded_video"] = None

# #         vid_col_submit, vid_col_blank, vid_col_reset = st.columns([2, 2, 1.2])

# #         #submit button as trigger for emotion extraction to playlist generation
# #         vid_submit_button = vid_col_submit.form_submit_button("▶ Generate Playlist",
# #                                                       args=[uploaded_video],
# #                                                       )

# #         #buttton to clear all video/s created or uploaded
# #         vid_reset_button = vid_col_reset.form_submit_button("↺ Reset",
# #                                                         args=[image_captured, uploaded_image],
# #                                                         on_click=reset_img_form,
# #                                                         use_container_width=True)


# #     if vid_submit_button:
# #         if uploaded_video:
# #             uploaded_vid_file = save_uploaded_file(uploaded_video)
# #             st.write("Reading emotion from uploaded video...")

# #         else:
# #             st.write("No input detected 😵")
# #             st.write("Please choose one of the designated image extraction methods above (🎥 or 📥). ")
# #             #default message when submit button was pressed but no file was fed.

# #     if vid_reset_button:
# #             st.write("✅ Reset media objects successful")
# #             st.write("Record a webcam face stream 🎥 or upload a video 📥 and click \" ▶️ Generate Playlist \".")


# # col1_vid.caption("Application Accuracy: <80.56%>")
# # #to do: change metric to appropriate score result

# #--------------------------------------------
# #       VIDEO TAB, COLUMN 3 ELEMENTS
# #--------------------------------------------
# # Display generated playlist
# # with col3_vid:
# #     st.subheader(" ")
# # Display generated playlist
#     # if video_cap:

#     #     input_file = video_cap

#     #     if input_file:
#     #         st.subheader(" ")
#     #         with st.spinner("Reading emotion from webcam recording..."):
#     #             time.sleep(2)
#     #             emotion = extract_emotion(input_file=input_file)

#     #             if emotion:
#     #                 emo_key = next(iter(emotion[0]))
#     #                 st.write(f"Emotion Extracted: {emo_key}")


#     #             #playlist generation function
#     #                 with st.spinner("Transforming Emotions into Melodies..."):
#     #                     # to improve: change into progress bar/ specify state after merging other functions
#     #                     time.sleep(3)  # simulate playlist generation time
#     #                     playlist, playlist_url = gen_playlist_ui(emotion)
#     #                     show_playlist(playlist_url=playlist_url)

#     # if uploaded_video:

#     #     input_file_upload = uploaded_vid_file

#     #     if input_file_upload:
#     #         st.subheader(" ")
#     #         with st.spinner("Starting playlist generation..."):
#     #             time.sleep(2)
#     #             emotion = extract_emotion(input_file=input_file_upload)

#     #             if emotion:
#     #                 emo_key = next(iter(emotion[0]))
#     #                 st.write(f"Emotion Extracted: {emo_key}")

#     #             #playlist generation function
#     #                 with st.spinner("Transforming Emotions into Melodies..."):
#     #                     # to improve: change into progress bar/ specify state after merging other functions
#     #                     time.sleep(3)  # simulate playlist generation time
#     #                     playlist, playlist_url = gen_playlist_ui(emotion)
#     #                     show_playlist(playlist=playlist, playlist_url=playlist_url)
#     # else:
#     #     st.subheader(" ")
#     #     st.image("interface/images/Playlist-amico (1).png")
#     #     #image attribute: <a href="https://storyset.com/app">App illustrations by Storyset</a>

#     #     st.markdown("""
#     #     <h1 style="font-size: 20px; text-align: center; color: #faaa0b">
#     #     Just chillin' for now...
#     #     </h1>
#     #     """, unsafe_allow_html=True)
