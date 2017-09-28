#!/usr/bin/env python
#coding: utf-8
from locust import HttpLocust, TaskSet, task

class WebsiteTasks(TaskSet):
    def on_start(self):
        pass
        #headers = {'content-type': "application/json"}
        self.client.post("/v1/callback", {"params":"test"})

    @task()
    def index(self):
        self.client.get("/task")

    @task(1)
    def about(self):
        self.client.post("/v1/callback", {"params":"test"})

class WebsiteUser(HttpLocust):
    task_set = WebsiteTasks
    host = "http://192.168.202.24:8989"
    min_wait = 1000
    max_wait = 5000