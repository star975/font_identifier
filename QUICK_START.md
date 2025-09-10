# 🚀 Font Identifier - Quick Start Guide

Get up and running with Font Identifier in minutes!

## 🎯 Choose Your Installation Method

### 1. 💻 **Local Installation (Recommended)**

**Windows:**
```cmd
# Download the project
# Extract to your desired folder
# Double-click install.bat or run:
install.bat
```

**macOS/Linux:**
```bash
# Download the project
# Extract to your desired folder
# Make executable and run:
chmod +x install.sh
./install.sh
```

**Then start the app:**
```bash
# Windows: Double-click start.bat or run:
start.bat

# macOS/Linux: Run:
./start.sh
```

### 2. 🐳 **Docker (Cross-Platform)**

```bash
# Clone or download the project
# Navigate to the project folder

# Quick start:
docker-compose up -d

# Or build from scratch:
docker build -t font-identifier .
docker run -p 8501:8501 font-identifier
```

### 3. 📦 **Python Package**

```bash
# Install directly from source:
pip install -e .

# Or install from PyPI (when published):
pip install font-identifier

# Then run:
streamlit run main.py
```

## 📱 Mobile Installation (PWA)

1. **Open** the app in your mobile browser: `http://your-server:8501`
2. **Add to Home Screen**:
   - **iOS**: Tap the share button (📤) → "Add to Home Screen"
   - **Android**: Tap the menu (⋮) → "Add to Home Screen" or "Install App"
3. **Use like a native app** with offline capabilities!

## ⚡ First Time Setup

1. **Open your browser** and go to: `http://localhost:8501`
2. **Create an account** by clicking "Signup"
3. **Log in** with your credentials
4. **Start identifying fonts** by uploading images!

## 🎯 Key Features

### Font Identification
- Upload images containing text
- Get AI-powered font predictions with confidence scores
- Support for 150+ popular fonts

### Screen Recording
- Record your screen with microphone audio
- Take screenshots directly from the browser
- Save and manage your recordings

### Account Management
- Secure user authentication
- Multiple subscription plans
- Payment integration ready

## 🛠️ Configuration

### Environment Variables
Copy `.env.example` to `.env` and customize:

```env
# Basic settings
STREAMLIT_SERVER_PORT=8501
DB_PATH=app_users.db
MODEL_PATH=model.pth

# Security (CHANGE IN PRODUCTION!)
SECRET_KEY=your-secret-key-here

# Payment (optional)
STRIPE_PUBLIC_KEY=pk_...
PAYPAL_CLIENT_ID=...
```

### Custom Model
Replace `model.pth` with your own trained model to recognize different fonts.

## 🎨 Customization

### Themes & Colors
Edit the CSS variables in `main.py`:

```css
:root {
  --accent: #6366f1;     /* Primary color */
  --accent-2: #06b6d4;   /* Secondary color */
  --accent-3: #ec4899;   /* Tertiary color */
  --bg: #0a0f1e;         /* Background */
}
```

### PWA Settings
Modify `static/manifest.json` to customize the mobile app experience.

## 🆘 Troubleshooting

### Common Issues

**Port already in use:**
```bash
streamlit run main.py --server.port 8502
```

**Permission errors (Windows):**
- Run PowerShell as Administrator
- Execute: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

**Python not found:**
- Install Python 3.8+ from [python.org](https://python.org)
- Make sure to check "Add Python to PATH"

**Docker issues:**
- Make sure Docker is installed and running
- Try: `docker-compose down && docker-compose up --build`

**Model not loading:**
- The app will create a dummy model if `model.pth` is missing
- For production, add your trained PyTorch model

## 📊 Usage Examples

### Basic Font Identification
1. Go to Dashboard
2. Upload an image with text
3. View the predicted font and confidence score

### Screen Recording
1. Navigate to "Screen Record"
2. Click "Start Recording"
3. Grant browser permissions
4. Select screen/window to record
5. Click "Stop Recording" when done
6. Download the recording

### Mobile Usage
- Install as PWA for app-like experience
- Works offline for basic features
- Touch-optimized interface

## 🎉 What's Next?

- **Explore** all features through the sidebar navigation
- **Customize** the app by modifying configuration files
- **Contribute** by reporting bugs or suggesting features
- **Deploy** to production using Docker or cloud platforms

## 📖 More Information

- **Full Documentation**: `README.md`
- **API Documentation**: Coming soon
- **Video Tutorials**: Coming soon
- **Community Forum**: GitHub Discussions

## 🤝 Support

Need help? Here's where to get it:

- **GitHub Issues**: Report bugs and request features
- **Documentation**: Check the README.md file
- **Email**: contact@fontidentifier.com
- **Community**: Join our Discord server

---

**Happy font identifying! 🖋️**
