from torchvision import models, torch, transforms
from PIL import Image

# Load the pre-trained model
model = models.alexnet(pretrained=True)

# Define image transformation pipeline
transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

# Load and preprocess the input image
img = Image.open("dog.jpg")
img_t = transform(img)
batch_t = torch.unsqueeze(img_t, 0)

# Set the model to evaluation mode and run the input image batch through it
model.eval()
out = model(batch_t)

# Load the ImageNet class labels and find the predicted class index and percentage confidence
with open('imagenet-classes.txt') as labels:
    classes = [line.strip() for line in labels.readlines()]
_, index = torch.max(out, 1)
percentage = torch.nn.functional.softmax(out, dim=1)[0] * 100

# Print the predicted class label and percentage confidence
print(classes[index[0]], percentage[index[0]].item())
