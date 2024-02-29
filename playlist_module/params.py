import os

########VARIABLES######
SPOTIFY_CLIENT_ID = os.environ.get("SPOTIFY_CLIENT_ID")
SPOTIFY_SECRET = os.environ.get("SPOTIFY_SECRET")
SPOTIFY_USERNAME = os.environ.get("SPOTIFY_USERNAME")
REDIRECT_URI = os.environ.get("REDIRECT_URI")
ACCOUNT_NAME = os.environ.get("ACCOUNT_NAME")

if not all([SPOTIFY_CLIENT_ID, SPOTIFY_SECRET, SPOTIFY_USERNAME, REDIRECT_URI]):
    raise ValueError("One or more required environment variables are not set.")
