import streamlit as st

def about_us():
    st.title("Meet the Team!")
    st.write("We comprise a cohort of aspiring data scientists enrolled in Batch 1384 of Le Wagon Tokyo's rigorous part-time Data Science program.")

    col1, col2, col3 = st.columns([0.3,2,2])

    with col2:
        st.image("interface/images/team_pics/atsuto_face.jpg", caption="Atsuto Tatsumi", width=150)
        st.image("interface/images/team_pics/daisuke_face.jpg", caption="Daisuke Kurata", width=150)

    with col3:
        st.image("interface/images/team_pics/krys_face.jpg", caption="Krystia Lewis", width=150)
        st.image("interface/images/team_pics/robert_face.jpg", caption="Robert Kanashiro", width=150)
