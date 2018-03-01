# coding=utf8
import requests
from flask import session
from config import (client_id, client_secret, redirect_uri, scope,
                    authorization_base_url, token_url, user_profile_url,
                    user_playlists_url, users_base_url, tracks_url,
                    audio_features_url,)

def get_token(code):
    return '<Response [200]>'


def get_user_profile():
    return ['ivtt57fgh0z5goqb1vqq5o9ff', 'valerie']


def get_user_playlists():
    return [{u'name': u'Test Tempo', u'collaborative': False, u'external_urls': 
            {u'spotify': u'https://open.spotify.com/user/ivtt57fgh0z5goqb1vqq5o9ff/playlist/3Q4gdFJkUc8cS2ff52Cin6'}, 
            u'uri': u'spotify:user:ivtt57fgh0z5goqb1vqq5o9ff:playlist:3Q4gdFJkUc8cS2ff52Cin6', 
            u'public': True, u'owner': {u'display_name': u'valerie', u'external_urls': 
            {u'spotify': u'https://open.spotify.com/user/ivtt57fgh0z5goqb1vqq5o9ff'}, 
            u'uri': u'spotify:user:ivtt57fgh0z5goqb1vqq5o9ff', u'href': 
            u'https://api.spotify.com/v1/users/ivtt57fgh0z5goqb1vqq5o9ff', u'type': 
            u'user', u'id': u'ivtt57fgh0z5goqb1vqq5o9ff'}, u'tracks': {u'total': 2, 
            u'href': u'https://api.spotify.com/v1/users/ivtt57fgh0z5goqb1vqq5o9ff/playlists/3Q4gdFJkUc8cS2ff52Cin6/tracks'}, 
            u'href': u'https://api.spotify.com/v1/users/ivtt57fgh0z5goqb1vqq5o9ff/playlists/3Q4gdFJkUc8cS2ff52Cin6', 
            u'snapshot_id': u'tzntQoout/3RFnCxnzIVghEZ4vr4qSwxWgMv74408hZBCCAzNhbZ6mQCCI+l1UUp', 
            u'images': [{u'url': u'https://i.scdn.co/image/3a3fc1256e0b30ebedd13dee5d3071744163cd63', 
            u'width': 640, u'height': 640}], u'type': u'playlist', u'id': u'3Q4gdFJkUc8cS2ff52Cin6'}, 
            {u'name': u'Test Length', u'collaborative': False, u'external_urls': 
            {u'spotify': u'https://open.spotify.com/user/ivtt57fgh0z5goqb1vqq5o9ff/playlist/4j5J5D0tO3qKbsfZGMaAAl'}, 
            u'uri': u'spotify:user:ivtt57fgh0z5goqb1vqq5o9ff:playlist:4j5J5D0tO3qKbsfZGMaAAl', 
            u'public': True, u'owner': {u'display_name': u'valerie', u'external_urls': 
            {u'spotify': u'https://open.spotify.com/user/ivtt57fgh0z5goqb1vqq5o9ff'}, 
            u'uri': u'spotify:user:ivtt57fgh0z5goqb1vqq5o9ff', u'href': 
            u'https://api.spotify.com/v1/users/ivtt57fgh0z5goqb1vqq5o9ff', u'type': 
            u'user', u'id': u'ivtt57fgh0z5goqb1vqq5o9ff'}, u'tracks': {u'total': 2, 
            u'href': u'https://api.spotify.com/v1/users/ivtt57fgh0z5goqb1vqq5o9ff/playlists/4j5J5D0tO3qKbsfZGMaAAl/tracks'}, 
            u'href': u'https://api.spotify.com/v1/users/ivtt57fgh0z5goqb1vqq5o9ff/playlists/4j5J5D0tO3qKbsfZGMaAAl', 
            u'snapshot_id': u'k1whELLCMVx5q2e5NbefvXNwdq2ivQr81K270yJ+sEHxzPVoQvGwLqkO8jqAOfyF', 
            u'images': [{u'url': u'https://i.scdn.co/image/fb0904566decc62b67b26e864e556e33166c7a73', 
            u'width': 640, u'height': 640}], u'type': u'playlist', u'id': u'4j5J5D0tO3qKbsfZGMaAAl'}]


# def get_playlist_data(sp_user_id, sp_playlist_id):
#     """Get playlist and track information for a given list of playlists"""

#     url = (users_base_url + sp_user_id + '/playlists/' + sp_playlist_id)
#     headers = create_headers()
#     payload = {'fields': 'name,tracks.items(track(id,name,artists(name),album(name),duration_ms,explicit))'}
    
#     response = requests.get(url, headers=headers, params=payload)
#     playlist_data = response.json()
#     playlist_name= playlist_data['name']
#     tracks_to_add = playlist_data['tracks']['items']

#     return [playlist_name, tracks_to_add]


# def get_tracks_sp(tracks_to_add):
#     """Get Spotify track objects for multiple track IDs"""

#     headers = create_headers()
#     payload = {'ids': tracks_to_add}

#     response = requests.get(tracks_url, headers=headers, params=payload)
#     print response
    
#     basic_track_info = response.json()['tracks']

#     return basic_track_info


# def get_audio_features_sp(tracks_to_add):
#     """Get Spotify audio feature objects for multiple track ids"""

#     headers = create_headers()
#     payload = {'ids': tracks_to_add}

#     response = requests.get(audio_features_url, headers=headers, params=payload)
#     audio_features = response.json()['audio_features']

#     return audio_features


def get_playlist_tracks_sp(sp_user_id, sp_playlist_id):
    return [u'5oK98mpTJSU0iqLHN1hZ3y', u'1cYgEwkyb7xOwtlosTPRdy']


def update_playlist_sp(sp_user_id, sp_playlist_id, new_track_ids):
    return '<Response [201]>'
