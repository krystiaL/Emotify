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


def process_file(file):
    #This function takes one required argument which is either an image or a video file from the file_uploader forms
    #and process the corresponding file type after user input.
    if file.type.startswith('image'):
        # process image
        st.image(file)
        return file
    elif file.type.startswith('video'):
        # process video
        st.video(file)
        return file
    else:
        st.write("Unsupported file type")
        return None
        #default if the file submitted is not among the required file types


# Define codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter(temp_file, fourcc, 20.0, (640, 480))

def record_video():
    #Function to start the recording
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
<h1 style="font-size: 80px;">Music Selector Project</h1>
""", unsafe_allow_html=True) #official name still hasn't been decided
st.write(" ") #line break

#split web layout
col1, col2,  col3 = st.columns([2.8, 0.3, 3])
col1.title(" ") #line break

with col1:
    #contains application tagline and the user input panel
    st.title("Tune in your Emotions, Transform out your Playlist!")
    st.subheader(" ")

    st.subheader("Take a selfie or a video capture!")
    #user input panel subheader

    container = st.container(border=True)
    container.write("Take a picture or a short video recording of your face showing how your current emotion.")
    # wraps boundery for user input

    row1_col1, row1_col2 = container.columns(2)

    with row1_col1:
    #--------------Camera Image---------------#
        image_captured = st.camera_input("click on \"Take Photo\" ")
        # camera widget; will return a jpeg file once image is taken.
        st.session_state["image_captured"] = None
        # Initialized camera state variable

    with row1_col2:
    #------------Camera Recoding-------------#
        container_1 = st.container(border=True)
        container_1.subheader(" ")
        container_1.subheader(" ")
        webcam = cv2.VideoCapture(0)
        #main camera; unable to show cam stream >>> st.camera_input is in use

        container_1.caption("to use ")
        #create start and stop buttons in seprate colums
        start = st.button('Start Face Recording')
        stop = st.button('Stop Face Recording')

        #progress bar to show start and stop of video recording
        progress_bar = st.progress(0)

        # Add a button to start recording
        if start:
            #Initialize start time
            start_time = time.time()

            #Start recording
            while True:
                # Do some heavy processing here
                time.sleep(1)  # replace this with your actual processing

                # Calculate the progress
                elapsed_time = time.time() - start_time
                progress = int(elapsed_time / 10 * 100)  # assuming the progress should increase every 10 seconds

                # Update the progress bar
                progress_bar.progress(progress)

                # Check if the user wants to stop recording
                if stop:
                    break

            # Stop recording
            progress_bar.empty()

    with container.form("collective_input", border=False):
        uploaded_file = st.file_uploader("or upload an image or a video",
                                         type=["image/jpeg", "image/png", "video/mp4", "video/x-msvideo"],
                                         )
        st.session_state["uploaded_file"] = None
        # if uploaded_file is not None:
        #     input_file = process_file(uploaded_file)
        #     st.session_state["uploaded_file"] = None

        submit_button = st.form_submit_button("Extract Emotion from File", args=[uploaded_file])
        if submit_button:
            input_file = st.session_state.get("input_data")
            if input_file:
                st.session_state["uploaded_file"] = input_file
                if input_file.type.startswith('image'):
                    st.write("Reading emotion from image file...")
                elif input_file.type.startswith('video'):
                    st.write("Reading emotion from video file...")


# Display generated playlist based on input
with col3:
    st.write(" ")
    if st.session_state.get("input_file"):
        with st.spinner("Transforming Emotions into Melodies..."): #change into progress bar
            time.sleep(5)  # simulate playlist generation time
        dummy_img_and_vid_function()

        #link to spotify
        st.write("Add this playlist to your Spotify library!")
        st.markdown('<iframe src="https://open.spotify.com/embed/playlist/0HI7czcgdxj4bPu3eRlc2C?utm_source=generator"\
        width="500" height="400"></iframe>', unsafe_allow_html=True)
        #change with dynamic link

    else:
        st.subheader(" ")
        st.caption("          Please Choose your preferred input type to generate the playlist.")

    col1.title(" ")
    col1.caption("Application Accuracy: <80.56%>")

    col3.image("interface/images/Playlist-amico (1).png")
    #image attribute: <a href="https://storyset.com/app">App illustrations by Storyset</a>
    st.subheader(" ")


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
