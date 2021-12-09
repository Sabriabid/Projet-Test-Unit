import json,datetime,time
from datetime import datetime
from os import error
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


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/showSummary',methods=['POST'])
def showSummary():
    club = [club for club in clubs if club['email'] == request.form['email']]
    if club:
        club_email = club[0]
        return render_template('welcome.html',club=club_email,competitions=competitions)
    else:
        return render_template("erreur.html"), 400



@app.route('/book/<competition>/<club>')
def book(competition,club):
    try:
        foundClub = [c for c in clubs if c['name'] == club ][0]
        foundCompetition = [c for c in competitions if c['name'] == competition][0]
        if foundClub and foundCompetition:
            return render_template('booking.html',club=foundClub,competition=foundCompetition)
    except:
        return render_template('erreur.html'),400


@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    try:
        competition = [c for c in competitions if c['name'] == request.form['competition']][0]
        club = [c for c in clubs if c['name'] == request.form['club']][0]
        placesRequired = int(request.form['places'])
        #Nombre de points insufisant:
        if int(club["points"]) < (placesRequired)*3:
            flash("Not enought points !")
        #Nombre de place acheté depasse 12
        elif int(placesRequired)*3 >= 36:
            flash('Impossible to purchase more than 12 places!')
        #Nombre de places negatives
        elif int(placesRequired) <= 0:
            flash('Serieously!!(negatif number of place)')
        #Nombre de place pas suffisant 
        elif placesRequired > int(competition["numberOfPlaces"])*3:
            flash("Not enought places availible !")

        elif int(datetime.timestamp(datetime.strptime(competition['date'], "%Y-%m-%d %H:%M:%S"))) <= int(datetime.timestamp(datetime.now())):
            flash("La competition est deja passé")

        elif int(club["points"]) > 0:
            competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - placesRequired
            club['points'] = int(club['points']) - (placesRequired)*3
            club['solde'] = club['points']
            flash('Great-booking complete!')
    except Exception as error:
        flash("Something went wrong-please try again")
    return render_template('welcome.html', club=club, competitions=competitions)
    
@app.route('/historique')
def index_historique():
    lesclub = [lesclub for lesclub in clubs]
    return render_template('score.html',clubs=clubs)

@app.route('/logout')
def logout():
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)