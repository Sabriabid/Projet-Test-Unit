import time 
from locust import HttpLocust, HttpUser , task , between
from locust.user import wait_time
from server import clubs, competitions

class PerfTest(HttpUser):
    wait_time = between(1,5)


    @task
    def index(self):
        self.client.get(url="/")


    @task
    def user_login(self):
        data = {"email":"admin@irontemple.com"}
        self.client.post("/showSummary",data)

    @task 
    def user_book(self):
        self.client.get(url='/book/Spring%20Festival/Iron%20Temple')

    @task
    def user_score(self):
        self.client.get(url='/score')

    @task
    def user_purchase(self):
        #self.client.get(url='/book/Spring%20Festival/Iron%20Temple')
        #data = {"competitions":"Spring%20Festival","clubs":"Iron%20Temple"}
        #self.client.get(url='/book/Spring%20Festival/Iron%20Temple')
        #self.client.post("/purchasePlaces", data =dict(club = 'Iron Temple', competition='Spring Festival', places = 1))
        data={"club":"Iron%20Temple","competition":"Spring%20Festival","places":1}
        self.client.post("/purchasePlaces", data)



    @task
    def logout(self):
        self.client.get(url='/logout')