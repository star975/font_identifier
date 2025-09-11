# 🚀 Font Identifier - cPanel Deployment Guide

This guide helps you deploy the Font Identifier app to any cPanel hosting provider.

## 📋 Prerequisites

### Hosting Requirements
- **Python 3.9+** support
- **pip** package installer
- **SSH access** (recommended) or File Manager
- **Subdomain/domain** for the app
- **Minimum 1GB RAM** (for PyTorch dependencies)

### Popular cPanel Hosts that Support Python
- ✅ **A2 Hosting** - Full Python support
- ✅ **SiteGround** - Python apps supported
- ✅ **InMotion Hosting** - Python/Django support
- ✅ **Hostinger** - Python applications
- ✅ **Bluehost** - Python support (check plan)
- ✅ **GoDaddy** - Python on some plans

## 🛠️ Deployment Methods

### Method 1: SSH Deployment (Recommended)
```bash
# 1. Connect to your server via SSH
ssh username@yourdomain.com

# 2. Navigate to your domain directory
cd public_html/yourdomain.com  # or subdomain directory

# 3. Clone the repository
git clone https://github.com/star975/font_identifier.git
cd font_identifier

# 4. Set up Python virtual environment
python3 -m venv venv
source venv/bin/activate

# 5. Install dependencies
pip install -r requirements_full.txt

# 6. Set up the application
python setup_cpanel.py
```

### Method 2: File Manager Upload
1. **Download ZIP** from GitHub repository
2. **Extract locally** and upload files via cPanel File Manager
3. **Create virtual environment** via cPanel Python app interface
4. **Install dependencies** using pip in terminal or Python app settings

### Method 3: cPanel Python App (If Available)
1. **Go to cPanel → Software → Python**
2. **Create New Python App**
3. **Configure settings** (see configuration section below)
4. **Upload application files**

## ⚙️ Configuration Files

### 1. Application Configuration (app.ini)
```ini
[uwsgi]
module = wsgi:application
home = /home/username/public_html/yourdomain.com/venv
pythonpath = /home/username/public_html/yourdomain.com

# Process settings
processes = 2
threads = 2
master = true
vacuum = true

# Socket settings
socket = /tmp/%n.sock
chmod-socket = 666
chown-socket = username:username

# Logging
logto = /home/username/logs/font_identifier.log
```

### 2. WSGI Entry Point (wsgi.py)
```python
import sys
import os
from pathlib import Path

# Add application directory to Python path
app_dir = Path(__file__).parent
sys.path.insert(0, str(app_dir))

# Set environment variables
os.environ['STREAMLIT_SERVER_HEADLESS'] = 'true'
os.environ['STREAMLIT_SERVER_PORT'] = '8501'
os.environ['STREAMLIT_BROWSER_GATHER_USAGE_STATS'] = 'false'

# Import and configure Streamlit
import streamlit.web.bootstrap as bootstrap
from streamlit import config as st_config

def application(environ, start_response):
    # Configure Streamlit for WSGI
    st_config.set_option('server.headless', True)
    st_config.set_option('server.enableCORS', False)
    
    # Start Streamlit application
    return bootstrap.run('main_full.py', '', [], {})
```

## 🔧 Setup Script for cPanel

I'll create an automated setup script that handles the cPanel deployment process.

## 📁 Directory Structure (cPanel)
```
public_html/yourdomain.com/
├── font_identifier/
│   ├── main_full.py           # Main application
│   ├── wsgi.py               # WSGI entry point
│   ├── requirements_full.txt  # Dependencies
│   ├── model.pth             # AI model (if available)
│   ├── app_users.db          # User database
│   ├── static/               # Static files
│   ├── recordings/           # User recordings
│   └── venv/                # Virtual environment
├── .htaccess                 # URL rewriting
└── logs/                     # Application logs
```

## 🌐 Domain Configuration

### .htaccess Configuration
```apache
RewriteEngine On
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule ^(.*)$ http://localhost:8501/$1 [P,L]

# Security headers
Header always set X-Frame-Options DENY
Header always set X-Content-Type-Options nosniff
```

## 🚀 Performance Optimizations for Shared Hosting

### Resource Limits
- **Memory**: Configure for shared hosting limits
- **CPU**: Optimize thread counts for shared resources
- **Storage**: Use efficient file caching

### Configuration Tweaks
```python
# Optimized for shared hosting
STREAMLIT_CONFIG = {
    'server.maxUploadSize': 10,  # 10MB max uploads
    'server.maxMessageSize': 50,  # 50MB max message
    'runner.maxCachedMessageAge': 300,  # 5 minutes cache
}
```

## 📊 Monitoring and Maintenance

### Log Files
- **Application logs**: `~/logs/font_identifier.log`
- **Error logs**: `~/logs/error.log` 
- **Access logs**: Check cPanel logs

### Health Monitoring
```bash
# Check if app is running
ps aux | grep streamlit

# Monitor resource usage
top -u username

# Check logs for errors
tail -f ~/logs/font_identifier.log
```

## 🔒 Security Considerations

### File Permissions
```bash
chmod 755 public_html/yourdomain.com/
chmod 644 *.py
chmod 600 app_users.db
chmod 755 recordings/
```

### Database Security
- Use strong database passwords
- Limit file upload sizes
- Implement rate limiting

## 📞 Troubleshooting

### Common Issues
1. **Python version mismatch** → Check hosting Python version
2. **Memory limits** → Optimize dependencies, use lighter model
3. **Permission errors** → Set correct file permissions
4. **Module not found** → Ensure virtual environment is activated

### Support Resources
- Check hosting provider's Python documentation
- Contact hosting support for Python app setup
- Use hosting provider's error logs

## 🎯 Next Steps After Reading This Guide

1. **Choose your hosting provider** (with Python support)
2. **Confirm Python version** (3.9+ required)
3. **Test with minimal version first** (current deployment)
4. **Scale up to full version** once basic setup works

Would you like me to create the automated setup script and deployment files for your specific hosting provider?
