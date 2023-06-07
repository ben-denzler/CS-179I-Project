import requests
import concurrent.futures
import subprocess
import os
import statistics
import csv
from time import time, sleep

SERVER_URL = 'http://127.0.0.1:5000/predict'
# SERVER_URL = 'http://128.110.218.71:30805/predict'
HOST_NAME = 'cs179i-project.default.example.com'
CLASSES_URL = 'https://raw.githubusercontent.com/xmartlabs/caffeflow/master/examples/imagenet/imagenet-classes.txt'
CLASSES_FILE = 'imagenet-classes.txt'
PICS_DIR = './pics'
FILENAME = "./data/execution_time_data.csv"
times = []
execution_times = []
times_to_sleep = [1, 2, 4, 2, 5, 5, 3, 1, 4, 5]

# Sends POST request for image recognition
def send_request(i, pic, model):
    pic_path = PICS_DIR + '/' + pic
    data = {'model': model}
    files = {'image': (pic, open(pic_path, 'rb'), 'image/jpeg')}
    headers = {'Host': HOST_NAME}

    print(f"Sending request {i+1} for pic {pic}...")
    try:
        # Measure time for sending one request
        start_time = time()
        response = requests.post(SERVER_URL, data=data, files=files, headers=headers)
        elapsed_time = time() - start_time

        # Record time since first request, and execution time for the one request
        time_since_first_req = start_time - total_time_start
        times.append(round(time_since_first_req, 3))
        execution_times.append(elapsed_time)

        if response.ok:
            result = response.json()
            print(f"Predicted class for {result['model']} request {i+1}: {result['class']}, confidence: {round(result['confidence'], 2)}%")
            print(f"Execution time for {result['model']} request {i+1}: {round(elapsed_time, 4)}s")
        else:
            print(f"An error occurred with code: {response.status_code}")

    except requests.exceptions.RequestException as e:
        print("An exception occurred while sending the request!")
        print(f"Error: {str(e)}")
        exit(1)

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

# Get user choice of pic
pic_list = os.listdir(PICS_DIR)
print(f"PICS: {list_to_csv(pic_list)}")
user_pic = input("Choose a pic: ")
while user_pic not in pic_list:
    user_pic = input("That's not a valid pic, please try again: ")

# Get number of requests
print("Choose the number of requests to send: ", end='')
num_requests = get_positive_integer()

# Get model to use
model_list = ["AlexNet", "SqueezeNet", "MobileNet"]
print(f"MODELS: {list_to_csv(model_list)}")
user_model = input("Choose a model: ")
while user_model not in model_list:
    user_model = input("That's not a valid model, please try again: ")

# Choose whether to wait between requests
wait_choice = input("Wait between requests? (Yes/No): ").strip().lower()
while wait_choice != "yes" and wait_choice != "no":
    wait_choice = input("That's not a valid choice, please try again (Yes/No): ").strip().lower()

# Send each request as a new thread
total_time_start = time()
with concurrent.futures.ThreadPoolExecutor() as executor:
    futures = []
    for i in range(num_requests):
        if wait_choice == "yes":
            sleep(times_to_sleep[i])
        futures.append(executor.submit(send_request, i=i, pic=user_pic, model=user_model))
    concurrent.futures.wait(futures)
total_time_end = time()

# Output statistics
average_time = statistics.mean(execution_times)
total_time = total_time_end - total_time_start
print(f"\nAverage execution time: {round(average_time, 4)}s")
print(f"Total time to process all requests: {round(total_time, 4)}s")
print(f"Total number of execution times: {len(execution_times)}")

# Write execution time data to CSV file
with open(FILENAME, "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Time (s)", "Execution time (s)"])
    for i in range(len(times)):
        writer.writerow([times[i], execution_times[i]])

print(f"\nData saved to {FILENAME} successfully.")