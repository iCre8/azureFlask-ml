from locust import HttpUser, task, between 

class index_loaded(HttpUser): 
    wait_time = between(1, 5)

    @task
    def index_loaded(self): 
        self.client.get("https://flask-ml-demo.azurewebsites.net")