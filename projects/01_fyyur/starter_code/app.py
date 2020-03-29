# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#

import os, sys, datetime
import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *

# ----------------------------------------------------------------------------#
# App Config.
# ----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# ----------------------------------------------------------------------------#
# Models.
# ----------------------------------------------------------------------------#


class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    genres = db.Column(db.String(500), nullable=False)
    website = db.Column(db.String(500))
    seeking_talent = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(500))
    shows = db.relationship('Show', backref='venue', lazy=True, cascade='delete')


class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(500), nullable=False)
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(500))
    seeking_venue = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(500))
    shows = db.relationship('Show', backref='artist', lazy=True, cascade='delete')


class Show(db.Model):
    __tablename__ = 'Show'

    id = db.Column(db.Integer, primary_key=True)
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)


# ----------------------------------------------------------------------------#
# Filters.
# ----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format)


app.jinja_env.filters['datetime'] = format_datetime


def extract_genres(genre_string):
    """Extract the list of genres from the genre string stored in the db.  Inverse of form submit."""
    result = list(map(lambda x: x.strip("'"), genre_string.strip('[]').split(', ')))
    return result


# ----------------------------------------------------------------------------#
# Controllers.
# ----------------------------------------------------------------------------#

@app.route('/')
def index():
    return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
    venues = Venue.query.all()
    cities_states_set = {(venue.city, venue.state) for venue in venues}  # set of all city, state pairs
    # populate the data dictionary according to how the html template expects it
    data = [
        {
            "city": city,
            "state": state,
            "venues": [
                {
                    "id": venue.id,
                    "name": venue.name,
                    "num_upcoming_shows": Show.query.filter_by(venue_id=venue.id).filter(Show.start_time > datetime.now()).count()
                }
                for venue in Venue.query.filter_by(city=city, state=state).all()
            ]
        }
        for (city, state) in cities_states_set
    ]
    return render_template('pages/venues.html', areas=data)


