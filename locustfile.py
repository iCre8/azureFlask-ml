from locust import HttpLocust, task, between 
app = Flask(__name__)

class WebsiteUser(HttpLocust): 
    wait_time = between(5, 15)

    def on_start(self): 
        self.client.post("/login", {
            "username" : "test_user", 
            "password" : ""
        })

    @task
    def index_page(self):
        self.client.get("/")
