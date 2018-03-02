import os

# Spotify app data
client_id = os.environ['SPOTIFY_CONSUMER_KEY']
client_secret = os.environ['SPOTIFY_CONSUMER_SECRET']
redirect_uri = 'http://localhost:5000/login'
scope = 'playlist-modify playlist-modify-private'

# API endpoints
authorization_base_url = 'https://accounts.spotify.com/authorize?'
token_url = 'https://accounts.spotify.com/api/token'
user_profile_url = 'https://api.spotify.com/v1/me'
user_playlists_url = 'https://api.spotify.com/v1/me/playlists'
users_base_url = 'https://api.spotify.com/v1/users/'
tracks_url = 'https://api.spotify.com/v1/tracks/'
audio_features_url = 'https://api.spotify.com/v1/audio-features/'
log_out_url = 'https://www.spotify.com/us/logout/'