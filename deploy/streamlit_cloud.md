# 🌩️ Streamlit Cloud Deployment

Deploy your Font Identifier app to Streamlit Cloud for free hosting.

## 📋 Prerequisites

1. **GitHub Repository**: Your code must be in a GitHub repository
2. **Streamlit Cloud Account**: Sign up at [share.streamlit.io](https://share.streamlit.io)
3. **Model File**: Ensure `model.pth` is accessible (see options below)

## 🚀 Deployment Steps

### 1. Prepare Your Repository

**Option A: Public Repository (Recommended)**
```bash
# Push your code to GitHub
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/yourusername/font-identifier.git
git push -u origin main
```

**Option B: Private Repository**
- Upload to GitHub as a private repository
- Grant Streamlit Cloud access to your private repos

### 2. Handle Large Files (Model.pth)

Since `model.pth` might be too large for GitHub, choose one option:

**Option A: Git LFS (Large File Storage)**
```bash
git lfs install
git lfs track "*.pth"
git add .gitattributes
git add model.pth
git commit -m "Add model with LFS"
git push
```

**Option B: External Storage**
```python
# Add to main.py before model loading
import requests
import os

def download_model():
    if not os.path.exists("model.pth"):
        print("Downloading model...")
        url = "https://your-storage.com/model.pth"  # Your model URL
        response = requests.get(url)
        with open("model.pth", "wb") as f:
            f.write(response.content)
        print("Model downloaded successfully!")

# Call before load_model_and_classes()
download_model()
```

**Option C: Dummy Model for Demo**
The app already handles missing model files by creating a dummy model.

### 3. Create Streamlit Configuration

Create `.streamlit/config.toml`:
```toml
[server]
headless = true
enableCORS = false
enableXsrfProtection = false
maxUploadSize = 50

[browser]
gatherUsageStats = false

[theme]
primaryColor = "#6366f1"
backgroundColor = "#0a0f1e"
secondaryBackgroundColor = "#1e293b"
textColor = "#f8fafc"
```

### 4. Create Secrets Configuration

In Streamlit Cloud dashboard, add secrets:
```toml
# .streamlit/secrets.toml (for local development)
# Add these as secrets in Streamlit Cloud dashboard

SECRET_KEY = "your-production-secret-key-here"
ENVIRONMENT = "production"

# Optional: Database URL for cloud database
DATABASE_URL = "postgresql://user:pass@host:port/dbname"

# Optional: Payment keys
STRIPE_SECRET_KEY = "sk_live_..."
PAYPAL_CLIENT_SECRET = "..."

# Optional: Storage keys
AWS_ACCESS_KEY_ID = "..."
AWS_SECRET_ACCESS_KEY = "..."
S3_BUCKET_NAME = "your-bucket"
```

### 5. Update Code for Cloud Deployment

Add to the top of `main.py`:
```python
# Production configuration
if st.secrets.get("ENVIRONMENT") == "production":
    DB_PATH = st.secrets.get("DATABASE_URL", "app_users.db")
    os.environ["SECRET_KEY"] = st.secrets.get("SECRET_KEY", "fallback-key")
    
    # Disable file watcher in production
    os.environ["STREAMLIT_SERVER_FILE_WATCHER_TYPE"] = "none"
```

### 6. Deploy to Streamlit Cloud

1. **Go to** [share.streamlit.io](https://share.streamlit.io)
2. **Sign in** with GitHub
3. **Click** "New app"
4. **Select** your repository
5. **Set** main file path: `main.py`
6. **Configure** advanced settings if needed
7. **Click** "Deploy!"

### 7. Configure Domain (Optional)

**Free Subdomain**: `your-app-name.streamlit.app`

**Custom Domain** (Requires GitHub Pro):
1. Add CNAME record: `your-domain.com` → `your-app.streamlit.app`
2. Configure in Streamlit Cloud dashboard

## ⚙️ Configuration Options

### Environment Variables in Streamlit Cloud

Add in the "Advanced settings" or secrets:

```bash
STREAMLIT_SERVER_HEADLESS=true
STREAMLIT_SERVER_ENABLE_CORS=false
PYTHONUNBUFFERED=1
```

### Database Options

**Option 1: SQLite (Simple)**
```python
# Uses local SQLite file (resets on deployment)
DB_PATH = "app_users.db"
```

**Option 2: PostgreSQL (Recommended for Production)**
```python
# Add to requirements.txt: psycopg2-binary
import psycopg2
DATABASE_URL = st.secrets["DATABASE_URL"]
```

**Option 3: Airtable/Sheets (No-code)**
```python
# Add to requirements.txt: pyairtable
import pyairtable
AIRTABLE_API_KEY = st.secrets["AIRTABLE_API_KEY"]
```

## 🔧 Troubleshooting

### Common Issues

**1. App won't start:**
- Check requirements.txt has all dependencies
- Verify Python version compatibility
- Check logs in Streamlit Cloud dashboard

**2. Model loading errors:**
- Ensure model.pth is accessible
- Check file size limits
- Verify PyTorch installation

**3. Database errors:**
- SQLite file resets on each deployment
- Use external database for persistence
- Check connection strings

**4. Memory issues:**
- Streamlit Cloud has 1GB RAM limit
- Optimize model size
- Use model quantization

### Performance Optimization

```python
# Add to main.py
@st.cache_resource
def load_model():
    # Your model loading code
    return model

@st.cache_data
def preprocess_image(image):
    # Your preprocessing code
    return processed_image
```

## 🚀 Production Checklist

- [ ] Repository is public/accessible
- [ ] All secrets configured
- [ ] Model file accessible
- [ ] Database configured
- [ ] SSL/HTTPS enabled (automatic)
- [ ] Custom domain configured (optional)
- [ ] Error handling implemented
- [ ] Monitoring set up

## 📊 Monitoring

Monitor your app through:
- **Streamlit Cloud dashboard**: View logs and metrics
- **GitHub**: Track repository activity
- **External monitoring**: Use services like UptimeRobot

## 💡 Tips

1. **Keep repository clean**: Use .gitignore for large files
2. **Use caching**: Implement st.cache for better performance
3. **Handle errors gracefully**: Add try-catch blocks
4. **Test locally first**: Always test before deploying
5. **Monitor usage**: Keep track of resource usage

Your app will be available at: `https://your-app-name.streamlit.app`
