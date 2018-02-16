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


def update_track_order(new_track_order):
    """Get the PlaylistTrack object from the database and update its position"""

    updated_pt_objects = []

    for pt_id, new_position in new_track_order.iteritems():
        playlist_track = PlaylistTrack.query.get(int(pt_id))
        playlist_track.position = (int(new_position))
        updated_pt_objects.append(playlist_track)

    db.session.commit()

    print "Updated in DB:", updated_pt_objects


def get_playlist_tracks_db(playlist_id):
    """Get the track IDs for a given playlist, in position order"""

    playlist_tracks = PlaylistTrack.query.filter(PlaylistTrack.playlist_id == playlist_id,
                                                 PlaylistTrack.position != None).order_by(PlaylistTrack.position).all()

    return playlist_tracks


def remove_playlist_tracks_db(playlist_tracks_to_remove):
    """"""

    for playlist_track in playlist_tracks_to_remove:
        playlist_track.position = None

    db.session.commit()

    print "Removed tracks from playlist"


def update_tracks_db(sp_tracks, audio_features):
    """"""

    # for each track that needs to be added, pass the Spotify track data and audio features to the db function
    for i in range(len(sp_tracks)):
        sp_track = sp_tracks[i]
        audio_features = audio_features[i]
        add_track_to_db(sp_track, audio_features)


def update_playlist_tracks_db(sp_track_ids, sp_playlist_id, playlist_tracks_to_add):

    for i, sp_track_id in enumerate(sp_track_ids):
        # check to see if the track & playlist combo is in the pt table
        # if not, add
        if sp_track_id in playlist_tracks_to_add:
            playlist = db.session.query(Playlist).filter(Playlist.sp_playlist_id == sp_playlist_id).first()
            track = db.session.query(Track).filter(Track.sp_track_id == sp_track_id).first()
            position = i
            add_playlist_track_to_db(playlist, track, position)
        # if it's already in the db, check position against sp data and update if necessary
        else:
            playlist_track = db.session.query(PlaylistTrack).join(PlaylistTrack.playlist).join(PlaylistTrack.track).filter(Track.sp_track_id == sp_track_id,
                                                        Playlist.sp_playlist_id == sp_playlist_id).first()
            if playlist_track.position != i:
                playlist_track.position = i


def get_tracks_in_playlist(playlist_id):
    """Takes a playlist ID, returns a list of track objects in that playlist"""

    tracks_in_playlist = db.session.query(Track).join(PlaylistTrack).filter(PlaylistTrack.playlist_id == playlist_id,
                                                                            PlaylistTrack.position != None).order_by(PlaylistTrack.position).all()
    
    print tracks_in_playlist

    return tracks_in_playlist





