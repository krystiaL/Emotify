import streamlit as st

def how_to_reset():
    reset = {
        1 : "Clear photo captured from camera or uploaded image.",
        2 : "Click the reset button.",
        3 : "Repeat the same steps for the playlist generation process."
    }

    reset_blank1, reset_img, reset_blank2 = st.columns([1, 2, 1])

    reset_img.image("interface/images/reset_icon.png")

    for step, instruction in reset.items():
        st.markdown(f"""
                    <h1 style="font-size: 15px; text-align: left">
                    Step {step}: {instruction}
                    </h1>
                    """, unsafe_allow_html=True)
