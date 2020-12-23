from locust import HttpUser, task, between 


class index_loaded(HttpUser): 
    wait_time = between(1, 5)

    def on_start(self): 
        self.client.get("https://flask-ml-demo.azurewebsites.net")

 