# coding=utf8
from flask import session
from model import User, Playlist, PlaylistTrack, Track, Category, db
import api_calls as a
import helper as h

################################################################################
#############################Users table functions##############################
################################################################################

#Add rows to users table

def add_user_to_db(sp_user_id, display_name):
    """Add the current user to the db"""

    current_user = User(sp_user_id=sp_user_id, display_name=display_name)
    db.session.add(current_user)
    db.session.commit()

    print "Added to DB:", current_user

    return current_user


#Query users table

def check_db_for_user(sp_user_id, display_name):
    """Check to see if the current user is in the db"""

    # find the user object in the database with the spotify user ID
    current_user = User.query.filter(User.sp_user_id == sp_user_id).first()

    # add to the db if it's not already there
    if not current_user:
        current_user = add_user_to_db(sp_user_id, display_name)

    return current_user


################################################################################
###########################Playlists table functions############################
################################################################################

#Add rows to playlists table

def add_playlist_to_db(user_id, sp_playlist_id, playlist_name):
    """Add a playlist to database"""

    playlist = Playlist(user_id=user_id, sp_playlist_id=sp_playlist_id, name=playlist_name)
    db.session.add(playlist)
    db.session.commit()

    print "Added to DB:", playlist

    return playlist


#Query playlists table

def get_playlist_info_db(playlist_id):
    """Given playlist ID, return Playlist object"""

    return Playlist.query.get(playlist_id)


def get_user_playlists():
    """Get playlists associated with the current user"""

    playlists = db.session.query(Playlist).filter(Playlist.user_id == session['current_user']).limit(20).all()

    return playlists


################################################################################
#############################Tracks table functions#############################
################################################################################

#Add rows to tracks table

def add_track_to_db(sp_track, audio_features):
    """Create Track object, add to database"""

    sp_track_id = sp_track['id']
    duration_ms = sp_track['duration_ms']
    album = sp_track['album']['name']
    is_explicit = sp_track['explicit']
    title = sp_track['name']
    artist = ', '.join(artist['name'] for artist in sp_track['artists'])
    tempo = int(round(audio_features['tempo']))
    danceability = audio_features['danceability']
    energy = audio_features['energy']
    valence = audio_features['valence']

    track = Track(sp_track_id=sp_track_id, title=title, artist=artist, album=album,
                  duration_ms=duration_ms, tempo=tempo, danceability=danceability,
                  energy=energy, is_explicit=is_explicit, valence=valence,)

    db.session.add(track)
    db.session.commit()

    print "Added to DB:", track

    return track


#Query tracks table

def get_user_tracks_db():
    """Returns a set of tracks in the database for the current user"""

    user_tracks = db.session.query(Track).join(PlaylistTrack.track).join(
                  PlaylistTrack.playlist).filter(Playlist.user_id == session['current_user']).all()

    return set(user_tracks)


def get_tracks_in_playlist(playlist_id):
    """Takes a playlist ID, returns a list of track objects in that playlist"""

    tracks_in_playlist = db.session.query(Track).join(PlaylistTrack).filter(
        PlaylistTrack.playlist_id == playlist_id, PlaylistTrack.position != None).order_by(
        PlaylistTrack.position).all()

    return tracks_in_playlist


def get_tracks(lst_track_ids):
    """Takes a list of track IDs, returns a list of corresponding track objects"""

    tracks = db.session.query(Track).filter(Track.track_id.in_(lst_track_ids)).all()

    return tracks


def get_tracks_list(lst_track_ids):
    """Given list of track IDs, get the corresponding Track objects"""

    tracks = db.session.query(Track).filter(Track.track_id.in_(lst_track_ids)).all()

    return tracks


def apply_category_to_playlist_db(cat_id, playlist_id):
    """Given a category ID and playlist ID, return tracks in that playlist that match the category criteria"""

    given_cat = get_category_info_db(cat_id)

    # base_query
    base_query = db.session.query(Track).join(PlaylistTrack).filter(
                 PlaylistTrack.playlist_id == playlist_id, PlaylistTrack.position != None)

    tracks_in_category = (h.apply_filter_query(base_query, given_cat)).all()

    return given_cat, tracks_in_category


def apply_category_to_user_db(cat_id):
    """Given a category ID, return all tracks in the current user's playlists that match"""

    given_cat = get_category_info_db(cat_id)

    # base_query
    base_query = db.session.query(Track).join(PlaylistTrack.track).join(PlaylistTrack.playlist).filter(
                 Playlist.user_id == session['current_user'], PlaylistTrack.position != None)

    tracks_in_category = (h.apply_filter_query(base_query, given_cat)).all()

    return given_cat, tracks_in_category


