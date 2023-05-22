import os
import subprocess
import torch
from flask import Flask, request, jsonify
from torchvision import models, transforms
from PIL import Image

CLASSES_URL = 'https://raw.githubusercontent.com/xmartlabs/caffeflow/master/examples/imagenet/imagenet-classes.txt'
CLASSES_FILE = 'imagenet-classes.txt'

# Download imagenet-classes.txt if it doesn't exist
if not os.path.exists(CLASSES_FILE):
    print("Downloading ImageNet classes file...")
    subprocess.run(['wget', CLASSES_URL])

# Load the pre-trained AlexNet model
model = models.alexnet(pretrained=True)

# Define image transformation pipeline
transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

app = Flask(__name__)

# Handle any issues that come up during processing
@app.errorhandler(Exception)
def handle_exception(error):
    # Log the error, outputs to console
    app.logger.error(f"Exception occurred during request processing: {error}")
    
    # Return an error response to the client
    response = jsonify({'error': 'An error occurred during request processing.'})
    response.status_code = 500
    return response

# Define a route for the image recognition endpoint
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Load and preprocess the input image from the client request
        file = request.files['image']
        img = Image.open(file.stream)
        img_t = transform(img)
        batch_t = torch.unsqueeze(img_t, 0)

        # Set the model to evaluation mode and run the input image batch through it
        model.eval()
        out = model(batch_t)

        # Load the ImageNet class labels and find the predicted class index and percentage confidence
        with open(CLASSES_FILE) as labels:
            classes = [line.strip() for line in labels.readlines()]
        _, index = torch.max(out, 1)
        percentage = torch.nn.functional.softmax(out, dim=1)[0] * 100

        # Return the predicted class label and percentage confidence to the client
        return jsonify({'class': classes[index[0]], 'confidence': percentage[index[0]].item()})
    
    except Exception as e:
        return handle_exception(e)

if __name__ == '__main__':
    app.run()
