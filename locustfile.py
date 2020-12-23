from locust import HttpUser, task, between 


class index_loaded(HttpUser): 
    wait_time = between(5, 15)

    def on_start(self): 
        self.client.get("https://flask-ml-demo.azurewebsites.net")

    @task
    def prediction(self):
        self.client.post("/secondary_router")

    @task
    def run_predict(self): 
        self.client.get("/predict")