import pytest
from werkzeug.utils import redirect
from server import loadClubs
from server import loadCompetitions
from server import app
from conftest import client
        
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
    # # pytest:
    # assert data.find("Number of Places: 22") 
    # assert data.find("Points available: 121") 
    # ligne de commande:
    assert data.find("Number of Places: 23") 
    assert data.find("Points available: 124") 
   
    #Deconnexion
    rv_logout = client.get("/logout", follow_redirects=True)
    assert rv_logout.status_code == 200
    data4= rv_logout.data.decode()
    assert data4.find("Welcome to the GUDLFT Registration Portal!")