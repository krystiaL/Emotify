import streamlit as st

def instructions_page():
    col_ex1, col_ex2 = st.columns([0.5, 2])
    #step 1
    col_ex1.write(" ")
    col_ex1.image("interface/images/upload_icon.png")
    col_ex2.image("interface/images/camera_icon.png")
    st.markdown(f"""
                    <h1 style="font-size: 20px; text-align: center; font-family: Trebuchet MS">
                    Choose whether to take a photo of your face using the camera or upload your own image showing your face.
                    </h1>
                    """, unsafe_allow_html=True)
    #step 2
    st.subheader(" ")
    st.image("interface/images/click_generate.png")
    st.markdown(f"""
                    <h1 style="font-size: 20px; text-align: center; font-family: Trebuchet MS">
                    Click the generate button to start the emotion extraction process and playlist generation.
                    </h1>
                    """, unsafe_allow_html=True)

    #step 3
    st.title(" ")
    st.subheader(" ")
    st.image("interface/images/emoji_icons.png")
    st.markdown(f"""
                    <h1 style="font-size: 20px; text-align: center; font-family: Trebuchet MS">
                    Please give the model some time to identify the emotion from the image.
                    </h1>
                    """, unsafe_allow_html=True)

    #step 4
    st.title(" ")
    st.title(" ")
    st.subheader(" ")
    st.image("interface/images/processing_icon.png")
    st.markdown(f"""
                    <h1 style="font-size: 20px; text-align: center; font-family: Trebuchet MS">
                    The model will start generating the playlist based on the extracted emotion from the image.
                    </h1>
                    """, unsafe_allow_html=True)

    #step 5
    st.title(" ")
    st.title(" ")
    st.subheader(" ")
    st.image("interface/images/musical_notes_icon.png")
    st.markdown(f"""
                    <h1 style="font-size: 20px; text-align: center; font-family: Trebuchet MS">
                    Play songs from the generated playlist directly from the Spotify embedding or click "..." to get redirected to Spotify.
                    </h1>
                    """, unsafe_allow_html=True)
