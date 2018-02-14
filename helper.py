# coding=utf8
from flask import (Flask, request, session)
import sys
import requests
import config
from model import User, Playlist, PlaylistTrack, Track, connect_to_db, db
# import api_calls as a


def add_user_to_session(current_user):
    """Add the current user id to the session"""

    session['current_user'] = current_user.user_id

    print "Added to session: current_user", session['current_user']


def response_error(status_code):
    """Status code error messaging"""

    return render_template('error-page.html', status_code=status_code)