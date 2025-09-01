import torch
from torchvision import transforms
from PIL import Image

# Define preprocessing (must match training setup!)
def preprocess(image: Image.Image):
    transform = transforms.Compose([
        transforms.Grayscale(num_output_channels=3),  # if fonts were grayscale
        transforms.Resize((224, 224)),                # adjust to match training size
        transforms.ToTensor(),
        transforms.Normalize([0.5], [0.5])            # adjust if you used different normalization
    ])
    return transform(image)
