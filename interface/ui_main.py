#---------------------------------------------------
#          LIBRARY AND MODULE IMPORTS
#---------------------------------------------------
import streamlit as st
import cv2
import time
import os
import tempfile


import instructions
import regarding_spotify_interact
import about_us

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
#          PATHS AND TEMP FILES
#---------------------------------------------------

# Get the path of the downloads folder
downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")

# # Set the downloads_path as an environment variable
# os.environ["DOWNLOADS_PATH"] = downloads_path

temp_file = tempfile.NamedTemporaryFile()
downloads_path = temp_file.name

#---------------------------------------------------
#             FUNCTIONS
#---------------------------------------------------

def dummy_img_and_vid_function():
    #This dummy function takes the either image or video files as input and returns the playlist
    #to be omitted and replaced with the playlist generator functions
    st.subheader(f"Here's a <identified emotion> playlist for you!")

    #embedd to spotify interface; to do: check if there are other ways to do this
    st.write("Add this playlist to your Spotify library!")
    st.markdown('<iframe src="https://open.spotify.com/embed/playlist/0HI7czcgdxj4bPu3eRlc2C?utm_source=generator"\
    width="500" height="400"></iframe>', unsafe_allow_html=True)
    #change with generated playlist link


def process_file(file):
    #This function takes one required argument which is either an image or a video file from the file_uploader forms
    #and process the corresponding file type after user input.
    if file.type.startswith('image'):
        # process image
        image_file = st.image(file)
        return image_file
    elif file.type.startswith('video'):
        # process video
        video_file = st.video(file)
        return video_file
    else:
        st.write("Unsupported file type")
        #default if the file submitted is not among the required file types


# Define codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('video_file.mp4', fourcc, 20.0, (640, 480))

def record_video():
    #Function to start the recording; might consider making this into an independent module
    global webcam, out
    if not webcam.isOpened():
        st.write("Error: Camera not found or already in use.")
        return

    while True:
        ret, frame = webcam.read()
        if not ret:
            break
        out.write(frame)
        cv2.imshow('Video', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    webcam.release()
    out.release()
    cv2.destroyAllWindows()


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

image_tab, video_tab = st.tabs(["Face Capture", "Face Recording"])

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
        st.session_state["image_captured"] = None
        # Initialized camera state variable

        uploaded_image = st.file_uploader("or upload an image of your face:", type=["png", "jpeg", "jpg"])
        #image_upload function using file_uploader widget
        st.session_state["uploaded_image"] = None
        # Initialized file uploader state variable


        submit_button = st.form_submit_button("Extract Emotion from File", args=[image_captured, uploaded_image])
        #submit button as entry for file extraction to image/video model pipe

        if submit_button:
            if uploaded_image:
                st.session_state["uploaded_image"] = uploaded_image
                st.write("Reading emotion from selfie...")
                #entry point for model input;
                # to do: add model function here

            elif image_captured:
                st.session_state["image_captured"] = image_captured
                st.write("Reading emotion from image file...")
                #entry point for model input;
                # to do: add model function here
            else:
                st.write("No input detected 😵")
                #default message when submit button was pressed but no file was fed.

col1.caption("Application Accuracy: <80.56%>")
#to do: change metric to appropriate score result

#--------------------------------------------
#       IMAGE TAB, COLUMN 3 ELEMENTS
#--------------------------------------------

# Display generated playlist
with col3:
    st.write(" ")
    if st.session_state.get("image_captured"):
        uploaded_image = st.session_state["image_captured"]
        st.write("-Emotion Extracted-")
        #playlist generation for camera capture
        with st.spinner("Transforming Emotions into Melodies..."):
            # to improve: change into progress bar/ specify state after merging other functions
            time.sleep(5)  # simulate playlist generation time
        dummy_img_and_vid_function()

    elif st.session_state.get("uploaded_image"):
        uploaded_image = st.session_state["uploaded_image"]
        st.write("Image input detected")
        with st.spinner("Transforming Emotions into Melodies..."):
            time.sleep(5)  # simulate playlist generation time
        dummy_img_and_vid_function()

    # elif st.session_state.get("recording"):
    #     #playlist generation for camera capture
    #     with st.spinner("Transforming Emotions into Melodies..."):
    #         # to improve: change into progress bar/ specify state after merging other functions
    #         time.sleep(5)  # simulate playlist generation time
    #     dummy_img_and_vid_function()

    else:
        st.subheader(" ")
        col3.image("interface/images/Playlist-amico (1).png")
        #image attribute: <a href="https://storyset.com/app">App illustrations by Storyset</a>

        col3.markdown("""
        <h1 style="font-size: 20px; text-align: center; color: #faaa0b">
        Just chillin' for now...
        </h1>
        """, unsafe_allow_html=True)


#--------------------##----------------------
#    SPLIT TAB LAYOUT FOR CAMERA RECORDING
#--------------------------------------------

col1_vid, col2_vid, col3_vid = video_tab.columns([2.8, 0.3, 3])
col1.write(" ") #line break

#-------------------##-----------------------
#       VIDEO TAB, COLUMN 1 ELEMENTS
#--------------------------------------------
with col1_vid:
    st.write(" ")
    #contains application tagline and the user input panel
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

    st.subheader("Take a selfie!")
    #user input panel subheader

    container = st.container(border=True)
    container.markdown("""
    <h1 style="font-weight: lighter; font-size: 20px; text-align: center">
    Take a picture of your face showing your current emotion
    </h1>
    """, unsafe_allow_html=True)

    #--------------Camera Image---------------#
    with st.form("video_input"):
   #------------Camera Recoding-------------#
        st.caption("for face(video) recording:")

        webcam = cv2.VideoCapture(0)
        #main camera; unable to show cam stream >>> st.camera_input is in use

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
        if start:
            #Initialize start time
            start_time = time.time()
            #Start recording
            record_video()

            while True:
                # Do some heavy processing here
                time.sleep(5)
                # to do: replace this with actual processing time

                # Calculate the progress
                elapsed_time = time.time() - start_time
                progress = int(elapsed_time / 1 * 10)
                # assuming the progress should increase every 1 second
                # to do: replace with actual progress

                # Update the progress bar
                progress_bar.progress(progress)

                # Check if the user wants to stop recording
                if stop:
                    break

            # Stop recording
            progress_bar.empty()

        uploaded_video = st.file_uploader("Choose a video:", type=["mp4"])
        st.session_state["uploaded_video"] = None

        submit_button = st.form_submit_button("Submit Video", args=[uploaded_video])
        #submit button as entry for file extraction to image/video model pipe
        #to do: figure out the return file for webcam face recording function
        if submit_button:
            if webcam:
                st.write("Reading emotion from face recording...")

            elif uploaded_video:
                st.write("Reading emotion from video file...")
                st.session_state["uploaded_video"] = uploaded_video



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
