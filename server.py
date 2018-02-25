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
# from api_calls import (create_oauth, get_auth_url, get_token, get_user_profile,
#                        get_user_playlists, get_playlist_data, get_track_data,
#                        get_playlist_tracks)
# from functions import (check_db_for_user, add_track_to_db,)

app = Flask(__name__)
app.secret_key = "ABC"
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def homepage():
    """Homepage"""

    if 'access_token' in session:
        return redirect('/profile')

    session['state'] = 'ohheythere'

    authorization_url = a.get_auth_url()

    return render_template("homepage.html", authorization_url=authorization_url)


@app.route('/login')
def log_in():
    """Return path after user logs in to Spotify"""

    # retrieve code and state from the return value from the OAuth
    code = request.args.get('code')
    state = request.args.get('state')

    # if the value for state doesn't match what's in the session,
    # redirect back to homepage and try login again
    if state != session['state']:
        flash("Authentication failed, please try again")
        return redirect('/')

    response = a.get_token(code)
    # if anything other than a 200 response code, call error message func
    if response.status_code != 200:
        return h.response_error(response.status_code)

    # if success, save the access token and refresh token to the session
    token = response.json()
    session['access_token'] = token['access_token']
    session['refresh_token'] = token['refresh_token']
    print "Added to session: access_token", session['access_token']
    print "Added to session: refresh_token", session['refresh_token']

    return redirect('/profile')


@app.route('/profile')
def view_user_profile():
    """View current user profile page"""
    
    # get the Spotify user profile
    sp_user_id, display_name = a.get_user_profile()
    # check to see if the current user is in the db/add if not
    current_user = f.check_db_for_user(sp_user_id, display_name)
    # add current user id to session
    h.add_user_to_session(current_user)

    return render_template("profile-page.html",
                           user=current_user)


@app.route('/my_playlists')
def view_user_playlists():
    """View current user's playlists in the database/import more from Spotify"""

    return render_template("my_playlists.html")


@app.route('/get_db_playlists.json')
def query_db_for_user_playlists():
    
    db_playlists = f.get_user_playlists()

    # make a list of dicts with just the id and name
    playlist_data = [{ 'playlist_id': playlist.playlist_id, 'name': playlist.name} for playlist in db_playlists]

    return jsonify(playlist_data)


@app.route('/get_sp_playlists.json')
def query_sp_for_user_playlists():

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

    print ('new playlists in route:', new_playlists)

    playlist_data = [{playlist.playlist_id: playlist.name} for playlist in new_playlists]
    print ('playlist data:', playlist_data)
  
    # redirect back to the user profile page
    return jsonify(playlist_data)


@app.route('/playlist/<playlist_id>')
def work_on_playlist(playlist_id):
    """View a selected playlist"""

    # query database to get the playlist info
    playlist = Playlist.query.get(playlist_id)

    # check Spotify to see if the user has changed the playlist since they last logged in
    playlist_tracks = h.check_sp_playlist_info(playlist)

    # get the current user's filters from the db
    user_categories = f.get_user_categories_db()

    return render_template('playlist.html', playlist=playlist, 
                           playlist_tracks=playlist_tracks,
                           user_categories=user_categories,
                           format_time=h.millisecs_to_mins_secs,
                           format_explicit=h.view_is_explicit,)


@app.route('/reorder', methods=['POST'])
def update_playlist_in_db():
    """Update the track order of a playlist in the database"""

    # playlist_id = request.form.get('playlist_id')
    new_track_order = json.loads(request.form.get('new_track_order'))
    f.update_track_order(new_track_order)

    return 'Successfully updated playlist in DB'


@app.route('/push_to_spotify', methods=['POST'])
def update_playlist_in_spotify():
    """Push playlist changes to Spotify"""

    playlist_id = request.form.get('playlist_id')

    h.update_spotify_tracks(playlist_id)

    return 'Successfully updated playlist in Spotify'


@app.route('/more_playlists')
def load_more_playlists():
    """Load & display more playlists from Spotify"""

    offset = request.args.get('offset')

    more_playlists = a.get_user_playlists(offset=offset)


@app.route('/my_categories')
def view_categories():
    """Display current user's song categories"""

    categories = f.get_user_categories_db()

    return render_template('user-categories.html', categories=categories)


@app.route('/create_category')
def create_new_category():
    """UI for user to create a new category"""
  
    return render_template('create_category.html')


@app.route('/create_category', methods=['POST'])
def add_category_to_db():
    """Create a new category, add to the db"""

    category_data = {key: (value if value else None) for key, value in request.form.iteritems()}
    category_data['user_id'] = session['current_user']
    category_data['exclude_explicit'] = category_data.get('exclude_explicit')

    f.add_category_to_db(category_data)
  
    # redirect back to the user categories page
    return redirect('/my_categories')


@app.route('/check_category.json')
def match_tracks_to_category():
    """Finds the tracks that match the selected categoy"""

    cat_info = request.json

    cat_id = request.args.get('cat_id')
    playlist_id = request.args.get('playlist_id')

    track_list = f.get_tracks_in_playlist(playlist_id)

    selected_cat, matching_tracks = h.apply_category(cat_id, track_list)

    print matching_tracks

    track_ids = [track.track_id for track in matching_tracks]

    return jsonify({'matchingTracks': track_ids, 'cagegoryName': selected_cat.cat_name})


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
