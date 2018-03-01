# coding=utf8
from flask import (Flask, request, session)
import sys
import requests
import config as c
import api_calls as a
import db_functions as f
from model import User, Playlist, PlaylistTrack, Track, Category, connect_to_db, db
# import api_calls as a

def get_auth_url():
    """Create the OAuth authorization URL for the current user"""

    # create params to get code from Spotify OAuth
    payload = [('client_id', c.client_id),
               ('response_type', 'code'),
               ('redirect_uri', c.redirect_uri),
               ('state', 'ohheythere'),
               ('scope', c.scope)]

    auth_url = c.authorization_base_url

    for key, value in payload:
        auth_url += key + '=' + value + '&'

    auth_url = auth_url.rstrip('&')

    print auth_url

    return auth_url


def authenticate_user(code, state):
    """"""

    # if the value for state doesn't match what's in the session,
    # redirect back to homepage and try login again
    if state != session['state']:
        flash("Authentication failed, please try again")
        return redirect('/')

    response = a.get_token(code)
    # if anything other than a 200 response code, call error message func
    if response.status_code != 200:
        return response.status_code

    # if success, save the access token and refresh token to the session
    token = response.json()
    session['access_token'] = token['access_token']
    session['refresh_token'] = token['refresh_token']
    print "Added to session: access_token", session['access_token']
    print "Added to session: refresh_token", session['refresh_token']

    return response.status_code


def add_user_to_session(current_user):
    """Add the current user id to the session"""

    session['current_user'] = current_user.user_id

    print "Added to session: current_user", session['current_user']


def import_user_playlists(sp_user_id, playlists_to_add):
    """send API call to get the playlist info, add playlist and track info to the db"""

    new_playlists = []
    print ('playlists to add', playlists_to_add)

    for sp_playlist_id in playlists_to_add:
        playlist_name, tracks_to_add = a.get_playlist_data(sp_user_id, sp_playlist_id)

        # create playlist object and add to db
        playlist = f.add_playlist_to_db(session['current_user'], sp_playlist_id, playlist_name)

        new_playlists.append(playlist)

        # get data for all the tracks
        sp_tracks = [track_obj['track'] for track_obj in tracks_to_add]
        
        # create string of all the spotify IDs to send to API call
        sp_track_ids = ""
        for sp_track in sp_tracks:
            sp_track_ids += sp_track['id'] + ","
        sp_track_ids = sp_track_ids.rstrip(',')
        
        audio_features = a.get_audio_features_sp(sp_track_ids)
        # make the track object and audio features object into a tuple
        sp_track_info = zip(sp_tracks, audio_features)

        # add each track to database
        for position, track_info in enumerate(sp_track_info):
            # create track object and add to the db
            track = f.add_track_to_db(track_info[0], track_info[1])
            # create PlaylistTrack object and add to the db
            f.add_playlist_track_to_db(playlist, track, position)

    print "All playlists and tracks added"

    return new_playlists


def check_sp_playlist_info(playlist):
    """"""

    # query the db to get the list of playlist track objects for the playlist
    playlist_tracks = f.get_playlist_tracks_db(playlist.playlist_id)

    # get current user's Spotify user ID
    sp_user_id = User.query.get(session['current_user']).sp_user_id

    # send API call to Spotify to get the current tracks in the playlist
    sp_track_ids = a.get_playlist_tracks_sp(sp_user_id, playlist.sp_playlist_id)

    # if sp_tracks is different from the tracks in the db for that playlist
    # ask user if they want to resync from spotify
    changed = False

    # check the length first
    if len(playlist_tracks) != len(sp_track_ids):
        changed = True

    # if the length matches, check each track in order to make sure the tracks are the same
    else:
        for i in range(len(playlist_tracks)):
            if (playlist_tracks[i]).track.sp_track_id != sp_track_ids[i]:
                changed = True
                break

    # if nothing has changed in spotify, return the playlist_tracks list
    if not changed:
        return playlist_tracks

    # otherwise, update the database with the new playlist track info and re-query
    else:
        # find all the tracks in the db currently associated with the playlist that are not in the Spotify list
        playlist_tracks_to_remove = []
        for playlist_track in playlist_tracks:
            if playlist_track.track.sp_track_id not in sp_track_ids:
                playlist_tracks_to_remove.append(playlist_track)
        f.remove_playlist_tracks_db(playlist_tracks_to_remove)
        # update the db with the new tracks and new track positions
        update_playlist_from_sp(playlist.sp_playlist_id, sp_track_ids)
    
    new_playlist_tracks = f.get_playlist_tracks_db(playlist.playlist_id)  
    print "Playlist has been updated"

    return new_playlist_tracks    


def update_playlist_from_sp(sp_playlist_id, sp_track_ids):
    """"Handle adding new tracks from Spotify"""

    tracks_to_add = ""
    playlist_tracks_to_add = []
        # query tracks table to see if it's already in the db
    for sp_track_id in sp_track_ids:
        track_obj = Track.query.filter(Track.sp_track_id == sp_track_id).first()
        pt_obj = db.session.query(PlaylistTrack).join(PlaylistTrack.playlist).join(PlaylistTrack.track).filter(Track.sp_track_id == sp_track_id,
                                                        Playlist.sp_playlist_id == sp_playlist_id).first()
        # if not, add to string of IDs to send
        if not track_obj:
            tracks_to_add += sp_track_id + "," 
        # if the playlist_track object isn't in the db, add to the list to be created
        if not pt_obj:
            playlist_tracks_to_add.append(sp_track_id)

    if tracks_to_add:
        tracks_to_add = tracks_to_add.rstrip(',')
        sp_tracks = a.get_tracks_sp(tracks_to_add)
        audio_features = a.get_audio_features_sp(tracks_to_add)

        f.update_tracks_db(sp_tracks, audio_features)

    f.update_playlist_tracks_db(sp_track_ids, sp_playlist_id, playlist_tracks_to_add)


def update_spotify_tracks(playlist_id):

    sp_user_id = User.query.get(session['current_user']).sp_user_id
    sp_playlist_id = Playlist.query.get(playlist_id).sp_playlist_id
    # query the db to get the list of playlist track objects for the playlist
    new_track_listings = f.get_tracks_in_playlist(playlist_id)

    new_track_ids = ""

    for track in new_track_listings:
        sp_track_id = track.sp_track_id
        new_track_ids += 'spotify:track:' + sp_track_id + ','

    new_track_ids = new_track_ids.rstrip(',')

    response = a.update_playlist_sp(sp_user_id, sp_playlist_id, new_track_ids)

    return response


def mins_secs_to_millisecs(mins_secs):
    """Turn a string formatted as mins:secs to an int representing milliseconds

    >>>mins_secs_to_millisecs('3:45')
    225000

    >>>mins_secs_to_millisecs('4')
    240000

    """

    if ':' in mins_secs:
        mins, secs = mins_secs.split(':')
    else:
        mins = mins_secs
        secs = 0

    return (int(mins) * 60000) + (int(secs) * 1000)


def percent_to_decimal(percentage):
    """Turn a string formatted as a whole number percentage to its decimal equivalent

    >>>percent_to_decimal('50')
    .5

    """

    return float(percentage) / 100
