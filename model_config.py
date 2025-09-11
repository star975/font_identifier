# Model Configuration for Font Identifier
# Configure model download URLs and fallback options

# Primary model download URL (set this to your hosted model URL)
MODEL_DOWNLOAD_URL = None  # e.g., "https://your-domain.com/models/font_model.pth"

# Alternative model URLs (tried in order if primary fails)
FALLBACK_MODEL_URLS = [
    # Add your backup URLs here
    # "https://github.com/your-repo/releases/download/v1.0/model.pth",
    # "https://drive.google.com/uc?id=YOUR_GOOGLE_DRIVE_FILE_ID",
]

# Hugging Face model configuration (if using HF Hub)
HUGGINGFACE_MODEL = {
    "repo_id": None,  # e.g., "your-username/font-identifier"
    "filename": None,  # e.g., "pytorch_model.bin"
}

# Model creation settings for demo/fallback model
DEMO_MODEL_CONFIG = {
    "use_pretrained_backbone": True,  # Use ImageNet pretrained ResNet-18
    "num_classes": 10,  # Number of font classes (auto-detected from labels.txt)
    "architecture": "resnet18"  # Model architecture
}

# Instructions for users
SETUP_INSTRUCTIONS = """
## Model Setup Options:

### Option 1: Upload Model File
- Place your trained `model.pth` file in the project root directory
- Ensure the file is not corrupted and properly saved with PyTorch

### Option 2: Host Model Online
- Upload your model to Google Drive, GitHub Releases, or any file hosting service
- Get the direct download URL
- Set `MODEL_DOWNLOAD_URL` in this file to your URL

### Option 3: Hugging Face Hub
- Upload your model to Hugging Face Hub
- Configure `HUGGINGFACE_MODEL` settings in this file

### Option 4: Use Demo Model
- The app will automatically create a demo model with pretrained weights
- This is for testing purposes only and won't provide accurate font predictions
"""
