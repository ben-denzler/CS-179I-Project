import requests
import concurrent.futures
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
            # print(f"Predicted class for {result['model']} request {i}: {result['class']}, confidence: {round(result['confidence'], 2)}%")
        else:
            print(f"An error occurred with code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print("An exception occurred while sending the request!")
        print(f"Error: {str(e)}")
        exit(1)
    except KeyboardInterrupt:
        print("Exiting, please wait...")
        exit(1)

# Sends `requests_per_second` images for `test_duration` seconds
i = 0
start_time = time()
end_time = start_time + test_duration
try:
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        while time() < end_time:
            futures.append(executor.submit(send_request, i=i, pic=pic, model=model))
            i += 1
            sleep(1 / requests_per_second)

            # Output num requests per second
            elapsed_time = time() - start_time
            if elapsed_time >= 1:
                print(f"Sent {i} requests in the past second.")
                start_time = time()
                i = 0

        concurrent.futures.wait(futures)
except KeyboardInterrupt:
    print("Exiting, please wait...")
    exit(1)