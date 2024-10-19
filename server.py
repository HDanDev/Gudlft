import json
import logging
from flask import Flask,render_template,request,redirect,flash,url_for
from datetime import datetime


def loadClubs():
    with open('clubs.json') as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
         listOfCompetitions = json.load(comps)['competitions']
         return listOfCompetitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()
maxBookingPlaces= 12

logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s %(message)s')

logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s %(message)s')

logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s %(message)s')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/showSummary',methods=['POST'])
def showSummary():
    email = request.form['email']
    club = next((club for club in clubs if club['email'] == email), None)
    other_clubs = [c for c in clubs if c != club]
    
    if club:
        return render_template('welcome.html', club=club, competitions=competitions,clubs=other_clubs)
    else:
        flash("Sorry, that email wasn't found.")
        logging.warning(f"Login attempt with unknown email: {email}")
        return redirect(url_for('index'))


@app.route('/book/<competition>/<club>')
def book(competition,club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        return render_template('booking.html',club=foundClub,competition=foundCompetition, maxBookingPlaces=maxBookingPlaces)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    competition_date = datetime.strptime(competition['date'], "%Y-%m-%d %H:%M:%S")
    current_date = datetime.now()
        
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    
    if competition_date < current_date:
        flash('Error: Cannot book a place on a past competition.')
        return render_template('welcome.html', club=club, competitions=competitions)
    
    placesRequired = int(request.form['places'])
    

    if placesRequired <= maxBookingPlaces:
        competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - placesRequired
        club['points'] = int(club['points']) - placesRequired
        flash(f'Great-booking complete!')
        logging.info(f"Club {club['name']} booked {placesRequired} places in {competition['name']}. Points used: {placesRequired}")
        if int(club['points']) >= placesRequired:
        else:
            competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - int(club['points'])
            availablePoints = club['points']
            club['points'] = 0        
            flash(f"Not enough available points to book the places. You were only able to afford {availablePoints}")
            logging.warning(f"Club {club['name']} attempted to book {placesRequired} places, but only has {club['points']} points.")
    else:    
        flash(f"Unfortunately, it is not authorized to book more than {maxBookingPlaces} places")
        logging.warning(f"Club attempted to book more than the allowed {maxBookingPlaces} places.")
    return render_template('welcome.html', club=club, competitions=competitions)


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))