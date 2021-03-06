# coding=utf8
from flask_sqlalchemy import SQLAlchemy
import json

db = SQLAlchemy()


class ToDictMixin(object):
    """Convert an object into a dict with attributes"""

    def to_dict(self):

        object_info = {}

        # loop through columns, set key as column name and value as attribute value
        for column_name in self.__mapper__.column_attrs.keys():
            attribute = getattr(self, column_name, None)
            object_info[column_name] = attribute

        return object_info

    def to_json(self):

        return json.dumps(self.to_dict())


class FormatConversionMixin(object):
    """Mixin to convert time and percentage formats"""

    def to_mins_secs(self, attribute):
        """Takes in the attribute to be converted (min_duration_ms or max_duration_ms), 
        turns length of time in milliseconds to a string in the format mins:secs or the string 'None'"""

        if not attribute:
            return 'None'

        mins = attribute / 60000
        secs = (attribute % 60000) / 1000

        if secs < 10:
            return str(mins) + ':0' + str(secs)
        else:
            return str(mins) + ':' + str(secs)

    def to_percentage(self, attribute):
        """Takes in the attribute to be converted,
        turns decimal representation of percentage to decimal string representation"""

        if not attribute:
            return 'None'

        return str(int(attribute * 100)) + '%'


class User(db.Model):
    """App user"""

    __tablename__ = 'users'

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    sp_user_id = db.Column(db.String(50), unique=True, nullable=False)
    display_name = db.Column(db.String(50))

    def __repr__(self):
        """Show relevant user info when printed"""

        return "\n<User user_id={} display_name={}>".format(self.user_id, self.display_name)


class Playlist(db.Model, ToDictMixin):
    """Playlist, belongs to a particular user"""

    __tablename__ = 'playlists'

    playlist_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    sp_playlist_id = db.Column(db.String(50))
    name = db.Column(db.String(100), nullable=False)

    user = db.relationship('User', backref='playlists')

    def __repr__(self):
        """Show relevant playlist info when printed"""

        return "\n<Playlist playlist_id={} name={}>".format(self.playlist_id, self.name)


class Track(db.Model, ToDictMixin, FormatConversionMixin):
    """Track in the database"""

    __tablename__ = 'tracks'

    track_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    sp_track_id = db.Column(db.String(100))
    title = db.Column(db.String(100))
    artist = db.Column(db.String(100))
    album = db.Column(db.String(100))
    duration_ms = db.Column(db.Integer)
    tempo = db.Column(db.Integer)
    danceability = db.Column(db.Float)
    energy = db.Column(db.Float)
    valence = db.Column(db.Float)
    is_explicit = db.Column(db.Boolean)

    # set up secondary relationship to Playlist table

    def __repr__(self):
        """Show relevant playlist info when printed"""

        return "\n<Track track_id={} artist={} title={}>".format(self.track_id,
                                                                 self.artist.encode('ascii', 'ignore'),
                                                                 self.title.encode('ascii', 'ignore'))

    def view_is_explicit(self):
        """Takes the boolean value of track.is_explicit and returns a descriptive string"""

        if self.is_explicit:
            return "Explicit"
        else:
            return ""


class PlaylistTrack(db.Model):
    """Playlist/track middle table"""

    __tablename__ = 'playlistTracks'

    pt_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    playlist_id = db.Column(db.Integer, db.ForeignKey('playlists.playlist_id'), nullable=False)
    track_id = db.Column(db.Integer, db.ForeignKey('tracks.track_id'), nullable=False)
    position = db.Column(db.Integer)

    playlist = db.relationship('Playlist', backref='playlistTracks')
    track = db.relationship('Track', backref='playlistTracks')

    def __repr__(self):
        """Show track order"""

        return "\n<PlaylistTrack pt_id={} position={}>".format(self.pt_id, self.position)


class Category(db.Model, ToDictMixin, FormatConversionMixin):
    """User-created category for a song type"""

    __tablename__ = 'categories'
    
    cat_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    cat_name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    min_duration_ms = db.Column(db.Integer)
    max_duration_ms = db.Column(db.Integer)
    min_tempo = db.Column(db.Integer)
    max_tempo = db.Column(db.Integer)
    min_danceability = db.Column(db.Float)
    max_danceability = db.Column(db.Float)
    min_energy = db.Column(db.Float)
    max_energy = db.Column(db.Float)
    min_valence = db.Column(db.Float)
    max_valence = db.Column(db.Float)
    exclude_explicit = db.Column(db.Boolean)

    user = db.relationship('User', backref='categories')

    def __repr__(self):
        """Show filter information"""

        return "\n<Category cat_id={} cat_name={}>".format(self.cat_id, self.cat_name)


################################Helper functions################################

def connect_to_db(app, db_uri='postgresql:///playtime'):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":

    from server import app
    connect_to_db(app)
    db.create_all()
    print "Connected to DB."