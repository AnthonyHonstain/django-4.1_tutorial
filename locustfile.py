from locust import HttpUser, task, between, constant
import json
import random

'''
In order to run this test locally (at least on Ubuntu) you will need the following.

pip3 install locust

'''


class DetailUser(HttpUser):
    #wait_time = constant(1)  # between(5, 9)

    def on_start(self):
        """ on_start is called when a Locust start before any task is scheduled """
        pass

    def on_stop(self):
        """ on_stop is called when the TaskSet is stopping """
        pass

    @task(1)
    def check_details(self):
        payload = {}
        headers = {}
        self.client.get("/polls/15938",  #adetail",
                        data=json.dumps(payload),
                        headers=headers)
