import os
import streamlit as st

########VARIABLES######
#To run locally;
# SPOTIFY_CLIENT_ID = os.environ.get("SPOTIFY_CLIENT_ID")
# SPOTIFY_SECRET = os.environ.get("SPOTIFY_SECRET")
# SPOTIFY_USERNAME = os.environ.get("SPOTIFY_USERNAME")
# REDIRECT_URI = os.environ.get("REDIRECT_URI")
# ACCOUNT_NAME = os.environ.get("ACCOUNT_NAME")

#For Streamlit Cloud;
SPOTIFY_CLIENT_ID = st.secrets["SPOTIFY_CLIENT_ID"]
SPOTIFY_SECRET = st.secrets["SPOTIFY_SECRET"]
SPOTIFY_USERNAME = st.secrets["SPOTIFY_USERNAME"]
REDIRECT_URI = st.secrets["REDIRECT_URI"]
ACCOUNT_NAME = st.secrets["ACCOUNT_NAME"]

if not all([SPOTIFY_CLIENT_ID, SPOTIFY_SECRET, SPOTIFY_USERNAME, REDIRECT_URI]):
    raise ValueError("One or more required environment variables are not set.")
