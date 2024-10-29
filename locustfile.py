from locust import HttpUser, TaskSet, task, between

class UserBehavior(TaskSet):
    @task
    def load_index(self):
        self.client.get("/")

    @task
    def load_show_summary(self):
        self.client.post("/showSummary", data={"email": "admin@irontemple.com"})

    @task
    def book_place(self):
        self.client.get("/book/Spring%20Festival/Simply%20Lift")
        
    @task
    def purchase_places(self):
        self.client.post("/purchasePlaces", data={
            "competition": "Fall Classic",
            "club": "She Lifts",
            "places": 5
        })

class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(1, 5)

