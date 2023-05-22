import requests
import subprocess
import os
import statistics
from time import time

SERVER_URL = 'http://localhost:5000/predict'
CLASSES_URL = 'https://raw.githubusercontent.com/xmartlabs/caffeflow/master/examples/imagenet/imagenet-classes.txt'
CLASSES_FILE = 'imagenet-classes.txt'
PICS_DIR = './pics'

# Prints a list as comma-seperated elements
def list_to_csv(list):
    list = [str(element) for element in list]
    list = ', '.join(list)
    return list

# Gets positive integer input with error checking
def get_positive_integer():
    while True:
        try:
            value = int(input())
            if value >= 0:
                return value
            else:
                print("Invalid input. Please enter a positive integer: ")
        except ValueError:
            print("Invalid input. Please enter a positive integer: ")

# Download imagenet-classes.txt if it doesn't exist
if not os.path.exists(CLASSES_FILE):
    print("Downloading ImageNet classes file...")
    subprocess.run(['wget', CLASSES_URL])

# Print the pics the user can choose from
pic_list = os.listdir(PICS_DIR)
print(f"PICS: {list_to_csv(pic_list)}")

# Get user choice of pic
user_pic = input("Choose a pic: ")
while user_pic not in pic_list:
    user_pic = input("That's not a valid pic, please try again: ")

# Get number of requests
print("Choose the number of requests to send: ", end='')
num_requests = get_positive_integer()

pic_path = PICS_DIR + '/' + user_pic
execution_times = []

# Send POST request to the server
for i in range(num_requests):
    files = {'image': (user_pic, open(pic_path, 'rb'), 'image/jpeg')}
    print(f"\nSending request {i+1} for pic {user_pic}...")
    try:
        start_time = time()
        response = requests.post(SERVER_URL, files=files)
        elapsed_time = time() - start_time
        execution_times.append(elapsed_time)
        if response.ok:
            result = response.json()
            print(f'Predicted class: {result["class"]}, confidence: {round(result["confidence"], 2)}%')
            print(f"Execution time: {round(elapsed_time, 4)}s")
        else:
            print(f"An error occurred with code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print("An exception occurred while sending the request!")
        print(f"Error: {str(e)}")
        exit(1)

average_time = statistics.mean(execution_times)
print(f"\nAverage execution time: {round(average_time, 4)}s")