def apply_category_to_all_tracks(cat_id):
    """Given a category ID, return all tracks in the DB that match (batches of 20)"""

    given_cat = get_category_info_db(cat_id)

    base_query = db.session.query(Track)

    tracks_in_category = (h.apply_filter_query(base_query, given_cat)).all()

    return given_cat, tracks_in_category


################################################################################
#########################PlaylistTracks table functions#########################
################################################################################

#Add rows to playlistTracks table

def add_playlist_track_to_db(playlist, track, position):
    """Create PlaylistTrack object, add to database"""

    playlist_track = PlaylistTrack(playlist_id=playlist.playlist_id,
                                   track_id=track.track_id,
                                   position=position,)
    db.session.add(playlist_track)
    db.session.commit()

    return playlist_track


#Edit rows in playlistTracks table

def update_track_order(new_track_order):
    """Given a list of PlaylistTrack object in order, update their positions"""

    updated_pt_objects = []

    for pt_id, new_position in new_track_order.iteritems():
        playlist_track = PlaylistTrack.query.get(int(pt_id))
        playlist_track.position = (int(new_position))
        updated_pt_objects.append(playlist_track)

    db.session.commit()

    print "Updated in DB:", updated_pt_objects


def update_playlist_tracks_db(sp_track_ids, sp_playlist_id, playlist_tracks_to_add):
    """Update PlaylistTrack objects in DB based on changes to playlist in Spotify"""

    for i, sp_track_id in enumerate(sp_track_ids):
        # check to see if the PlaylistTrack needs to be added to the DB
        if sp_track_id in playlist_tracks_to_add:
            playlist = db.session.query(Playlist).filter(Playlist.sp_playlist_id == sp_playlist_id).first()
            track = db.session.query(Track).filter(Track.sp_track_id == sp_track_id).first()
            add_playlist_track_to_db(playlist, track, i)
        # if it's already in the db, check position against sp data and update if necessary
        else:
            playlist_track = match_playlist_track_db(sp_track_id, sp_playlist_id)
            if playlist_track.position != i:
                playlist_track.position = i


def remove_playlist_tracks_db(playlist_tracks_to_remove):
    """Remove tracks from a playlist"""

    for playlist_track in playlist_tracks_to_remove:
        playlist_track.position = None

    db.session.commit()


#Query playlistTracks table

def get_playlist_tracks_db(playlist_id):
    """Get the PlaylistTrack objects for a given playlist, in position order"""

    playlist_tracks = db.session.query(PlaylistTrack).filter(PlaylistTrack.playlist_id == playlist_id).filter(
                      PlaylistTrack.position != None).order_by(PlaylistTrack.position).all()

    return playlist_tracks


def match_playlist_track_db(sp_track_id, sp_playlist_id):
    """Given Spotify playlist ID and track ID, get the corresponding PlaylistTrack object from the DB if it exists"""

    playlist_track = db.session.query(PlaylistTrack).join(PlaylistTrack.playlist).join(PlaylistTrack.track).filter(
                     Track.sp_track_id == sp_track_id, Playlist.sp_playlist_id == sp_playlist_id).first()

    return playlist_track


################################################################################
###########################Categories table functions###########################
################################################################################

#Add rows to categories table

def add_category_to_db(category_data):
    """Create Category object, add to database"""

    if category_data.get('min_duration_ms'):
        category_data['min_duration_ms'] = h.to_millisecs(category_data['min_duration_ms'])   
    if category_data.get('max_duration_ms'):
        category_data['max_duration_ms'] = h.to_millisecs(category_data['max_duration_ms'])
    if category_data.get('min_danceability'):
        category_data['min_danceability'] = h.to_decimal(category_data['min_danceability'])
    if category_data.get('max_danceability'):
        category_data['max_danceability'] = h.to_decimal(category_data['max_danceability'])
    if category_data.get('min_energy'):
        category_data['min_energy'] = h.to_decimal(category_data['min_energy'])
    if category_data.get('max_energy'):
        category_data['max_energy'] = h.to_decimal(category_data['max_energy'])
    if category_data.get('min_valence'):
        category_data['min_valence'] = h.to_decimal(category_data['min_valence'])
    if category_data.get('max_valence'):
        category_data['max_valence'] = h.to_decimal(category_data['max_valence'])
    if category_data.get('exclude_explicit'):
        category_data['exclude_explicit'] = True

    new_category = Category(**category_data)

    db.session.add(new_category)
    db.session.commit()

    print "Added to DB:", new_category

    return new_category


#Query categories table

def get_category_info_db(cat_id):
    """Given category ID, return Category object"""

    return Category.query.get(cat_id)


def get_user_categories_db():
    """Gets the list of categories in the database for the current user"""

    user_categories = Category.query.filter(Category.user_id == session['current_user']).all()

    return user_categories
