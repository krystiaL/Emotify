import streamlit as st

def spotify_page():
    st.write(" ")

    spot_blank1, spot_img, spot_blank2 = st.columns([0.5, 2, 0.5])

    spot_img.image("interface/images/listen_on_spotify.png")

    st.subheader("I have a Spotify account:")
    st.markdown(f"""
                    <h1 style="font-size: 15px; text-align: justify">
                    The generated playlist will be automatically saved in your library if you have authenticated yourself.
                    </h1>
                    """, unsafe_allow_html=True)
    st.subheader(" ")
    st.subheader("'I don't have a spotify account:")
    st.markdown(f"""
                    <h1 style="font-size: 15px; text-align: justify">
                    You can create a Spotify account and add the generated playlist to your library.
                    </h1>
                    """, unsafe_allow_html=True)
