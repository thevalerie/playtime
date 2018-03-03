# coding=utf8
from jinja2 import StrictUndefined
from flask_debugtoolbar import DebugToolbarExtension
from flask import (Flask, render_template, redirect, request, flash, session, jsonify)
import json
import sys
import requests
import config as c
import api_calls as a
import db_functions as f
import helper as h
from model import User, Playlist, PlaylistTrack, Track, Category, connect_to_db, db

app = Flask(__name__)
app.secret_key = "ABC"
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def homepage():
    """Homepage"""

    if 'access_token' in session:
        return redirect('/profile')

    session['state'] = 'ohheythere'

    authorization_url = h.get_auth_url()

    return render_template("homepage.html", authorization_url=authorization_url)


@app.route('/login')
def log_in():
    """Return path after user logs in to Spotify"""

    # retrieve code and state from the return value from the OAuth
    code = request.args.get('code')
    state = request.args.get('state')

    status_code = h.authenticate_user(code, state)

    # get the Spotify user profile
    sp_user_id, display_name = a.get_user_profile()
    # check to see if the current user is in the db/add if not
    current_user = f.check_db_for_user(sp_user_id, display_name)
    # add current user id to session
    h.add_user_to_session(current_user)

    if status_code != 200:
        return render_template('error-page.html', status_code=status_code)
    else:
        return redirect('/profile')


@app.route('/log_out')
def log_out():
    """Remove user and tokens from session, redirect to homepage"""

    session.clear()

    return redirect(c.log_out_url)


@app.route('/profile')
def view_user_profile():
    """View current user profile page"""

    if 'current_user' not in session:
        return redirect('/')

    current_user = User.query.get(session['current_user'])

    return render_template("profile-page.html", user=current_user)


@app.route('/my_playlists')
def view_user_playlists():
    """View current user's playlists in the database/import more from Spotify"""

    if 'current_user' not in session:
        return redirect('/')

    return render_template("my_playlists.html")


@app.route('/get_db_playlists.json')
def query_db_for_user_playlists():
    """Get all Playlist objects in the DB belonging to the current user"""
        
    db_playlists = f.get_user_playlists()

    # make a list of dicts with just the id and name
    playlist_data = [{'playlist_id': playlist.playlist_id, 'name': playlist.name} for playlist in db_playlists]

    return jsonify(playlist_data)


@app.route('/get_sp_playlists.json')
def query_sp_for_user_playlists():
    """Get all playlists from Spotify belonging to the current user"""

    spotify_playlists = a.get_user_playlists()

    return jsonify(spotify_playlists)


@app.route('/add_playlists.json', methods=['POST'])
def add_playlists_to_db():
    """Pull in playlists from Spotify and add the relevant information to the DB"""
    
    # get the playlists that the user selected in the add playlists form
    playlists_to_add = request.json
    sp_user_id = User.query.get(session['current_user']).sp_user_id

    # send API call to get the playlist info,
    # add playlist and track info to the db
    new_playlists = h.import_user_playlists(sp_user_id, playlists_to_add)

    playlist_data = [{playlist.playlist_id: playlist.name} for playlist in new_playlists]
    
    # redirect back to the user profile page
    return jsonify(playlist_data)


@app.route('/playlist/<playlist_id>')
def work_on_playlist(playlist_id):
    """View a selected playlist"""

    if 'current_user' not in session:
        return redirect('/')

    # query database to get the playlist info
    playlist = Playlist.query.get(playlist_id)

    # check Spotify to see if the user has changed the playlist since they last logged in
    playlist_tracks = h.check_sp_playlist_info(playlist)

    # get the current user's filters from the db
    user_categories = f.get_user_categories_db()

    return render_template('playlist.html', playlist=playlist,
                           playlist_tracks=playlist_tracks,
                           user_categories=user_categories)          


@app.route('/reorder.json', methods=['POST'])
def update_playlist_in_db():
    """Update the track order of a playlist in the database"""

    new_track_order = json.loads(request.form.get('new_track_order'))

    f.update_track_order(new_track_order)

    return 'Successfully updated playlist in DB'


@app.route('/push_to_spotify.json', methods=['POST'])
def update_playlist_in_spotify():
    """Push playlist changes to Spotify"""

    playlist_id = request.form.get('playlist_id')

    response = h.update_spotify_tracks(playlist_id)

    return 'Updated playlist response:' + str(response)


@app.route('/more_playlists')
def load_more_playlists():
    """Load & display more playlists from Spotify"""

    offset = request.args.get('offset')

    more_playlists = a.get_user_playlists(offset=offset)


@app.route('/my_categories')
def view_categories():
    """Display current user's song categories"""

    if 'current_user' not in session:
        return redirect('/')

    categories = f.get_user_categories_db()

    return render_template('my_categories.html', categories=categories)


@app.route('/create_category.json', methods=['POST'])
def add_category_to_db():
    """Create a new category, add to the db"""

    category_data = {key: (value if value else None) for key, value in request.form.iteritems()}
    category_data['user_id'] = session['current_user']
    category_data['exclude_explicit'] = category_data.get('exclude_explicit')

    f.add_category_to_db(category_data)
  
    # redirect back to the user categories page
    return 'Success!'


@app.route('/check_category.json')
def match_tracks_to_category():
    """Finds the tracks that match the selected categoy"""

    cat_id = request.args.get('cat_id')
    playlist_id = request.args.get('playlist_id')

    selected_cat, matching_tracks = f.apply_category_to_playlist_db(cat_id, playlist_id)

    track_ids = [track.track_id for track in matching_tracks]

    return jsonify({'matchingTracks': track_ids, 'categoryName': selected_cat.cat_name})


@app.route('/get_recommendations')
def category_recommendations():

    cat_id = request.args.get('cat_id')

    category, recommended_tracks = h.get_category_recommendations(cat_id)

    return render_template('/recommendations.html', category=category, 
                                   recommended_tracks=recommended_tracks)


@app.route('/delete_tracks_playlist', methods=['POST'])
def delete_tracks_from_playlist():

    playlist_id = request.form.get('playlist_id')
    track_ids = request.form.getlist('track_ids[]')

    h.delete_spotify_tracks(playlist_id, track_ids)

    return jsonify(playlist_id)


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
