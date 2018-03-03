# coding=utf8
import requests
from flask import session
from config import (client_id, client_secret, redirect_uri, scope,
                    authorization_base_url, token_url, user_profile_url,
                    user_playlists_url, users_base_url, tracks_url,
                    audio_features_url, recommendations_url)


def create_headers():
    """Create headers for API requests with the access token"""
    
    headers = {'Authorization': 'Bearer ' + session['access_token']}

    return headers


def get_token(code):
    """Get OAuth token"""

    # create params to send to retrieve OAuth token
    payload = {'grant_type': 'authorization_code',
               'code': code,
               'redirect_uri': redirect_uri,
               'client_id': client_id,
               'client_secret': client_secret,}

    # request token from API
    response = requests.post(token_url, payload)

    return response


def get_user_profile():
    """Get the current user's Spotify ID and display name"""

    headers = create_headers()

    response = requests.get(user_profile_url, headers=headers)
    spotify_user = response.json()

    return [spotify_user['id'], spotify_user['display_name']]


def get_user_playlists():
    """Get all playlists owned by the current user (limit of 20)"""

    headers = create_headers()
    # payload = {'offset': offset}

    response = requests.get(user_playlists_url, headers=headers)
    spotify_playlists = response.json()['items']

    return spotify_playlists


def get_playlist_data(sp_user_id, sp_playlist_id):
    """Get playlist and track information for a given list of playlists"""

    url = (users_base_url + sp_user_id + '/playlists/' + sp_playlist_id)
    headers = create_headers()
    payload = {'fields': 'name,tracks.items(track(id,name,artists(name),album(name),duration_ms,explicit))'}
    
    response = requests.get(url, headers=headers, params=payload)
    playlist_data = response.json()
    playlist_name = playlist_data['name']
    tracks_to_add = playlist_data['tracks']['items']

    return [playlist_name, tracks_to_add]


def get_tracks_sp(tracks_to_add):
    """Get Spotify track objects for multiple track IDs"""

    headers = create_headers()
    payload = {'ids': tracks_to_add}

    response = requests.get(tracks_url, headers=headers, params=payload)
    
    basic_track_info = response.json()['tracks']

    return basic_track_info


def get_audio_features_sp(tracks_to_add):
    """Get Spotify audio feature objects for multiple track ids"""

    headers = create_headers()
    payload = {'ids': tracks_to_add}

    response = requests.get(audio_features_url, headers=headers, params=payload)
    audio_features = response.json()['audio_features']

    return audio_features


def get_playlist_tracks_sp(sp_user_id, sp_playlist_id):
    """Get Spotify track IDs for all tracks in a given playlist"""

    url = (users_base_url + sp_user_id + '/playlists/' + sp_playlist_id + '/tracks')
    headers = create_headers()
    payload = {'fields': 'items(track(id))'}

    response = requests.get(url, headers=headers, params=payload)
    sp_tracks = response.json()['items']
    sp_track_ids = [track['track']['id'] for track in sp_tracks]

    return sp_track_ids


def update_playlist_sp(sp_user_id, sp_playlist_id, new_track_ids):
    """Replace all current tracks in a Spotify playlist with a new list of tracks"""

    url = (users_base_url + sp_user_id + '/playlists/' + sp_playlist_id + '/tracks')
    headers = create_headers()
    payload = {'uris': new_track_ids}

    response = requests.put(url, headers=headers, params=payload)

    return response


def delete_tracks_sp(sp_user_id, sp_playlist_id, tracks_to_remove):
    """Remove specified tracks from a specified playlist"""

    url = (users_base_url + sp_user_id + '/playlists/' + sp_playlist_id + '/tracks')
    headers = {'Authorization': 'Bearer ' + session['access_token'], 'Content-Type': 'application/json'}
    payload = {"tracks": tracks_to_remove}

    response = requests.delete(url, headers=headers, json=payload)

    return response


def get_recommendations_sp(parameters):
    """Given a set of parameters, get recommendations from Spotify"""

    headers = create_headers()
    payload = parameters

    response = requests.get(recommendations_url, headers=headers, params=payload)

    basic_track_info = response.json()['tracks']

    seed_info = response.json()['seeds']

    return basic_track_info