@app.route('/venues/search', methods=['POST'])
def search_venues():
    # case-insensitive search on venues with partial string search.
    search_term = request.form.get('search_term', '')
    matched_venues = Venue.query.filter(Venue.name.ilike("%" + search_term + "%")).all()

    response = {
        "count": len(matched_venues),
        "data": [
            {
                "id": matching_venue.id,
                "name": matching_venue.name,
                "num_upcoming_shows": Show.query.filter_by(venue_id=matching_venue.id).filter(Show.start_time > datetime.now()).count(),
            }
            for matching_venue in matched_venues
        ]
    }
    return render_template('pages/search_venues.html', results=response, search_term=search_term)


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    # shows the venue page with the given venue_id
    venue = Venue.query.get(venue_id)
    past_shows = Show.query.filter_by(venue_id=venue_id).filter(Show.start_time <= datetime.now()).all()
    upcoming_shows = Show.query.filter_by(venue_id=venue_id).filter(Show.start_time > datetime.now()).all()
    data = {
        "id": venue_id,
        "name": venue.name,
        "genres": extract_genres(venue.genres),
        "address": venue.address,
        "city": venue.city,
        "state": venue.state,
        "phone": venue.phone,
        "website": venue.website,
        "facebook_link": venue.facebook_link,
        "seeking_talent": venue.seeking_talent,
        "seeking_description": venue.seeking_description,
        "image_link": venue.image_link,
        "past_shows": [
           {
               "artist_id": show.artist_id,
               "artist_name": show.artist.name,
               "artist_image_link": show.artist.image_link,
               "start_time": format_datetime(str(show.start_time)),
           }
            for show in past_shows
        ],
        "upcoming_shows": [
            {
               "artist_id": show.artist_id,
               "artist_name": show.artist.name,
               "artist_image_link": show.artist.image_link,
               "start_time": format_datetime(str(show.start_time)),
            }
            for show in upcoming_shows
        ],
        "past_shows_count": len(past_shows),
        "upcoming_shows_count": len(upcoming_shows),
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
    # called upon submitting the new venue listing form
    form = request.form
    data = create_record(form, "Venue")  # can create and insert any of Venue, Artist, and Show

    return render_template('pages/home.html')


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    name = ""
    try:
        venue = Venue.query.get(venue_id)
        name = " " + venue.name
        db.session.delete(venue)
        db.session.commit()
        # on successful db delete, flash success
        flash("Venue" + name + ' was successfully deleted!')
    except:
        db.session.rollback()
        error = True
        print(sys.exc_info())
        # on unsuccessful db delete, flash an error instead.
        flash('An error occurred. Venue' + name + ' could not be deleted.')
    finally:
        db.session.close()

    # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
    # clicking that button delete it from the db then redirect the user to the homepage
    return redirect(url_for('index'))


#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
    data = [
        {
            "id": artist.id,
            "name": artist.name,
        }
        for artist in Artist.query.all()
    ]
    return render_template('pages/artists.html', artists=data)


@app.route('/artists/search', methods=['POST'])
def search_artists():
    # case-insensitive search on artists with partial string search.
    search_term = request.form.get('search_term', '')
    matched_artists = Artist.query.filter(Artist.name.ilike("%" + search_term + "%")).all()

    response = {
        "count": len(matched_artists),
        "data": [
            {
                "id": matching_artist.id,
                "name": matching_artist.name,
                "num_upcoming_shows": Show.query.filter_by(artist_id=matching_artist.id).filter(Show.start_time > datetime.now()).count(),
            }
            for matching_artist in matched_artists
        ]
    }
    return render_template('pages/search_artists.html', results=response, search_term=search_term)


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    # shows the artist page with the given artist_id
    artist = Artist.query.get(artist_id)
    past_shows = Show.query.filter_by(artist_id=artist_id).filter(Show.start_time <= datetime.now()).all()
    upcoming_shows = Show.query.filter_by(artist_id=artist_id).filter(Show.start_time > datetime.now()).all()
    data = {
        "id": artist_id,
        "name": artist.name,
        "genres": extract_genres(artist.genres),
        "city": artist.city,
        "state": artist.state,
        "phone": artist.phone,
        "website": artist.website,
        "facebook_link": artist.facebook_link,
        "seeking_venue": artist.seeking_venue,
        "seeking_description": artist.seeking_description,
        "image_link": artist.image_link,
        "past_shows": [
            {
                "venue_id": show.venue_id,
                "venue_name": show.venue.name,
                "venue_image_link": show.venue.image_link,
                "start_time": format_datetime(str(show.start_time)),
            }
            for show in past_shows
        ],
        "upcoming_shows": [
            {
                "venue_id": show.venue_id,
                "venue_name": show.venue.name,
                "venue_image_link": show.venue.image_link,
                "start_time": format_datetime(str(show.start_time)),
            }
            for show in upcoming_shows
        ],
        "past_shows_count": len(past_shows),
        "upcoming_shows_count": len(upcoming_shows),
    }
    return render_template('pages/show_artist.html', artist=data)


#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    artist = Artist.query.get(artist_id)

    # populate artist form with current data
    form = ArtistForm(
        name=artist.name,
        city=artist.city,
        state=artist.state,
        phone=artist.phone,
        facebook_link=artist.facebook_link,
        genres=extract_genres(artist.genres),
    )

    return render_template('forms/edit_artist.html', form=form, artist=artist)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    # takes values from the form submitted, and update existing
    # artist record with ID <artist_id> using the new attributes
    form = request.form
    name = ""
    try:
        artist = Artist.query.get(artist_id)
        artist.name = form['name']
        artist.city = form['city']
        artist.state = form['state']
        artist.phone = form['phone']
        artist.genres = str(form.getlist('genres'))  # store genres as a string of the list of genres
        artist.facebook_link = form['facebook_link']
        db.session.add(artist)
        db.session.commit()
        name = " " + str(artist.id)
        # on successful db update, flash success
        flash("Artist" + name + ' was successfully edited!')
    except:
        db.session.rollback()
        error = True
        print(sys.exc_info())
        # on unsuccessful db update, flash an error instead.
        flash('An error occurred. Artist' + name + ' could not be edited.')
    finally:
        db.session.close()

    return redirect(url_for('show_artist', artist_id=artist_id))


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    form = VenueForm()
    venue = {
        "id": 1,
        "name": "The Musical Hop",
        "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
        "address": "1015 Folsom Street",
        "city": "San Francisco",
        "state": "CA",
        "phone": "123-123-1234",
        "website": "https://www.themusicalhop.com",
        "facebook_link": "https://www.facebook.com/TheMusicalHop",
        "seeking_talent": True,
        "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
        "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
    }
    # TODO: populate form with values from venue with ID <venue_id>
    return render_template('forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    # TODO: take values from the form submitted, and update existing
    # venue record with ID <venue_id> using the new attributes
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
    form = request.form
    data = create_record(form, "Artist")  # can create and insert any of Artist, Venue, and Show

    return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
    # displays list of shows at /shows
    show = Show.query.all()[0]
    data = [
        {
            "venue_id": show.venue_id,
            "venue_name": show.venue.name,
            "artist_id": show.artist_id,
            "artist_name": show.artist.name,
            "artist_image_link": show.artist.image_link,
            "start_time": format_datetime(str(show.start_time)),
        }
        for show in Show.query.all()
    ]
    return render_template('pages/shows.html', shows=data)


@app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    # called to create new shows in the db, upon submitting new show listing form
    form = request.form
    data = create_record(form, "Show")  # can create and insert any of Show, Artist, and Venue

    return render_template('pages/home.html')


# ----------------------------------------------------------------------------#
# Generic Record Management.
# ----------------------------------------------------------------------------#


def create_record(form, record_type):
    name = ""
    try:
        if record_type != "Show":
            name = " " + form['name']
            if record_type == "Venue":
                data = Venue(**form)
            elif record_type == "Artist":
                data = Artist(**form)
            data.genres = str(form.getlist('genres'))  # store genres as a string of the list of genres
        else:
            data = Show(**form)
        db.session.add(data)
        db.session.commit()
        if record_type == "Show":
            name = " " + str(data.id)
        # on successful db insert, flash success
        flash(record_type + name + ' was successfully listed!')
    except:
        db.session.rollback()
        error = True
        print(sys.exc_info())
        # on unsuccessful db insert, flash an error instead.
        flash('An error occurred. ' + record_type + name + ' could not be listed.')
    finally:
        db.session.close()
    return data


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

# ----------------------------------------------------------------------------#
# Launch.
# ----------------------------------------------------------------------------#

# Default port:
'''
if __name__ == '__main__':
    app.run()
'''

# Or specify port manually:
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    #app.run(host='0.0.0.0', port=port)
    app.run()
