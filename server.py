# coding=utf8
from jinja2 import StrictUndefined
from flask_debugtoolbar import DebugToolbarExtension
from flask import (Flask, render_template, redirect, request, flash, session, url_for)
import sys
import requests
import config as c
import api_calls as a
import functions as f
from model import User, Playlist, PlaylistTrack, Track, connect_to_db, db
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

    # if 'access_token' not in session:
    oauth = a.create_oauth()
    authorization_url, state = a.get_auth_url(oauth)
    session['state'] = state

    # can try to refactor using requests library instead of OAuth object
    # paylod = {'client_id': client_id,
    #           'response_type': 'code'
    #           'redirect_uri': redirect_uri,
                # 'state': 'ohheythere'
    #           'scope': scope,}

    # response = requests.get(authorization_base_url, payload)

    return render_template("homepage.html", authorization_url=authorization_url)


@app.route('/login')
def log_in():
    """Return path after user logs in to Spotify"""

    # import pdb; pdb.set_trace()

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
        return response_error(response.status_code)

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
    sp_user_id, display_name = a.get_user_profile(c.user_profile_url)
    # check to see if the current user is in the db/add if not
    current_user = f.check_db_for_user(sp_user_id, display_name)
    # add current user id to session
    f.add_user_to_session(current_user)

    spotify_playlists = a.get_user_playlists(c.user_playlists_url)

    playlists = Playlist.query.filter(Playlist.user_id == current_user.user_id).all()

    return render_template("profile-page.html",
                           user=current_user,
                           playlists=playlists,
                           spotify_playlists=spotify_playlists,)


@app.route('/add_playlists', methods=['POST'])
def add_playlists_to_db():
    """Pull in playlists from Spotify and add the relevant information to the DB"""

    # get the playlists checked in the add playlists form
    playlists_to_add = request.form.getlist('sp_playlists')
    sp_user_id = User.query.get(session['current_user']).sp_user_id
    
    print playlists_to_add

    # send API call to get the playlist info
    for sp_playlist_id in playlists_to_add:
        playlist_name, tracks_to_add = a.get_playlist_data(sp_user_id, sp_playlist_id)
        print tracks_to_add

        # create playlist object and add to db
        playlist = f.add_playlist_to_db(session['current_user'], sp_playlist_id, playlist_name)

        # get data for each track & add to database
        for position, track_obj in enumerate(tracks_to_add):

            sp_track = track_obj['track']
            sp_track_id = sp_track['id']

            # get audio features info from Spotify
            audio_features = a.get_track_data(sp_track_id)
            print audio_features
            
            # create track object and add to the db
            track = f.add_track_to_db(sp_track, audio_features)


            # create PlaylistTrack object and add to the db
            f.add_playlist_track_to_db(playlist, track, position)
  
    # redirect back to the user profile page
    return redirect('/profile')


@app.route('/playlist/<playlist_id>')
def work_on_playlist(playlist_id):
    """View a selected playlist"""

    # query database to get the playlist info and list of tracks in the playlist
    playlist = Playlist.query.get(playlist_id)
    playlist_tracks = PlaylistTrack.query.filter(PlaylistTrack.playlist_id == playlist_id).all()

    # send API call to Spotify to see if the tracks in the playlist have changed
    sp_user_id = User.query.get(session['current_user']).sp_user_id
    sp_tracks = a.get_playlist_tracks(sp_user_id, playlist.sp_playlist_id)
    print sp_tracks

    # if sp_tracks is different from the tracks in the db for that playlist
    # ask user if they want to resync from spotify, 

    return render_template('playlist.html', playlist=playlist, playlist_tracks=playlist_tracks)


#################Helper functions######################

def response_error(status_code):
    """Status code error messaging"""

    return render_template('error-page.html', status_code=status_code)


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
