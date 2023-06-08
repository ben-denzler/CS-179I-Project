from locust import HttpUser, task, constant

"""
Configuration for Locust load tester, see https://docs.locust.io/
"""

host_name = 'cs179i-project.default.example.com'
pics_dir = './pics'
pic = "strawberries.jpg"
model = "AlexNet"

class MyUser(HttpUser):
    wait_time = constant(0)  # Wait time between each task execution
    host = 'http://128.110.218.63:32676'

    @task
    def send_request(self):
        pic_path = pics_dir + '/' + pic
        data = {'model': model}
        files = {'image': (pic, open(pic_path, 'rb'), 'image/jpeg')}
        headers = {'Host': host_name}

        # Send POST request with fields "data, files, headers" to "host"
        with self.client.post("/predict", data=data, files=files, headers=headers, catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Request failed with status code: {response.status_code}")
