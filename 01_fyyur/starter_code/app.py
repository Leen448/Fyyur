#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import (
    Flask, 
    render_template, 
    request, 
    Response, 
    flash, 
    redirect, 
    url_for
)
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *

from flask_migrate import Migrate
from sqlalchemy import distinct
from models import app, db, Venue, Artist, Show
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')


# TODO: connect to a local postgresql database
db = SQLAlchemy(app)
migrate = Migrate(app, db)


#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format)


app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#


@app.route('/')
def index():
    return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  # num_shows should be aggregated based on number of upcoming shows per venue.
  locals = []
  venues = Venue.query.all()
  for place in Venue.query.distinct(Venue.city, Venue.state).all():
    locals.append({
      'city': place.city,
      'state': place.state,
      'venues': [{
          'id': venue.id,
          'name': venue.name,
      } for venue in venues if
         venue.city == place.city and venue.state == place.state]
    })
  return render_template('pages/venues.html', areas=locals)


@app.route('/venues/search', methods=['POST'])
def search_venues():
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for Hop should return "The Musical Hop".
    # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
    search_term = request.form.get("search_term", "")
    response = {}
    response['data'] = Venue.query.filter(
        Venue.name.ilike(f"%{search_term}%")).all()
    response['count'] = len(response['data'])
    return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    # shows the venue page with the given venue_id
    # TODO: replace with real venue data from the venues table, using venue_id
    data = []
    query = db.session.query(Show, Venue,
                             Artist.id.label("artist_id"),
                             Artist.name.label("artist_name"),
                             Artist.image_link.label("artist_image_link")
                             ).join(Venue).filter(Venue.id == venue_id).join(Artist).group_by(Show.id, Artist.id, Venue.id,).all()
    # check if query has a result if not just show venue info
    if query:
        data = {
            "id": venue_id,
            "name": query[0].Venue.name,
            "genres": query[0].Venue.genres,
            "city": query[0].Venue.city,
            "state": query[0].Venue.state,
            "phone": query[0].Venue.phone,
            "address": query[0].Venue.address,
            "website": query[0].Venue.website,
            "seeking_talent": query[0].Venue.seeking_talent,
            "seeking_description": query[0].Venue.seeking_description,
            "facebook_link": query[0].Venue.facebook_link,
            "image_link": query[0].Venue.image_link,
            "upcoming_shows_count": 0,
            "past_shows_count": 0
        }
        past_shows_count = 0
        upcoming_shows_count = 0
        upcoming_shows = []
        past_shows = []
        for d in query:
            if datetime.now() > d.Show.start_time:
                show = {
                    "artist_id": d.artist_id,
                    "artist_name": d.artist_name,
                    "artist_image_link": d.artist_image_link,
                    "start_time": str(d.Show.start_time)
                }
                past_shows.append(show)
                past_shows_count = past_shows_count+1
            elif datetime.now() < d.Show.start_time:
                show = {
                    "artist_id": d.artist_id,
                    "artist_name": d.artist_name,
                    "artist_image_link": d.artist_image_link,
                    "start_time": str(d.Show.start_time)
                }
                upcoming_shows.append(show)
                upcoming_shows_count = upcoming_shows_count+1
        data["past_shows_count"] = past_shows_count
        data["upcoming_shows_count"] = upcoming_shows_count
        data["past_shows"] = past_shows
        data["upcoming_shows"] = upcoming_shows
        return render_template('pages/show_venue.html', venue=data)
    else:
        query = db.session.query(Venue).filter(Venue.id == venue_id).all()
        data = {
            "id": venue_id,
            "name": query[0].name,
            "genres": query[0].genres,
            "city": query[0].city,
            "state": query[0].state,
            "phone": query[0].phone,
            "address": query[0].address,
            "seeking_talent": query[0].seeking_talent,
            "seeking_description": query[0].seeking_description,
            "facebook_link": query[0].facebook_link,
            "image_link": query[0].image_link,
            "website": query[0].website,
            "upcoming_shows_count": 0,
            "past_shows_count": 0
        }
    return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------


@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    # TODO: insert form data as a new Venue record in the db, instead
    # TODO: modify data to be the data object returned from db insertion

    form = VenueForm(request.form, meta={'csrf': False})
    try:
        venue = Venue()
        form.populate_obj(venue)
        db.session.add(venue)
        db.session.commit()
        # on successful db insert, flash success
        flash('Venue ' + form.name.data + ' was successfully listed!')
    except ValueError as e:
        print(e)
        error = True
        db.session.rollback()
        # TODO: on unsuccessful db insert, flash an error instead.
        flash('An error occurred. Venue ' +
              form.name.data + ' could not be listed.')
    finally:
        db.session.close()
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    return render_template('pages/home.html')


  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record.
  # Handle cases where the session commit could fail.
  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page,
  # have it so that clicking that button delete it
  # from the db then redirect the user to the homepage
  # return None
