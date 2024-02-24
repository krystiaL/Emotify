import streamlit as st
import cv2
import tempfile
import time


# Page title and icon
st.set_page_config(page_title="<Music Selector Name>", page_icon=":musical_note:", layout="wide")

#Default moods and corresponding songs
# note: change this into the working code

moods = {
    "Happy": ["song 1", "song 2", "song 3", "song 4", "song 5"],
    "Sad": ["song 1", "song 2", "song 3", "song 4", "song 5"],
    "Excited": ["song 1", "song 2", "song 3", "song 4", "song 5"],
    "Relaxed": ["song 1", "song 2", "song 3", "song 4", "song 5"]
}

def dummy_text_function():
    st.subheader(f"Here's a {mood.lower()} playlist for you!")
    for playlist in moods[mood]:
        return st.write(playlist)

def dummy_image_function():
    st.subheader(f"Here's a <identified emotion> playlist for you!")
    st.write("imagine this is a list of songs")

def dummy_video_function():
    st.subheader(f"Here's a <identified emotion> playlist for you!")
    st.write("imagine this is a list of songs")


#---------------------------------------------------------------

# Header and Description
st.title("<Music Selector Project>") #official name still hasn't been decided
st.write(" ")

col3, col4 = st.columns([1.5,3])
col3.title(" ")
with col3:
    st.subheader("Tune in your Emotions, Transform out your Playlist!")
    st.subheader(" ")
    col3_1, col3_2, col3_3 = col3.columns([0.5,1,0.5])
    col3_2.image("images/inst_flow1_hd.png")


col3.title(" ")
col3.caption("Application Accuracy: <80.56%>")
col4.image("/root/code/Atsuto-T/Music_Selector_Project/music-selector/interface/images/Playlist-amico (1).png")
#image attribute: <a href="https://storyset.com/app">App illustrations by Storyset</a>
st.subheader(" ")

#---------------------------------------------------------------

# Sidebar

with st.sidebar:
    st.title("About <Music Selector>") #change to official name
    st.image("/root/code/Atsuto-T/Music_Selector_Project/music-selector/interface/images/Music-cuate.png")
    #attribute: <a href="https://storyset.com/app">App illustrations by Storyset</a>

    instructions = {
        2: "Click the submit button to start the process.",
        3: "Please give the application some time identify the emotion to be used.",
        4: "After emotion recognition, the application will start generating the playlist based on the extracted emotion from the image/video.",
        5: "Play the generated playlist from the website and/ save it to your Spo."
    }

    with st.expander("How to generate your playlist?"):
        col_ex1, col_ex2 = st.columns([0.5, 2])
        #step 1
        col_ex1.write(" ")
        col_ex1.image("images/upload_icon.png")
        col_ex2.write(" ")
        col_ex2.write("Upload a photo or video showing your face.")
        #step 2
        col_ex1.subheader(" ")
        col_ex1.image("images/click_submit_icon.png")
        col_ex2.write("Click the submit button to start the emotion extraction process.")
        #step 3
        col_ex1.title(" ")
        col_ex1.subheader(" ")
        col_ex1.image("images/emoji_icons.png")
        col_ex2.write("Please give the application some time to identify the emotion from the image or video file.")
        #step 4
        col_ex1.title(" ")
        col_ex1.title(" ")
        col_ex1.subheader(" ")
        col_ex1.image("images/processing_icon.png")
        col_ex2.write("After emotion recognition, the application will start generating the playlist based on the extracted emotion from the image/video.")
        #step 5
        col_ex1.title(" ")
        col_ex1.title(" ")
        col_ex1.subheader(" ")
        col_ex1.image("images/musical_notes_icon.png")
        col_ex2.write("Play the generated playlist from the website and/or save it to your Spotify account library.")


    with st.expander("How to add the playlist to your Spotify library?"):
        st.write('''
                dummy text
                 ''')
    with st.expander("How to reset the generation process"):
        st.write('''
                 dummy text
                 ''')
    with st.expander("Meet the Team!"):
        st.write('''
                 dummy text
                 ''')

#---------------------------------------------------------------

#configure page layout
# three columns for inputs
col1, col2,  col3 = st.columns([3, 0.8, 4])

