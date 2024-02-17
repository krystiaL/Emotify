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
    #this is a dummy function for back-up text input
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
col3.subheader("Tune in your Emotions, Transform out your Playlist!")
col3.subheader(" ")
col3.write("1. some graphic instructions here")
col3.write(" ")
col3.write("2. some graphic instructions here")
col3.write(" ")
col3.write("3. some graphic instructions here")

col3.title(" ")
col3.write("Some disclaimer here: data scope, accuracy etc.")
col4.image("/root/code/Atsuto-T/Music_Selector_Project/music-selector/interface/images/Playlist-amico (1).png")
#image attribute: <a href="https://storyset.com/app">App illustrations by Storyset</a>
st.subheader(" ")

#---------------------------------------------------------------

# Sidebar
st.sidebar.title("About <Music Selector>") #change to official name
st.sidebar.image("/root/code/Atsuto-T/Music_Selector_Project/music-selector/interface/images/Music-cuate.png")
#attribute: <a href="https://storyset.com/app">App illustrations by Storyset</a>
st.sidebar.subheader("I. How to generate your playlist?")
st.sidebar.subheader("II. How to add the playlist to your Spotify library?")
st.sidebar.subheader("II. How to reset the playlist generation?")
st.sidebar.subheader("III. Meet the Team")

#---------------------------------------------------------------

#configure page layout
# three columns for inputs
col1, col2,  col3 = st.columns([3, 0.8, 4])

with col1:
    # text input form
    st.subheader("Select your current mood")
    with st.form("text_input"):
        mood = st.selectbox("Choose an emotion:", list(moods.keys()))
        st.session_state["mood"] = None
        submit_button= st.form_submit_button("Submit Emotion")
        if submit_button:
            st.write("Emotion selected")
            st.session_state["mood"] = mood

with col1:
    #image input form
    st.write(" ")
    st.subheader("Upload an image of your face showing how you currently feel")
    with st.form("image_input"):
        uploaded_image = st.file_uploader("Choose a picture:", type=["png", "jpeg", "jpg"])
        st.session_state["uploaded_image"] = None
        submit_button = st.form_submit_button("Submit Image")
        if submit_button:
            st.write("Image input detected")
            st.session_state["uploaded_image"] = uploaded_image


with col1:
    #video input form
    st.write(" ")
    st.subheader("Upload a 10 second video of your face showing how you currently feel")
    with st.form("video_input"):
        uploaded_video = st.file_uploader("Choose a video:", type=["mp4"])
        st.session_state["uploaded_video"] = None
        submit_button = st.form_submit_button("Submit Video")
        if submit_button:
            st.write("Video input detected")
            st.session_state["uploaded_video"] = uploaded_video


# Display generated playlist based on input
with col3:
    st.write(" ")
    if st.session_state.get("mood"):
        mood = st.session_state["mood"]
        st.write(f"Selected emotion: {mood}")
        with st.spinner("Transforming Emotions into Melodies..."):
            time.sleep(5)  # simulate playlist generation time
        dummy_text_function()

        #link to spotify
        st.write("Add this playlist to your Spotify library!")
        st.markdown('<iframe src="https://open.spotify.com/embed/playlist/0HI7czcgdxj4bPu3eRlc2C?utm_source=generator"\
        width="500" height="400"></iframe>', unsafe_allow_html=True)

    elif st.session_state.get("uploaded_image"):
        uploaded_image = st.session_state["uploaded_image"]
        st.write("Image input detected")
        with st.spinner("Transforming Emotions into Melodies..."):
            time.sleep(5)  # simulate playlist generation time
        dummy_image_function()

        #link to spotify
        st.write("Add this playlist to your Spotify library!")
        st.link_button("share to library", "https://docs.streamlit.io/library/api-reference/widgets/st.link_button")

    elif st.session_state.get("uploaded_video"):
        uploaded_video = st.session_state["uploaded_video"]
        st.write("Video input detected")
        with st.spinner("Transforming Emotions into Melodies..."):
            time.sleep(5)  # simulate playlist generation time
        dummy_video_function()

        #link to spotify
        st.write("Add this playlist to your Spotify library!")
        st.link_button("share to library", "https://docs.streamlit.io/library/api-reference/widgets/st.link_button")

    else:
        st.subheader(" ")
        st.caption("                 Please Choose your preferred input type to generate the playlist.")
st.title("Play Uploaded File")

uploaded_file = st.file_uploader("Choose a video...", type=["mp4"])
temporary_location = False

if uploaded_file is not None:
    temporary_location = write_to_disk(uploaded_file)

if temporary_location:
    video_stream = cv2.VideoCapture(temporary_location)
    # Check if camera opened successfully
    if (video_stream.isOpened() == False):
        print("Error opening video  file")
    else:
        # Read until video is completed
        while (video_stream.isOpened()):
            # Capture frame-by-frame
            ret, image = video_stream.read()
            if ret:
                # Display the resulting frame
                st.image(image, channels="BGR", use_column_width=True)
            else:
                break
        video_stream.release()
        cv2.destroyAllWindows()

def write_to_disk(uploaded_file):
    """Writes an uploaded video file to disk and returns the file path."""
    with tempfile.NamedTemporaryFile(delete=False) as out:
        out.write(uploaded_file.read())
        return out.name