@app.route("/venues/Delete_by_ID/<venue_id>")
def delete_venue(venue_id):
    venue_name = Venue.query.get(venue_id).name
    try:
        venue = db.session.query(Venue).filter(Venue.id == venue_id).first()
        db.session.delete(venue)
        db.session.commit()
        flash("Venue: " + venue_name + " was successfully deleted.")
    except:
        db.session.rollback()
        flash('An error occured. Venue could not be deleted.')
    finally:
        db.session.close()
        return redirect(url_for("index"))

#  Artists
#  ----------------------------------------------------------------


@app.route('/artists')
def artists():
    # TODO: replace with real data returned from querying the database
    data = db.session.query(Artist.id, Artist.name).all()
    return render_template('pages/artists.html', artists=data)


@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search.
  #  Ensure it is case-insensitive.
  # seach for "A" should return
  # "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  search_term = request.form.get("search_term", "")
  response = {}
  response['data'] = Artist.query.filter(
      Artist.name.ilike(f"%{search_term}%")).all()
  response['count'] = len(response['data'])
  return render_template('pages/search_artists.html',
                          results=response, 
                          search_term=request.form.get('search_term','')
                        )


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
# shows the artist page with the given artist_id
# TODO: replace with real artist data 
# from the artists table, using artist_id
  data = []
  query = db.session.query(Show, Artist,
                            Venue.id.label("venue_id"),
                            Venue.name.label("venue_name"),
                            Venue.image_link.label("venue_image_link")
                            ).join(Artist).filter(Artist.id == artist_id
                            ).join(Venue
                            ).group_by(Show.id, Artist.id, Venue.id,
                            ).all()
  # check if query has a result if not just show artist info
  if query:
      data = {
      "id": artist_id,
      "name": query[0].Artist.name,
      "genres": query[0].Artist.genres,
      "city": query[0].Artist.city,
      "state": query[0].Artist.state,
      "phone": query[0].Artist.phone,
      "website": query[0].Artist.website,
      "seeking_venue": query[0].Artist.seeking_venue,
      "seeking_description": query[0].Artist.seeking_description,
      "facebook_link": query[0].Artist.facebook_link,
      "image_link": query[0].Artist.image_link,
      "upcoming_shows_count": 0,
      "past_shows_count": 0
      }
      past_shows_count = 0
      upcoming_shows_count = 0
      upcoming_shows = []
      past_shows = []
      for d in query:
          if datetime.today() > d.Show.start_time:
              show = {
                  "venue_id": d.venue_id,
                  "venue_name": d.venue_name,
                  "venue_image_link": d.venue_image_link,
                  "start_time": str(d.Show.start_time)
              }
              past_shows.append(show)
              past_shows_count = past_shows_count+1
          elif datetime.today() <= d.Show.start_time:
              show = {
                  "venue_id": d.venue_id,
                  "venue_name": d.venue_name,
                  "venue_image_link": d.venue_image_link,
                  "start_time": str(d.Show.start_time)
              }
              upcoming_shows.append(show)
              upcoming_shows_count = upcoming_shows_count+1
      data["past_shows_count"] = past_shows_count
      data["upcoming_shows_count"] = upcoming_shows_count
      data["past_shows"] = past_shows
      data["upcoming_shows"] = upcoming_shows
      return render_template('pages/show_artist.html', artist=data)
  else:
      query = db.session.query(Artist).filter(Artist.id == artist_id).all()
      data = {
          "id": artist_id,
          "name": query[0].name,
          "genres": query[0].genres,
          "city": query[0].city,
          "state": query[0].state,
          "phone": query[0].phone,
          "website": query[0].website,
          "seeking_venue": query[0].seeking_venue,
          "seeking_description": query[0].seeking_description,
          "facebook_link": query[0].facebook_link,
          "image_link": query[0].image_link,
          "upcoming_shows_count": 0,
          "past_shows_count": 0
      }
      return render_template('pages/show_artist.html', artist=data)


