from locust import HttpUser, task, between

"""
This file is intended to be used with the load tester Locust.
This is for testing.
"""

HOST_NAME = 'cs179i-project.default.example.com'
PICS_DIR = './pics'
pic = "strawberries.jpg"
model = "AlexNet"

class MyUser(HttpUser):
    wait_time = between(1, 3)  # Wait time between each task execution
    host = 'http://128.110.218.63:32676/predict'

    @task
    def send_request(self):
        pic_path = PICS_DIR + '/' + pic
        data = {'model': model}
        files = {'image': (pic, open(pic_path, 'rb'), 'image/jpeg')}
        headers = {'Host': HOST_NAME}

        with self.client.post("/predict", data=data, files=files, headers=headers, catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure("Request failed")
