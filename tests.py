from model import User, Playlist, PlaylistTrack, Track, Category, connect_to_db, db
from server import app
import server
import helper
import db_functions
import fake_api_calls
server.a = fake_api_calls
helper.a = fake_api_calls
db_functions.a = fake_api_calls
import unittest
from unittest import TestCase
import doctest
from flask import Flask, session

class FlaskTestsBasic(TestCase):
    """Flask tests """

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True

    def test_index(self):
        """Test homepage"""

        result = self.client.get('/')
        self.assertIn('<h1>Welcome to PlayTime!</h1>', result.data)


class FlaskTestsRoutes(TestCase):
    """Flask route tests"""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        app.config['TESTING'] = True
        self.client = app.test_client()

        # Connect to test database
        connect_to_db(app, "postgresql:///testdb")

        with self.client as c:
            with c.session_transaction() as sess:
                sess['current_user'] = 1

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        # db.drop_all()

    def test_profile(self):
        """Test profile page for a logged in user"""
        
        result = self.client.get('/profile')
        self.assertIn('Hi valerie!', result.data)

    def test_playlists(self):
        """Test my_playlists page"""

        result = self.client.get('/my_playlists')
        self.assertIn('My Playlists', result.data)

    def test_view_playlist(self):
        """Test a single playlist view/edit page"""

        result = self.client.get('/playlist/1')
        self.assertIn('Bon Iver', result.data)

    def test_categories(self):
        """Test my_categories page"""

        result = self.client.get('/my_categories')
        self.assertIn('Slow', result.data)



if __name__ == '__main__':
    # If called like a script, run our tests
    unittest.main()