#  Update
#  ----------------------------------------------------------------
@app.route('/artists/Edite_by_ID/<int:artist_id>', methods=['GET'])
def edit_artist(artist_id):
  try:
      artist = db.session.query(Artist).filter(
          Artist.id == artist_id).first()
      form = ArtistForm(obj=artist)
      artist = {
          'id': artist_id,
          'name': artist.name
      }
  except:
      db.session.rollback()
      flash("Something went wrong. Please try again.")
      return redirect(url_for("index"))
  finally:
      db.session.close()
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)


@app.route('/artists/Edite_by_ID/<int:artist_id>', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  try:
      artist = db.session.query(Artist).filter(
          Artist.id == artist_id).first()
      form = ArtistForm(request.form, meta={'csrf': False})
      form.populate_obj(artist)
      db.session.add(artist)
      db.session.commit()
      flash("The artist has been edited successfully")
  except:
      db.session.rollback()
      flash("Something went wrong. Please try again.")
      return redirect(url_for("index"))
  finally:
      db.session.close()
  return redirect(url_for('show_artist', artist_id=artist_id))


@app.route('/venues/Edite_by_ID/<int:venue_id>', methods=['GET'])
def edit_venue(venue_id):
  try:
      venue = db.session.query(Venue).filter(Venue.id == venue_id).first()
      form = VenueForm(obj=venue)
      venue = {
          'id': venue_id,
          'name': venue.name
      }
  except:
      db.session.rollback()
      flash("Something went wrong. Please try again.")
      return redirect(url_for("index"))
  finally:
      db.session.close()
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/Edite_by_ID/<int:venue_id>', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  try:
      venue = db.session.query(Venue).filter(Venue.id == venue_id).first()
      form = VenueForm(request.form, meta={'csrf': False})
      form.populate_obj(venue)
      db.session.add(venue)
      db.session.commit()
      flash("The venue has been edited successfully")
  except:
      db.session.rollback()
      flash("Something went wrong. Please try again.")
      return redirect(url_for("index"))
  finally:
      db.session.close()
      return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------


@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    # called upon submitting the new artist listing form
    # TODO: insert form data as a new artist record in the db, instead
    # TODO: modify data to be the data object returned from db insertion

    form = ArtistForm(request.form, meta={'csrf': False})
    try:
        artist = Artist()
        form.populate_obj(artist)
        db.session.add(artist)
        db.session.commit()
    # on successful db insert, flash success
        flash('Artist ' + form.name.data + ' was successfully listed!')
    except ValueError as e:
        print(e)
        db.session.rollback()
        # TODO: on unsuccessful db insert, flash an error instead.
        flash('An error occurred. Artist ' +
              form.name.data + ' could not be listed.')
    finally:
        db.session.close()
    
    return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
    # displays list of shows at /shows
    # TODO: replace with real venues data.
  # num_shows should be aggregated based on
  # number of upcoming shows per venue.
  data = []
  query = db.session.query(
      Show.id,
      Show.start_time,
      Artist.name.label("artist_name"),
      Artist.image_link.label("artist_image_link"),
      Artist.id.label("artist_id"),
      Venue.id.label("venue_id"),
      Venue.name.label("venue_name")
    ).join(Artist).join(Venue).group_by(Show.id, Artist.id, Venue.id,
    ).order_by(Show.id).all()
  for d in query:
      each_show_data = {
          "Show.id": d.id,
          "start_time": str(d.start_time),
          "artist_id": d.artist_id,
          "artist_name": d.artist_name,
          "artist_image_link": d.artist_image_link,
          "venue_id": d.venue_id,
          "venue_name": d.venue_name,
      }
      data.append(each_show_data)
  return render_template('pages/shows.html', shows=data)


@app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db,
  # upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
  error = False
  artist_id = request.form['artist_id']
  venue_id = request.form['venue_id']
  start_time = request.form['start_time']
  Artist_result = Artist.query.filter(Artist.id == artist_id).count()

  if Artist_result > 0:
      Venue_result = Venue.query.filter(Venue.id == venue_id).count()
      if Venue_result > 0:
        try:
            show = Show(artist_id=artist_id, venue_id=venue_id,
                        start_time=start_time)
            db.session.add(show)
            db.session.commit()
        except:
            db.session.rollback()
            db.session.close()
            error = True
        if error:
            # TODO: on unsuccessful db insert, flash an error instead.
            flash('An error occurred. Show could not be listed.')
        else:
            # on successful db insert, flash success
            flash('Show was successfully listed!')
            # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
        return render_template('pages/home.html')
      else:
          flash('Venue ID not valid')
          form = ShowForm()
          return render_template('forms/new_show.html', form=form)
  else:
      flash('Artist ID not valid')
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
