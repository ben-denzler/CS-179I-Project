import requests
import subprocess
import os
from torchvision import models

# TODO: Client should let user specify the image that is sent for recognition
# It's probably fine to just download a set of images in the `pics` folder and let the user choose from those

# Prints a list as comma-seperated elements
def list_to_csv(list):
    list = [str(element) for element in list]
    list = ', '.join(list)
    return list

# Download imagenet-classes.txt if it doesn't exist
if not os.path.exists('imagenet-classes.txt'):
    print("Downloading ImageNet classes file...")
    subprocess.run(['wget', 'https://raw.githubusercontent.com/xmartlabs/caffeflow/master/examples/imagenet/imagenet-classes.txt'])

# Print the models the user can choose from
model_list = dir(models)
print(f"MODELS: {list_to_csv(model_list)}")

# Get user choice of model
user_model = input("\nChoose a model: ")
while user_model not in model_list:
    user_model = input("That's not a valid model, please try again: ")
print(f"\nSending request with model {user_model}...")

# Print the pics the user can choose from
pic_list = os.listdir('./pics')
print(f"PICS: {list_to_csv(pic_list)}")

# Get user choice of pic
user_pic = input("\nChoose a pic: ")
while user_pic not in pic_list:
    user_pic = input("That's not a valid pic, please try again: ")

# Send POST request to the `predict` endpoint
print(f"\nSending request for pic {user_pic} with model {user_model}...")
url = 'http://localhost:5000/predict'
files = {'image': ('dog.jpg', open('pics/dog.jpg', 'rb'), 'image/jpeg')}
try:
    response = requests.post(url, files=files)
    if response.ok:
        result = response.json()
        print(f'Predicted class: {result["class"]}, confidence: {result["confidence"]}')
except requests.exceptions.RequestException as e:
    print("An error occurred while sending the request!")
    print(f"Error: {str(e)}")
