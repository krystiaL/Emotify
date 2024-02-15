import streamlit as st
import time

# Page title and icon
st.set_page_config(page_title="<Music Selector Name>", page_icon=":musical_note:", layout="wide")

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
st.subheader("Generate a playlist befitting your mood")
st.subheader(" ")

# Sidebar
with st.sidebar:
    st.title("Tune in your Emotion")
    st.image("images/emotion_spectrum.jpg")
    # Get user's current mood
    mood = st.selectbox("Your mood:", list(moods.keys()))

#configure page layout
# Create two columns
col1, col2 = st.columns(2)

with col1:
    # Display image in left column
    st.image("images/Playlist-amico.png")
    #image attribute:<a href="https://storyset.com/app">App illustrations by Storyset</a>
    st.write("Upload a photo of your face showing how your currently feel.")
    #take a video of your current emotions (change this when incorporating a webcam instead )

    uploaded_file = st.file_uploader("Upload a picture of your face", type=["png", "jpeg", "jpg"])
    #can add more file type

    if uploaded_file is not None:
        st.sidebar.image(uploaded_file)

with col2:
    # Display text in right column
    st.write("Tune in your emotions, Transform Out your playlist!")
    st.write("How to use this app💡")
    st.write("list of instructions here...")


# Add a spinner to indicate playlist generation
with st.spinner("Transforming Emotions into Melodies..."):
    time.sleep(5)  # simulate playlist generation time

# Display generated playlist
st.subheader(f"Here's your playlist for {mood.lower()} mood:")
for playlist in moods[mood]:
    st.write(playlist)

st.write("Connect to your Spotify account and share this app with your friends!")
st.link_button("button docu", "https://docs.streamlit.io/library/api-reference/widgets/st.link_button")
