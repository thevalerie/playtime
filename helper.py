# coding=utf8
from flask import session
import random
from config import client_id, redirect_uri, scope, authorization_base_url
from model import User, Playlist, PlaylistTrack, Track, Category, db
import api_calls as a
import db_functions as f

def get_auth_url():
    """Create the OAuth authorization URL for the current user"""

    # create params to get code from Spotify OAuth
    payload = [('client_id', client_id),
               ('response_type', 'code'),
               ('redirect_uri', redirect_uri),
               ('state', 'ohheythere'),
               ('scope', scope)]

    auth_url = authorization_base_url

    for key, value in payload:
        auth_url += key + '=' + value + '&'

    auth_url = auth_url.rstrip('&')

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

    for sp_playlist_id in playlists_to_add:
        playlist_name, tracks_to_add = a.get_playlist_data(sp_user_id, sp_playlist_id)

        # create playlist object and add to db
        playlist = f.add_playlist_to_db(session['current_user'], sp_playlist_id, playlist_name)

        new_playlists.append(playlist)

        # get data for all the tracks
        sp_tracks = [track_obj['track'] for track_obj in tracks_to_add]

        # create string of all the spotify IDs to send to API call
        sp_track_ids = ','.join(sp_track['id'] for sp_track in sp_tracks)
        
        audio_features = a.get_audio_features_sp(sp_track_ids)
        # make the track object and audio features object into a tuple
        sp_track_info = zip(sp_tracks, audio_features)

        # add each track to database
        for position, track_info in enumerate(sp_track_info):
            # create track object and add to the db
            track = f.add_track_to_db(track_info[0], track_info[1])
            # create PlaylistTrack object and add to the db
            f.add_playlist_track_to_db(playlist, track, position)

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
        pt_obj = f.match_playlist_track_db(sp_track_id, sp_playlist_id)
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

        update_tracks_db(sp_tracks, audio_features)

    f.update_playlist_tracks_db(sp_track_ids, sp_playlist_id, playlist_tracks_to_add)


def update_tracks_db(sp_tracks, audio_features):
    """Add tracks to database from lists of Spotify tracks and corresponding audio features"""

    # for each track that needs to be added, pass the Spotify track data and audio features to the db function
    for i in range(len(sp_tracks)):
        f.add_track_to_db(sp_tracks[i], audio_features[i])


def update_spotify_tracks(playlist_id):
    """Handle updating Spotify with new track order"""

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


def add_spotify_tracks(source_playlist_id, target_playlist_id, track_ids):
    """Handle adding tracks to a Spotify playlist"""

    print('Helper 200 track_ids:', track_ids)

    sp_user_id = User.query.get(session['current_user']).sp_user_id
    sp_playlist_id = Playlist.query.get(target_playlist_id).sp_playlist_id
    import pdb; pdb.set_trace()
    tracks_to_add = f.get_tracks_list(source_playlist_id, track_ids)

    print('Helper 207 tracks_to_add:', tracks_to_add)

    sp_track_ids = ""

    for track in tracks_to_add:
        sp_track_id = track.sp_track_id
        sp_track_ids += 'spotify:track:' + sp_track_id + ','

    sp_track_ids = sp_track_ids.rstrip(',')

    print('Helper 217 sp_track_ids', sp_track_ids)

    response = a.add_tracks_sp(sp_user_id, sp_playlist_id, sp_track_ids)

    return response


def delete_spotify_tracks(playlist_id, track_ids):
    """Handle removing tracks from Spotify playlist"""

    tracks_to_remove = f.get_tracks_list(playlist_id, track_ids)

    sp_track_ids_to_remove = []

    for track in tracks_to_remove:
        sp_track_id = track.sp_track_id
        value = "spotify:track:" + sp_track_id
        sp_track_ids_to_remove.append({"uri": value})

    sp_user_id = User.query.get(session['current_user']).sp_user_id
    sp_playlist_id = Playlist.query.get(playlist_id).sp_playlist_id

    response = a.delete_tracks_sp(sp_user_id, sp_playlist_id, sp_track_ids_to_remove)

    return response


