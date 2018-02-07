from jinja2 import StrictUndefined
from requests_oauthlib import OAuth2Session
from flask_debugtoolbar import DebugToolbarExtension
from flask import (Flask, render_template, redirect, request, flash, session, url_for)
import os
import sys
import requests
from model import User, connect_to_db, db

app = Flask(__name__)
app.secret_key = "ABC"
app.jinja_env.undefined = StrictUndefined

authorization_base_url = 'https://accounts.spotify.com/authorize/'
token_url = 'https://accounts.spotify.com/api/token'
client_id = os.environ['SPOTIFY_CONSUMER_KEY']
client_secret=os.environ['SPOTIFY_CONSUMER_SECRET']
redirect_uri = 'http://localhost:5000/login'
scope = ['user-read-private']

# create OAuth2 object
oauth = OAuth2Session(client_id=client_id, redirect_uri=redirect_uri,
                      scope=scope)

@app.route('/')
def homepage():
    """Homepage"""

    # if 'access_token' not in session:

    authorization_url, state = oauth.authorization_url(authorization_base_url)
    session[state] = state

    # can try to refactor using requests library instead of OAuth object
    # paylod = {'client_id': client_id,
    #           'response_type': 'code'
    #           'redirect_uri': redirect_uri,
    #           'scope': scope,}

    # response = requests.get(authorization_base_url, payload)

    return render_template("homepage.html", authorization_url=authorization_url)


@app.route('/login')
def log_in():
    """Log in using OAuth"""

    code = request.args.get('code')
    state = request.args.get('state')

    payload = {'grant_type': 'authorization_code',
               'code': code,
               'redirect_uri': redirect_uri,
               'client_id': client_id,
               'client_secret': client_secret,}

    response = requests.post(token_url, payload)
    # need to put some code in here for if I get an error message back
    token = response.json()
    session['access_token'] = token['access_token']

    return redirect('/profile')


@app.route('/profile')
def display_profile():
    """User profile page"""

    headers = {'Authorization': 'Bearer ' + session['access_token']}

    response = requests.get('https://api.spotify.com/v1/me', headers=headers)

    spotify_user = response.json()
    sp_user_id = spotify_user['id']
    display_name = spotify_user['display_name']

    # find the user object in the database with the spotify user ID
    current_user = User.query.filter(User.sp_user_id == sp_user_id).first()

    # if a user with this Spotify user ID is not in the database, add it
    if not current_user:
        User(sp_user_id=sp_user_id, display_name=display_name)
        db.session.add(new_user)
        db.session.commit()

    # add the user object to the session
    session['current_user'] = current_user

    return render_template("profile-page.html")


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
