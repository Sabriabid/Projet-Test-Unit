
import pytest
from werkzeug.utils import redirect
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
    assert data.find("Number of Places: 23") 
    assert data.find("Points available: 124") 

#Test de la limite des 12 places achetées 
def test_purchase_12places(client):
    rv2=client.post('/purchasePlaces', data =dict(club = "Simply Lift", competition="Spring Festival", places = 12), follow_redirects = True)
    assert rv2.status_code == 200
    data = rv2.data.decode()
    assert data.find("Impossible to purchase more than 12 places!")
    #pytest
    assert data.find("Number of Places: 23") 
    assert data.find("Points available: 124") 
    #ligne de commande
    # assert data.find("Number of Places: 25") 
    # assert data.find("Points available: 130") 

#Test de la disponibilité des points lors de l'achat
def test_purchase_PointDispo(client):
    rv2=client.post('/purchasePlaces', data =dict(club = "Simply Lift", competition="Spring Festival", places = 130), follow_redirects = True)
    assert rv2.status_code == 200
    data = rv2.data.decode()
    assert data.find("Not enought points !")
    #pytest
    assert data.find("Number of Places: 23") 
    assert data.find("Points available: 124") 
    #ligne de commande:
    # assert data.find("Number of Places: 25") 
    # assert data.find("Points available: 130") 
# Test de Date de competition 
def test_datecompetition(client):
    rv=client.post('/purchasePlaces', data =dict(club = "Simply Lift", competition="Fall Classic", places = 1), follow_redirects = True)
    assert rv.status_code ==200
    data= rv.data.decode()
    assert data.find("La competition est deja passé")
     #pytest
    assert data.find("Number of Places: 11") 
    assert data.find("Points available: 124") 
    #ligne de commande:
    # assert data.find("Number of Places: 13") 
    # assert data.find("Points available: 130") 

def test_logout(client):
    rv = client.get("/logout", follow_redirects=True)
    assert rv.status_code == 200
    data= rv.data.decode()
    assert data.find("Welcome to the GUDLFT Registration Portal!")

