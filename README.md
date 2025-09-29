# 🖋️ Font Identifier & Screen Recorder

An AI-powered font identification tool with integrated screen recording capabilities. Upload images to identify fonts with high confidence, record your screen with audio narration, and manage your work through a modern web interface.

## ✨ Features

- 🎯 **AI Font Recognition**: Upload images and get accurate font predictions with confidence scores
- 🎥 **Screen Recording**: Record screen with microphone audio and webcam overlay
- 📸 **Screenshots**: Capture and save screenshots directly from the browser
- 👤 **User Accounts**: Persistent login system with subscription management
- 💳 **Payment Integration**: Support for multiple payment methods (MasterCard, PayPal, Mobile Money)
- 📱 **Mobile Responsive**: Works seamlessly on desktop and mobile devices
- 🔐 **Secure**: Encrypted passwords and secure user data management

## 🚀 Quick Start

### Option 1: Local Installation (Recommended)

1. **Clone or Download** this repository
2. **Install Python 3.8+** if not already installed
3. **Run the installation script**:

   **Windows:**
   ```powershell
   .\install.bat
   ```

   **macOS/Linux:**
   ```bash
   chmod +x install.sh
   ./install.sh
   ```

4. **Start the application:**
   ```bash
   streamlit run main.py
   ```

5. **Open your browser** and navigate to `http://localhost:8501`

### Option 2: Docker (Cross-Platform)

1. **Install Docker** on your system
2. **Clone this repository**
3. **Run with Docker Compose:**
   ```bash
   docker-compose up -d
   ```
4. **Access the app** at `http://localhost:8501`

### Option 3: Manual Installation

1. **Install Python 3.8+**
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the application:**
   ```bash
   streamlit run main.py
   ```

## 📱 Mobile Installation (PWA)

1. **Open the app** in your mobile browser
2. **Add to Home Screen**:
   - **iOS**: Tap the share button → "Add to Home Screen"
   - **Android**: Tap the menu → "Add to Home Screen" or "Install App"
3. **Use like a native app** with offline capabilities

## 🛠️ System Requirements

### Minimum Requirements
- **OS**: Windows 10, macOS 10.14, Ubuntu 18.04 or newer
- **Python**: 3.8 or higher
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 2GB free space
- **Internet**: Required for initial setup and updates

### Recommended Requirements
- **RAM**: 8GB or more
- **CPU**: Multi-core processor
- **GPU**: NVIDIA GPU with CUDA support (optional, for faster inference)

## 📦 Installation Troubleshooting

### Common Issues

**1. Python not found:**
- Download and install Python from [python.org](https://python.org)
- Make sure to check "Add Python to PATH" during installation

**2. Permission errors (Windows):**
- Run PowerShell as Administrator
- Set execution policy: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

**3. PyTorch installation issues:**
- For CPU-only: `pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu`
- For GPU support: Visit [pytorch.org](https://pytorch.org/get-started/locally/) for specific instructions

**4. Port already in use:**
- Change the port: `streamlit run main.py --server.port 8502`

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the project root:

```env
# Database
DB_PATH=app_users.db

# Model
MODEL_PATH=model.pth

# Server
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0

# Recording
RECORDINGS_DIR=recordings
```

### Custom Model
 The model should be compatible with PyTorch and output predictions for the classes listed in `data/fontlist.txt`.

## 🎯 Usage

### Font Identification
1. **Log in** or create an account
2. **Navigate** to the Dashboard
3. **Upload an image** containing text
4. **View the prediction** with confidence score

### Screen Recording
1. **Go to "Screen Record"** section
2. **Click "Start Recording"** and grant permissions
3. **Select the screen/window** to record
4. **Click "Stop Recording"** when done
5. **Download** your recording from the browser

### Account Management
- **Free Plan**: Basic features with limitations
- **Basic Plan** ($5/month): Unlimited recordings, no watermark
- **Premium Plan** ($10/month): All features + priority support

## 🏗️ Development

### Setup Development Environment
```bash
git clone <repository-url>
cd font-identifier
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements-dev.txt
```

### Project Structure
```
font-identifier/
├── main.py              # Main Streamlit application
├── utils.py             # Image preprocessing utilities
├── requirements.txt     # Python dependencies
├── model.pth           # Pre-trained font classification model
├── data/               # Font data and labels
│   ├── fontlist.txt   # List of font classes
│   └── *.json         # Font metadata
├── recordings/         # Saved recordings (created at runtime)
├── static/            # Static assets for PWA
└── config/            # Configuration files
```

### Adding New Features
1. **Create a new page function** in `main.py`
2. **Add navigation** in the sidebar or navbar
3. **Test thoroughly** on different devices
4. **Update documentation**

## 🐳 Docker Deployment

### Build and Run
```bash
# Build the image
docker build -t font-identifier .

# Run the container
docker run -p 8501:8501 font-identifier
```

### Production Deployment
```bash
# Use docker-compose for production
docker-compose -f docker-compose.prod.yml up -d
```

## 📄 License

This project is licensed under the NSR License. See `LICENSE` file for details.

## 🤝 Contributing

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature-name`
3. **Commit** your changes: `git commit -m 'Add feature'`
4. **Push** to the branch: `git push origin feature-name`
5. **Submit** a pull request

## 🆘 Support

- **Issues**: Report bugs and request features on GitHub Issues
- **Email**: Contact support at -emailkirundastanley@nehemiahstemresearch.com
- **Documentation**: Check the [Wiki](link-to-wiki) for detailed guides

## 🎉 Changelog

### v1.0.0 (Current)
- Initial release with font identification
- Screen recording with audio
- User authentication and subscriptions
- Mobile-responsive design
- Docker support

---

**Made with ❤️ by Mr Stanley**
"# font_identifier" 
