# coding=utf8
from flask import (Flask, request, session)
import sys
import requests
import config
from model import User, Playlist, PlaylistTrack, Track, connect_to_db, db
import api_calls as a


def check_db_for_user(sp_user_id, display_name):
    """Check to see if the current user is in the db"""

    # find the user object in the database with the spotify user ID
    current_user = User.query.filter(User.sp_user_id == sp_user_id).first()

    # add to the db if it's not already there
    if not current_user:
        current_user = add_user_to_db(sp_user_id, display_name)

    return current_user


def add_user_to_db(sp_user_id, display_name):
    """Add the current user to the db"""

    current_user = User(sp_user_id=sp_user_id, display_name=display_name)
    db.session.add(current_user)
    db.session.commit()

    print "Added to DB:", current_user

    return current_user


def add_user_to_session(current_user):
    """Add the current user id to the session"""

    session['current_user'] = current_user.user_id

    print "Added to session: current_user", session['current_user']


def add_playlist_to_db(user_id, sp_playlist_id, playlist_name):
    """Add a playlist to database"""

    playlist = Playlist(user_id=user_id, sp_playlist_id=sp_playlist_id, name=playlist_name)
    db.session.add(playlist)
    db.session.commit()

    print "Added to DB:", playlist

    return playlist


def add_track_to_db(sp_track, audio_features):
    """Create Track object, add to database"""

    sp_track_id = sp_track['id']
    duration =  sp_track['duration_ms']
    album = sp_track['album']['name']
    explicit = sp_track['explicit']
    title = sp_track['name']
    artist = ', '.join(artist['name'] for artist in sp_track['artists'])
    tempo = int(round(audio_features['tempo']))
    danceability = audio_features['danceability']
    energy = audio_features['energy']
    valence = audio_features['valence']

    track = Track(sp_track_id=sp_track_id, title=title, artist=artist, album=album,
                  duration=duration, tempo=tempo, danceability=danceability,
                  energy=energy, explicit=explicit, valence=valence,)

    db.session.add(track)
    db.session.commit()

    print "Added to DB:", track

    return track


def add_playlist_track_to_db(playlist, track, position):
    """Create PlaylistTrack object, add to database"""

    playlist_track = PlaylistTrack(playlist_id=playlist.playlist_id,
                                           track_id=track.track_id,
                                           position=position,)
    db.session.add(playlist_track)
    db.session.commit()


