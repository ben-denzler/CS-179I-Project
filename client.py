import requests
import subprocess
import os
from torchvision import models

# TODO: Client should let user specify the image that is sent for recognition
# It's probably fine to just download a set of images in the `pics` folder and let the user choose from those

# TODO: Client should let user specify the model the server uses for image recognition
# The command `print(dir(models))` prints all the models
# User probably doesn't need to choose from every one of them
# We can identify the most interesting models and provide those as options

# Download imagenet-classes.txt if it doesn't exist
if not os.path.exists('imagenet-classes.txt'):
    print("Downloading ImageNet classes file...")
    subprocess.run(['wget', 'https://raw.githubusercontent.com/xmartlabs/caffeflow/master/examples/imagenet/imagenet-classes.txt'])

# Send POST request to the `predict` endpoint
url = 'http://localhost:5000/predict'
files = {'image': ('dog.jpg', open('pics/dog.jpg', 'rb'), 'image/jpeg')}
response = requests.post(url, files=files)

if response.ok:
    result = response.json()
    print(f'Predicted class: {result["class"]}, confidence: {result["confidence"]}')
else:
    print(f'Error: {response.status_code} - {response.text}')
