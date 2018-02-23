# coding=utf8
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """App user"""

    __tablename__ = 'users'

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    sp_user_id = db.Column(db.String(50), unique=True, nullable=False)
    display_name = db.Column(db.String(50))

    def __repr__(self):
        """Show relevant user info when printed"""

        return "\n<User user_id={} display_name={}>".format(self.user_id,
                                                            self.display_name)


class Playlist(db.Model):
    """Playlist, belongs to a particular user"""

    __tablename__ = 'playlists'

    playlist_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    sp_playlist_id = db.Column(db.String(50))
    name = db.Column(db.String(100), nullable=False)

    user = db.relationship('User', backref='playlists')

    def __repr__(self):
        """Show relevant playlist info when printed"""

        return "\n<Playlist playlist_id={} name={}>".format(self.playlist_id,
                                                            self.name)


class Track(db.Model):
    """Track in the database"""

    __tablename__ = 'tracks'

    track_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    sp_track_id = db.Column(db.String(100))
    title = db.Column(db.String(100))
    artist = db.Column(db.String(100))
    album = db.Column(db.String(100))
    duration = db.Column(db.Integer)
    tempo = db.Column(db.Integer)
    danceability = db.Column(db.Float)
    energy = db.Column(db.Float)
    valence = db.Column(db.Float)
    explicit = db.Column(db.Boolean)

    def __repr__(self):
        """Show relevant playlist info when printed"""

        return "\n<Track track_id={} artist={} title={}>".format(self.track_id,
                                                                 self.artist.encode('ascii', 'ignore'),
                                                                 self.title.encode('ascii', 'ignore'))


class PlaylistTrack(db.Model):
    """Playlist/track association table"""

    __tablename__ = 'playlistTracks'

    pt_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    playlist_id = db.Column(db.Integer, db.ForeignKey('playlists.playlist_id'), nullable=False)
    track_id = db.Column(db.Integer, db.ForeignKey('tracks.track_id'), nullable=False)
    position = db.Column(db.Integer)

    playlist = db.relationship('Playlist', backref='playlistTracks')
    track = db.relationship('Track', backref='playlistTracks')

    def __repr__(self):
        """Show track order"""

        return "\n<PlaylistTrack pt_id={} position={}>".format(self.pt_id,
                                                               self.position)


class Filter(db.Model):
    """Filter for a song type"""

    __tablename__ = 'filters'
    
    filter_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    filter_name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    duration_min = db.Column(db.Integer)
    duration_max = db.Column(db.Integer)
    tempo_min = db.Column(db.Integer)
    tempo_max = db.Column(db.Integer)
    danceability_min = db.Column(db.Float)
    danceability_max = db.Column(db.Float)
    energy_min = db.Column(db.Float)
    energy_max = db.Column(db.Float)
    valence_min = db.Column(db.Float)
    valence_max = db.Column(db.Float)
    explicit = db.Column(db.Boolean)

    user = db.relationship('User', backref='filters')

    def __repr__(self):
        """Show filter information"""

        return "\n<Filter filter_id={} filter_name={}>".format(self.filter_id,
                                                               self.filter_name)

# class Template(db.Model):
#     """Template for a type of playlist"""
#     pass


def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///playtime'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    db.create_all()
    print "Connected to DB."