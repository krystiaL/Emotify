import streamlit as st

def instructions_page():
    #step 1
    step1_img1, step1_blank, step1_img2 = st.columns([2, 0.7, 2])

    st.write(" ")
    step1_img1.image("interface/images/upload_icon.png")
    step1_img2.image("interface/images/camera_icon.png")
    st.markdown(f"""
                    <h1 style="font-size: 15px; text-align: center">
                    Choose whether to take a photo of your face using the camera or upload your own image showing your face.
                    </h1>
                    """, unsafe_allow_html=True)
    #step 2
    step2_blank1, step2_img, step2_blank2 = st.columns([1, 2, 1])

    st.subheader(" ")
    step2_img.image("interface/images/click_generate.png")
    st.markdown(f"""
                    <h1 style="font-size: 15px; text-align: center">
                    Click the generate button to start the emotion extraction process and playlist generation.
                    </h1>
                    """, unsafe_allow_html=True)

    #step 3
    step3_blank1, step3_img, step3_blank2 = st.columns([1, 2, 1])

    st.title(" ")
    st.subheader(" ")
    step3_img.image("interface/images/emoji_icons.png")
    st.markdown(f"""
                    <h1 style="font-size: 15px; text-align: center">
                    Please give the model some time to identify the emotion from the image.
                    </h1>
                    """, unsafe_allow_html=True)

    #step 4
    step4_blank1, step4_img, step4_blank2 = st.columns([1, 2, 1])

    st.title(" ")
    st.title(" ")
    st.subheader(" ")
    step4_img.image("interface/images/processing_icon.png")
    st.markdown(f"""
                    <h1 style="font-size: 15px; text-align: center">
                    The model will start generating the playlist based on the extracted emotion from the image.
                    </h1>
                    """, unsafe_allow_html=True)

    #step 5
    step5_blank1, step5_img, step5_blank2 = st.columns([1, 2, 1])

    st.title(" ")
    st.title(" ")
    st.subheader(" ")
    step5_img.image("interface/images/musical_notes_icon.png")
    st.markdown(f"""
                    <h1 style="font-size: 15px; text-align: center">
                    Play songs from the generated playlist directly from the Spotify embedding or click "..." to get redirected to Spotify.
                    </h1>
                    """, unsafe_allow_html=True)
