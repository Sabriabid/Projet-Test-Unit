
import pytest
from werkzeug.utils import redirect
from server import loadClubs
from server import loadCompetitions
from server import app
from conftest import client
        
# Test page index
def test_index_ok(client):
    response = client.get('/')
    assert response.status_code == 200

#Test page show summary 
def test_showSummary(client):
    rv = client.post('/showSummary', data=dict(email="john@simplylift.co"), follow_redirects=True)
    assert rv.status_code == 200
    data = rv.data.decode()
    assert "Welcome, john@simplylift.co" in data
    
#Test adresse mail non indetifiée
def test_NoShowSummary(client):
     rv = client.post('/showSummary', data=dict(email="john@simplylift.com"), follow_redirects=True)
     assert rv.status_code == 400
     data = rv.data.decode()
     assert "404" in data
     assert "PAGE NOT FOUND" in data

#test du booking
def test_booking(client):
    rv= client.post('/purchasePlaces', data =dict(club = 'Simply Lift', competition='Spring Festival', places = 5), follow_redirects = True)
    assert rv.status_code == 200
    data = rv.data.decode()
    assert "/book/Fall%20Classic/Simply%20Lift" in data

#Test de nobooking
def test_nobooking(client):
    rv= client.get("/book/Spring%20Festival/Simply%20Lift1", follow_redirects=True)
    assert rv.status_code == 400
    data = rv.data.decode()
    assert "PAGE NOT FOUND" in data

#Test du bon deroulement de l'achat
def test_purchase(client):
    rv2=client.post('/purchasePlaces', data =dict(club = "Simply Lift", competition="Spring Festival", places = 2), follow_redirects = True)
    assert rv2.status_code == 200
    data = rv2.data.decode()
    assert "Great-booking complete!" in data
    #pytest et commande
    assert "Number of Places: 23" in data 
    assert "Points available: 7" in data 

#Test de la limite des 12 places achetées 
def test_purchase_12places(client):
    rv2=client.post('/purchasePlaces', data =dict(club = "Simply Lift", competition="Spring Festival", places = 12), follow_redirects = True)
    assert rv2.status_code == 200
    data = rv2.data.decode()
    assert data.find("Impossible to purchase more than 12 places!")
    #pytest
    assert "Number of Places: 23" in data 
    assert "Points available: 7" in data
    #ligne de commande
    # assert "Number of Places: 25" in data 
    # assert "Points available: 13" in data

#Test de la disponibilité des points lors de l'achat
def test_purchase_PointDispo(client):
    rv2=client.post('/purchasePlaces', data =dict(club = "Simply Lift", competition="Spring Festival", places = 10), follow_redirects = True)
    assert rv2.status_code == 200
    data = rv2.data.decode()
    assert data.find("Not enought points !")
    #pytest
    assert "Number of Places: 23" in data 
    assert "Points available: 7" in data
    #ligne de commande:*
    assert "Number of Places: 25" in data 
    assert "Points available: 13" in data
# Test de Date de competition 
def test_datecompetition(client):
    rv=client.post('/purchasePlaces', data =dict(club = "Simply Lift", competition="Fall Classic", places = 1), follow_redirects = True)
    assert rv.status_code ==200
    data= rv.data.decode()
    assert data.find("La competition est deja passé")
     #pytest
    # assert "Number of Places: 11" in data 
    # assert "Points available: 7" in data
    #ligne de commande:*
    assert "Number of Places: 13" in data 
    assert "Points available: 13" in data

def test_logout(client):
    rv = client.get("/logout", follow_redirects=True)
    assert rv.status_code == 200
    data= rv.data.decode()
    assert data.find("Welcome to the GUDLFT Registration Portal!")

def test_integration(client):
    #Load Club
    club= loadClubs()
    assert list(club[0].keys())==['name','email','points']
    #Load Compet
    competitions = loadCompetitions()
    assert list(competitions[0].keys())==['name','date','numberOfPlaces']

    #index
    rp = client.get('/')
    assert rp.status_code == 200
    data=rp.data.decode()
    print(data)
    assert "Welcome to the GUDLFT Registration Portal!" in data

    #Connexion
    rv= client.post('/showSummary',data=dict(email="john@simplylift.co"),follow_redirects=True)
    assert rv.status_code == 200
    data1 = rv.data.decode()
    assert "/book/Fall%20Classic/Simply%20Lift" in data1

    #Acces a la page d'achat
    rv_test= client.get('/book/Spring%20Festival/Simply%20Lift',follow_redirects=True)
    assert rv_test.status_code==200
    data2=rv_test.data.decode()
    print(data1)
    assert "Spring Festival" in data2

    #Achat
    rv_test1=client.post('/purchasePlaces', data =dict(club="Simply Lift", competition="Spring Festival", places= 1), follow_redirects = True)
    assert rv_test1.status_code == 200
    data3 =rv_test1.data.decode()
    print(data2)
    assert "Great-booking complete!" in data3
    # pytest:
    # assert "Number of Places: 22" in data3 
    # assert "Points available: 4" in data3
    # ligne de commande:
    assert "Number of Places: 24" in data3
    assert "Points available: 10" in data3
    
    #Deconnexion
    rv_logout = client.get("/logout", follow_redirects=True)
    assert rv_logout.status_code == 200
    data4= rv_logout.data.decode()
    assert data4.find("Welcome to the GUDLFT Registration Portal!")