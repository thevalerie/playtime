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
from model import User, Playlist, PlaylistTrack, Track, connect_to_db, db


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


@app.route('/get_db_playlists.json')
def query_db_for_user_playlists():
    """Add a comment?"""

    db_playlists = f.get_user_playlists()

    # make a list of dicts with just the id and name
    playlist_data = [{'playlist_id': playlist.playlist_id, 'name': playlist.name} for playlist in db_playlists]

    return jsonify(playlist_data)


@app.route('/get_sp_playlists.json')
def query_sp_for_user_playlists():
    """Add a comment?"""

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

    # query database to get the playlist info
    playlist = Playlist.query.get(playlist_id)

    # check Spotify to see if the user has changed the playlist since they last logged in
    playlist_tracks = h.check_sp_playlist_info(playlist)

    return render_template('playlist.html', playlist=playlist,
                           playlist_tracks=playlist_tracks,
                           format_time=h.millisecs_to_mins_secs)


@app.route('/reorder', methods=['POST'])
def update_playlist_in_db():
    """Update the track order of a playlist in the database"""

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


@app.route('/my_filters')
def view_filters():
    """Display current user's song filters"""

    filters = f.get_user_filters_db()

    return render_template('user-filters.html', filters=filters)


@app.route('/create_filter')
def create_new_filter():
    """UI for user to create a new filter"""

    return render_template('create_filter.html')


@app.route('/create_filter', methods=['POST'])
def add_filter_to_db():
    """Create a new filter, add to the db"""

    filter_data = {key: (value if value else None) for key, value in request.form.iteritems()}
    filter_data['user_id'] = session['current_user']
    filter_data['explicit'] = not filter_data.get('explicit')

    f.add_filter_to_db(filter_data)

    # redirect back to the user filters page
    return redirect('/my_filters')


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
