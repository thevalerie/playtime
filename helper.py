# coding=utf8
from flask import (Flask, request, session)
import sys
import requests
import config as c
import api_calls as a
import db_functions as f
from model import User, Playlist, PlaylistTrack, Track, Category, connect_to_db, db
# import api_calls as a


def add_user_to_session(current_user):
    """Add the current user id to the session"""

    session['current_user'] = current_user.user_id

    print "Added to session: current_user", session['current_user']


def response_error(status_code):
    """Status code error messaging"""

    return render_template('error-page.html', status_code=status_code)


def import_user_playlists(sp_user_id, playlists_to_add):
    """send API call to get the playlist info, add playlist and track info to the db"""

    new_playlists = []
    print ('playlists to add', playlists_to_add)

    for sp_playlist_id in playlists_to_add:
        playlist_name, tracks_to_add = a.get_playlist_data(sp_user_id, sp_playlist_id)
        print tracks_to_add

        # create playlist object and add to db
        playlist = f.add_playlist_to_db(session['current_user'], sp_playlist_id, playlist_name)

        print playlist

        new_playlists.append(playlist)

        # get data for each track & add to database
        for position, track_obj in enumerate(tracks_to_add):

            sp_track = track_obj['track']
            sp_track_id = sp_track['id']

            # get audio features info from Spotify
            audio_features = a.get_track_data(sp_track_id)
            # create track object and add to the db
            track = f.add_track_to_db(sp_track, audio_features)
            # create PlaylistTrack object and add to the db
            f.add_playlist_track_to_db(playlist, track, position)

    print "All playlists and tracks added"
    print ('new playlists from helper function', new_playlists)

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

    result = a.update_playlist_sp(sp_user_id, sp_playlist_id, new_track_ids)

    print result


def mins_secs_to_millisecs(mins_secs):
    """Turn a string formatted as mins:secs to an int representing milliseconds"""

    if ':' in mins_secs:
        mins, secs = mins_secs.split(':')
    else:
        mins = mins_secs
        secs = 0

    return (int(mins) * 60000) + (int(secs) * 1000)


def millisecs_to_mins_secs(milliseconds):
    """Turn an int representing a length of time in milliseconds to a string in the format mins:secs"""

    mins = milliseconds / 60000
    secs = (milliseconds % 60000) / 1000

    if secs < 10:
        return str(mins) + ':0' + str(secs)
    else:
        return str(mins) + ':' + str(secs)


def view_is_explicit(is_explicit):
    """Takes the boolean value of playlist.is_explicit and returns a descriptive string"""

    if is_explicit:
        return "Explicit"
    else:
        return ""


def apply_category(cat_id, track_list):
    """Given a category ID and a list of track objects, return a list of tracks that match the category"""

    given_cat = Category.query.get(cat_id)
    tracks_in_category = []

    # check the track against each criterion in the category, if it passes all, add to the list
    for track in track_list:
        if track.duration < given_cat.duration_min:
            continue
        if given_cat.duration_max and (track.duration > given_cat.duration_max):
            continue
        if track.tempo < given_cat.tempo_min:
            continue
        if given_cat.tempo_max and (track.tempo > given_cat.tempo_max):
            continue
        if track.danceability < given_cat.danceability_min:
            continue
        if given_cat.danceability_max and (track.danceability > given_cat.danceability_max):
            continue
        if track.energy < given_cat.energy_min:
            continue
        if given_cat.energy_max and (track.energy > given_cat.energy_max):
            continue
        if track.valence < given_cat.valence_min:
            continue
        if given_cat.valence_max and (track.valence > given_cat.valence_max):
            continue
        if given_cat.exclude_explicit and track.is_explicit:
            continue
        tracks_in_category.append(track)

    return given_cat, tracks_in_category





