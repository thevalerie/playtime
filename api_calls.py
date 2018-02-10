# coding=utf8
from requests_oauthlib import OAuth2Session
import requests
from flask import session
from model import User, Playlist, PlaylistTrack, Track, connect_to_db, db
from config import (client_id, client_secret, redirect_uri, scope,
                    authorization_base_url, token_url, user_profile_url,
                    user_playlists_url, users_base_url, audio_features_url,)


def create_oauth():
    """Create OAuth2 object"""
    
    oauth = OAuth2Session(client_id=client_id, redirect_uri=redirect_uri, scope=scope)

    return oauth


def create_headers():
    """Create headers for API requests with the access token"""

    headers = {'Authorization': 'Bearer ' + session['access_token']}

    return headers


def get_auth_url(oauth):
    """Takes in OAuth2 object, generates auth URL and state"""
    
    return oauth.authorization_url(authorization_base_url)


def get_token(code):
    """Get OAuth token"""

    # import pdb; pdb.set_trace()

    # create params to send to retrieve OAuth token
    payload = {'grant_type': 'authorization_code',
               'code': code,
               'redirect_uri': redirect_uri,
               'client_id': client_id,
               'client_secret': client_secret,}

    # request token from API
    response = requests.post(token_url, payload)

    return response


def get_user_profile(url):

    headers = create_headers()
    response = requests.get(url, headers=headers)
    spotify_user = response.json()

    return [spotify_user['id'], spotify_user['display_name']]


def get_user_playlists(url):

    headers = create_headers()
    response = requests.get(url, headers=headers)
    spotify_playlists = response.json()['items']

    return spotify_playlists


def get_playlist_data(sp_user_id, sp_playlist_id):

    url = (users_base_url + sp_user_id + '/playlists/' + sp_playlist_id)
    headers = create_headers()
    payload = {'fields': 'name,tracks.items(track(id,name,artists(name),album(name),duration_ms,explicit))'}
    
    response = requests.get(url, headers=headers, params=payload)
    playlist_data = response.json()
    playlist_name= playlist_data['name']
    tracks_to_add = playlist_data['tracks']['items']

    return [playlist_name, tracks_to_add]


def get_track_data(sp_track_id):

    url = (audio_features_url + sp_track_id)
    headers = create_headers()
    
    response = requests.get(url, headers=headers)
    audio_features = response.json()

    return audio_features


def get_playlist_tracks(sp_user_id, sp_playlist_id):

    url = (users_base_url + sp_user_id + '/playlists' + sp_playlist_id + '/tracks')
    headers = create_headers()
    payload = {'fields': 'items(track(id))'}

    response = requests.get(url, headers=headers, params=payload)
    sp_tracks = response.json()

    return sp_tracks









