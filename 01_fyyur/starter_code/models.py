from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import datetime

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120),nullable=False)
    state = db.Column(db.String(120),nullable=False)
    address = db.Column(db.String(120),nullable=False)
    phone = db.Column(db.String(120),nullable=False)
    genres = db.Column(db.ARRAY(db.String),nullable=False)
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120),nullable=False)
    website = db.Column(db.String(120),nullable=False)
    seeking_talent = db.Column(db.Boolean,default=False,nullable=False)
    seeking_description = db.Column(db.String(200),nullable=True) 
    pass

    # TODO: implement any missing fields, 
    # as a database migration using Flask-Migrate

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120),nullable=False)
    state = db.Column(db.String(120),nullable=False)
    phone = db.Column(db.String(120),nullable=False)
    genres = db.Column(db.ARRAY(db.String),nullable=False)
    image_link = db.Column(db.String(500),nullable=False)
    facebook_link = db.Column(db.String(120),nullable=False)
    website = db.Column(db.String(120),nullable=False)
    seeking_venue = db.Column(db.Boolean,default=False,nullable=False)
    seeking_description = db.Column(db.String(200),nullable=True) 
    pass
    # TODO: implement any missing fields,
    #  as a database migration using Flask-Migrate

# TODO Implement Show and Artist models, and
# complete all model relationships and properties,
#  as a database migration.

class Show(db.Model):
  __tablename__ = 'Show'
  id = db.Column(db.Integer, primary_key=True , autoincrement=True)
  artist_id = db.Column(db.Integer,
                        db.ForeignKey('Artist.id'),
                        nullable=False)
  venue_id= db.Column(db.Integer,
                     db.ForeignKey("Venue.id", ondelete="CASCADE")
                     ,nullable=False)
  start_time = db.Column(db.DateTime,
                         nullable=False,
                         default=datetime.datetime.today())
  pass



