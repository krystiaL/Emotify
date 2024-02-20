import streamlit as st

def instructions_page():
    st.title("How to use this application:")

    col_ex1, col_ex2 = st.columns([0.5, 2])
    #step 1
    col_ex1.write(" ")
    col_ex1.image("interface/images/upload_icon.png")
    col_ex2.write(" ")
    col_ex2.write("Upload a photo or video showing your face.")
    #step 2
    col_ex1.subheader(" ")
    col_ex1.image("interface/images/click_submit_icon.png")
    col_ex2.write("Click the submit button to start the emotion extraction process.")
    #step 3
    col_ex1.title(" ")
    col_ex1.subheader(" ")
    col_ex1.image("interface/images/emoji_icons.png")
    col_ex2.write("Please give the application some time to identify the emotion from the image or video file.")
    #step 4
    col_ex1.title(" ")
    col_ex1.title(" ")
    col_ex1.subheader(" ")
    col_ex1.image("interface/images/processing_icon.png")
    col_ex2.write("After emotion recognition, the application will start generating the playlist based on the extracted emotion from the image/video.")
    #step 5
    col_ex1.title(" ")
    col_ex1.title(" ")
    col_ex1.subheader(" ")
    col_ex1.image("interface/images/musical_notes_icon.png")
    col_ex2.write("Play the generated playlist from the website and/or save it to your Spotify account library.")
