import streamlit as st
import time

# Page title and icon
st.set_page_config(page_title="Playlist Alchemy", page_icon=":musical_note:", layout="wide")

#Default moods and corresponding songs
# note: change this into the working code

moods = {
    "Happy": ["list of songs"],
    "Sad": ["list of songs"],
    "Excited": ["list of songs"],
    "Relaxed": ["list of songs"]
}

# Header and Description
st.title("Music Selector Project") #official name still hasn't been decided
st.caption("Transforming Emotions into Melodies")
st.write("Tune in your emotions, Transform Out your playlist!")

# Sidebar
with st.sidebar:
    st.title("Tune in your Emotion")
    # st.sidebar.image("music_selector_logo.png")
    st.write("Upload a photo of your face showing how your currently feel.")
    #take a video of your current emotions (change this when incorporating a webcam instead )

    uploaded_file = st.sidebar.file_uploader("Upload a picture of your face", type=["png", "jpeg", "jpg"])
    #can add more file type

    if uploaded_file is not None:
        st.sidebar.image(uploaded_file)

# Add a spinner to indicate playlist generation
with st.spinner("Sit tight while we generate the playlist for you..."):
    time.sleep(5)  # simulate playlist generation time

# Get user's current mood
mood = st.selectbox("Your mood:", list(moods.keys()))

# Display generated playlist
st.subheader(f"Here's your playlist for {mood.lower()} mood:")
for playlist in moods[mood]:
    st.write(playlist)

st.write("Connect to your Spotify account and share this app with your friends!")