def apply_filter_query(base_query, given_cat):
    """Given a base query and a category object, build a query based on the filter criteria"""
    
    # go through each criterion, if it is specified, add it to the filter
    if given_cat.min_duration_ms:
        base_query = base_query.filter(Track.duration_ms > given_cat.min_duration_ms)
    if given_cat.max_duration_ms:
        base_query = base_query.filter(Track.duration_ms < given_cat.max_duration_ms)
    if given_cat.min_tempo:
        base_query = base_query.filter(Track.tempo > given_cat.min_tempo)
    if given_cat.max_tempo:
        base_query = base_query.filter(Track.tempo < given_cat.max_tempo)
    if given_cat.min_danceability:
        base_query = base_query.filter(Track.danceability > given_cat.min_danceability)
    if given_cat.max_danceability:
        base_query = base_query.filter(Track.danceability < given_cat.max_danceability)
    if given_cat.min_energy:
        base_query = base_query.filter(Track.energy > given_cat.min_energy)
    if given_cat.max_energy:
        base_query = base_query.filter(Track.energy < given_cat.max_energy)
    if given_cat.min_valence:
        base_query = base_query.filter(Track.valence > given_cat.min_valence)
    if given_cat.max_valence:
        base_query = base_query.filter(Track.valence < given_cat.max_valence)
    if given_cat.exclude_explicit:
        base_query = base_query.filter(not Track.is_explicit)

    return base_query


def to_millisecs(mins_secs):
    """Turn a string formatted as mins:secs to an int representing milliseconds

    >>>to_millisecs('3:45')
    225000

    >>>to_millisecs('4')
    240000

    """

    if ':' in mins_secs:
        mins, secs = mins_secs.split(':')
    else:
        mins = mins_secs
        secs = 0

    return (int(mins) * 60000) + (int(secs) * 1000)


def to_decimal(percentage):
    """Turn a string formatted as a whole number percentage to its decimal equivalent

    >>>to_decimal('50')
    .5

    """

    return float(percentage) / 100


def get_category_recommendations(cat_id):
    """Get track recommendations matching a given category ID"""

    recommended_tracks = []

    # first, check the database to see if we already have 20 tracks that match
    given_cat, matches_in_db = f.apply_category_to_all_tracks(cat_id)

    # if the list is 20 tracks long, add the track IDs to the suggested list and return
    # if len(matches_in_db) >= 20:
    #     recommended_tracks.extend(matches_in_db)
    #     return recommended_tracks

    # if we have some matching tracks in the DB, but not enough to recommend,
    # use those tracks as seed data to get more tracks from Spotify
    if matches_in_db:
        seed_tracks = random.sample(matches_in_db, 5)
        seed_track_ids = [track.sp_track_id for track in seed_tracks]
        params = create_recommendation_params(given_cat, seed_track_ids=seed_track_ids)
        sp_tracks = a.get_recommendations_sp(params)

        # create string of all the spotify IDs to send to audio featuresAPI call
        sp_track_ids = ','.join(track['id'] for track in sp_tracks)
        
        audio_features = a.get_audio_features_sp(sp_track_ids)
        # make the track object and audio features object into a tuple
        sp_track_info = zip(sp_tracks, audio_features)

        # add each track to database
        for track_info in sp_track_info:
            # create track object and add to the db
            track = f.add_track_to_db(track_info[0], track_info[1])
            recommended_tracks.append(track)

        return given_cat, recommended_tracks


def create_recommendation_params(category_object, seed_artist_ids=None, seed_genre_ids=None, seed_track_ids=None):
    """Given a category object and seed data, construct parameters for Spotify get request"""

    # get all the category's attributes make a dict of just the ones we need
    category_attrs = category_object.to_dict()
    extra_attrs = ('cat_id', 'cat_name', 'user_id', 'exclude_explicit')
    params = {key: value for key, value in category_attrs.iteritems()
                      if key not in extra_attrs and value is not None}

    # code to handle seeding with artists and/or genres

    # if seed_artist_ids:
    #     seed_artists = ','.join(seed_artist_ids)
    #     params['seed_artists'] = seed_artists

    # if seed_genre_ids:
    #     seed_genres = ','.join(seed_genre_ids)
    #     params['seed_genres'] = seed_genres

    if seed_track_ids:
        seed_tracks = ','.join(seed_track_ids)
        params['seed_tracks'] = seed_tracks

    return params
