import json
import logging
from flask import Flask,render_template,request,redirect,flash,url_for


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

logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s %(message)s')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/showSummary', methods=['POST'])
def showSummary():
    email = request.form['email']
    club = next((club for club in clubs if club['email'] == email), None)

    if club:
        return render_template('welcome.html', club=club, competitions=competitions)
    else:
        flash("Sorry, that email wasn't found.")
        logging.warning(f"Login attempt with unknown email: {email}")
        return redirect(url_for('index'))


@app.route('/book/<competition>/<club>')
def book(competition,club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        return render_template('booking.html',club=foundClub,competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        logging.error(f"Booking failed for competition {competition} and club {club}")
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    placesRequired = int(request.form['places'])
    placesCost = placesRequired * 1  # Each place costs 3 points

    if placesRequired <= int(competition['numberOfPlaces']):
        if int(club['points']) >= placesCost:
            competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - placesRequired
            club['points'] = int(club['points']) - placesCost
            flash(f'Great - booking complete! You have used {placesCost} points.')
            logging.info(f"Club {club['name']} booked {placesRequired} places in {competition['name']}. Points used: {placesCost}")
        else:
            flash("Not enough points to book the required places.")
            logging.warning(f"Club {club['name']} attempted to book {placesRequired} places, but only has {club['points']} points.")
    else:
        flash("Not enough places available for booking.")
        logging.warning(f"Club {club['name']} attempted to book {placesRequired} places, but only {competition['numberOfPlaces']} are available.")

    return render_template('welcome.html', club=club, competitions=competitions)



# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))