with col1:
    #image input form
    st.write(" ")
    st.subheader("       Take a selfie!")


    with st.form("image_input"):
        # # Initialize camera state variable
        # if "image_captured" not in st.session_state:

        image_captured = st.camera_input("Take a picture of your face showing how you feel")
        st.session_state["image_captured"] = None
        uploaded_image = st.file_uploader("Or choose a picture:", type=["png", "jpeg", "jpg"])
        st.session_state["uploaded_image"] = None

        submit_button = st.form_submit_button("Submit Image", args=[image_captured])
        if submit_button:
            if uploaded_image:
                st.session_state["uploaded_image"] = uploaded_image
                st.write("Image upload detected")
            elif image_captured:
                st.session_state["image_captured"] = image_captured
                st.write("Camera image detected")

with col1:
    #video input form
    st.write(" ")
    st.subheader("Take a short video!")
    with st.form("video_input"):
        uploaded_video = st.file_uploader("Choose a video:", type=["mp4"])
        st.session_state["uploaded_video"] = None
        submit_button = st.form_submit_button("Submit Video")
        if submit_button:
            st.write("Video input detected")
            st.session_state["uploaded_video"] = uploaded_video

with col1:
    # text input form
    st.subheader("Select a mood!")
    with st.form("text_input"):
        mood = st.selectbox("Choose an emotion:", list(moods.keys()))
        st.session_state["mood"] = None
        submit_button= st.form_submit_button("Submit Emotion")
        if submit_button:
            st.write("Emotion selected")
            st.session_state["mood"] = mood

# Display generated playlist based on input
with col3:
    st.write(" ")
    if st.session_state.get("uploaded_image"):
        uploaded_image = st.session_state["uploaded_image"]
        st.write("Image input detected")
        with st.spinner("Transforming Emotions into Melodies..."):
            time.sleep(5)  # simulate playlist generation time
        dummy_image_function()

        #link to spotify
        st.write("Add this playlist to your Spotify library!")
        st.markdown('<iframe src="https://open.spotify.com/embed/playlist/0HI7czcgdxj4bPu3eRlc2C?utm_source=generator"\
        width="500" height="400"></iframe>', unsafe_allow_html=True)
        #change with dynamic link

    elif st.session_state.get("image_captured"):
        uploaded_image = st.session_state["image_captured"]
        st.write("Camera Image detected")
        with st.spinner("Transforming Emotions into Melodies..."):
            time.sleep(5)  # simulate playlist generation time
        dummy_image_function()

        #link to spotify
        st.write("Add this playlist to your Spotify library!")
        st.markdown('<iframe src="https://open.spotify.com/embed/playlist/0HI7czcgdxj4bPu3eRlc2C?utm_source=generator"\
        width="500" height="400"></iframe>', unsafe_allow_html=True)
        #change with dynamic link

    elif st.session_state.get("uploaded_video"):
        uploaded_video = st.session_state["uploaded_video"]
        st.write("Video input detected")
        with st.spinner("Transforming Emotions into Melodies..."):
            time.sleep(5)  # simulate playlist generation time
        dummy_video_function()

        #link to spotify
        st.write("Add this playlist to your Spotify library!")
        st.markdown('<iframe src="https://open.spotify.com/embed/playlist/0HI7czcgdxj4bPu3eRlc2C?utm_source=generator"\
        width="500" height="400"></iframe>', unsafe_allow_html=True)
        #change with dynamic link

    elif st.session_state.get("mood"):
        mood = st.session_state["mood"]
        st.write(f"Selected emotion: {mood}")
        with st.spinner("Transforming Emotions into Melodies..."):
            time.sleep(5)  # simulate playlist generation time
        dummy_text_function()

        #embeded link to spotify
        st.write("Add this playlist to your Spotify library!")
        st.markdown('<iframe src="https://open.spotify.com/embed/playlist/0HI7czcgdxj4bPu3eRlc2C?utm_source=generator"\
        width="500" height="400"></iframe>', unsafe_allow_html=True)
        #change with dynamic link

    else:
        st.subheader(" ")
        st.caption("                 Please Choose your preferred input type to generate the playlist.")

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
