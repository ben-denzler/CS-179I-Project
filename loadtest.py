import requests
from time import time, sleep

"""
This script places a load on our service by sending image recognition requests.
We can specify requests per second (RPS) and the test duration.
"""

SERVER_URL = 'http://128.110.218.63:32676/predict'
HOST_NAME = 'cs179i-project.default.example.com'
PICS_DIR = './pics'

# Test settings
requests_per_second = 100
test_duration = 10
pic = "strawberries.jpg"
model = "AlexNet"

# Sends POST request for image recognition
def send_request(i, pic, model):
    pic_path = PICS_DIR + '/' + pic
    data = {'model': model}
    files = {'image': (pic, open(pic_path, 'rb'), 'image/jpeg')}
    headers = {'Host': HOST_NAME}
    try:
        response = requests.post(SERVER_URL, data=data, files=files, headers=headers)
        if response.ok:
            result = response.json()
            print(f"Predicted class for {result['model']} request {i}: {result['class']}, confidence: {round(result['confidence'], 2)}%")
        else:
            print(f"An error occurred with code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print("An exception occurred while sending the request!")
        print(f"Error: {str(e)}")
        exit(1)

# Sends `requests_per_second` images for `test_duration` seconds
i = 0
end_time = time() + test_duration
try:
    while time() < end_time:
        send_request(i, pic, model)
        i += 1
        sleep(1 / requests_per_second)
except KeyboardInterrupt:
    exit(1)