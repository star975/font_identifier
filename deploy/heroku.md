# 🚀 Heroku Deployment

Deploy your Font Identifier app to Heroku with custom domain and SSL support.

## 📋 Prerequisites

1. **Heroku Account**: Sign up at [heroku.com](https://heroku.com)
2. **Heroku CLI**: Install from [devcenter.heroku.com/articles/heroku-cli](https://devcenter.heroku.com/articles/heroku-cli)
3. **Git Repository**: Your code in a Git repository

## 🛠️ Setup Files

### 1. Create Procfile

```bash
# Procfile (no extension)
web: streamlit run main.py --server.port=$PORT --server.address=0.0.0.0 --server.headless=true
```

### 2. Create runtime.txt

```bash
# runtime.txt
python-3.9.19
```

### 3. Update requirements.txt

```txt
streamlit==1.38.0
torch==2.2.2+cpu
torchvision==0.17.2+cpu
Pillow==10.4.0
opencv-python-headless==4.10.0.84
pyautogui==0.9.54
numpy==1.26.4
pandas==2.2.2
scikit-learn==1.5.2
matplotlib==3.9.2
moviepy==1.0.3
requests==2.31.0
imageio[ffmpeg]
gunicorn==21.2.0
psycopg2-binary==2.9.7
```

### 4. Create app.json (Optional)

```json
{
  "name": "Font Identifier",
  "description": "AI-powered font identification with screen recording",
  "keywords": ["streamlit", "ai", "font-identification", "machine-learning"],
  "website": "https://github.com/nehemiahsterm/font-identifier",
  "repository": "https://github.com/star975/font-identifier",
  "logo": "https://your-nehemiahsterm.com/logo.png",
  "success_url": "/",
  "env": {
    "SECRET_KEY": {
      "description": "Secret key for sessions",
      "generator": "secret"
    },
    "ENVIRONMENT": {
      "description": "Application environment",
      "value": "production"
    }
  },
  "formation": {
    "web": {
      "quantity": 1,
      "size": "basic"
    }
  },
  "addons": [
    "heroku-postgresql:mini"
  ],
  "buildpacks": [
    {
      "url": "heroku/python"
    }
  ]
}
```

## 🚀 Deployment Steps

### 1. Login to Heroku

```bash
heroku login
```

### 2. Create Heroku App

```bash
# Create new app
heroku create your-font-identifier-app

# Or with specific region
heroku create your-font-identifier-app --region eu
```

### 3. Add PostgreSQL Database (Recommended)

```bash
# Add PostgreSQL addon
heroku addons:create heroku-postgresql:mini
```

### 4. Configure Environment Variables

```bash
# Set production environment
heroku config:set ENVIRONMENT=production

# Set secret key
heroku config:set SECRET_KEY=$(openssl rand -base64 32)

# Set Streamlit configuration
heroku config:set STREAMLIT_SERVER_HEADLESS=true
heroku config:set STREAMLIT_SERVER_ENABLE_CORS=false
heroku config:set STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION=false

# Optional: Payment configuration
heroku config:set STRIPE_SECRET_KEY=sk_live_...
heroku config:set PAYPAL_CLIENT_SECRET=...

# Optional: File storage
heroku config:set AWS_ACCESS_KEY_ID=...
heroku config:set AWS_SECRET_ACCESS_KEY=...
heroku config:set S3_BUCKET_NAME=your-bucket
```

### 5. Deploy to Heroku

```bash
# Add Heroku remote
heroku git:remote -a your-font-identifier-app

# Deploy
git add .
git commit -m "Deploy to Heroku"
git push heroku main
```

### 6. Scale the App

```bash
# Ensure at least one web dyno is running
heroku ps:scale web=1
```

## 🗄️ Database Configuration

### Update main.py for PostgreSQL

Add to the beginning of `main.py`:

```python
import os
import urllib.parse

# Database configuration for Heroku
if os.getenv('ENVIRONMENT') == 'production':
    # Parse DATABASE_URL
    database_url = os.getenv('DATABASE_URL')
    if database_url and database_url.startswith('postgres://'):
        # Heroku provides postgres://, but SQLAlchemy needs postgresql://
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    
    # Use PostgreSQL instead of SQLite
    DB_PATH = database_url or "app_users.db"
    
    # Production settings
    os.environ["STREAMLIT_SERVER_FILE_WATCHER_TYPE"] = "none"
    os.environ["STREAMLIT_SERVER_RUN_ON_SAVE"] = "false"
```

### Create Database Migration Script

Create `migrate_db.py`:

```python
import os
import psycopg2
import sqlite3
from urllib.parse import urlparse

def migrate_sqlite_to_postgres():
    """Migrate SQLite database to PostgreSQL"""
    
    # Connect to SQLite
    sqlite_conn = sqlite3.connect('app_users.db')
    sqlite_cursor = sqlite_conn.cursor()
    
    # Connect to PostgreSQL
    postgres_url = os.getenv('DATABASE_URL')
    postgres_conn = psycopg2.connect(postgres_url)
    postgres_cursor = postgres_conn.cursor()
    
    # Create users table in PostgreSQL
    postgres_cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(255) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            created_at TIMESTAMP NOT NULL,
            plan VARCHAR(50) DEFAULT 'Free',
            expiry_date TIMESTAMP
        );
    """)
    
    # Migrate data
    sqlite_cursor.execute("SELECT username, password_hash, created_at, plan, expiry_date FROM users")
    users = sqlite_cursor.fetchall()
    
    for user in users:
        postgres_cursor.execute("""
            INSERT INTO users (username, password_hash, created_at, plan, expiry_date)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (username) DO NOTHING
        """, user)
    
    postgres_conn.commit()
    postgres_cursor.close()
    postgres_conn.close()
    sqlite_cursor.close()
    sqlite_conn.close()

if __name__ == "__main__":
    migrate_sqlite_to_postgres()
```

## 📁 File Storage Configuration

### Option 1: Heroku Ephemeral File System

```python
# Files are temporary and reset on dyno restart
RECORDINGS_DIR = "/tmp/recordings"
os.makedirs(RECORDINGS_DIR, exist_ok=True)
```

### Option 2: AWS S3 Integration

```python
import boto3
from botocore.exceptions import ClientError

def upload_to_s3(file_path, bucket_name, object_name=None):
    """Upload a file to an S3 bucket"""
    if object_name is None:
        object_name = os.path.basename(file_path)

    s3_client = boto3.client(
        's3',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
    )

    try:
        s3_client.upload_file(file_path, bucket_name, object_name)
    except ClientError as e:
        return False
    return True
```

## 🔧 Production Optimizations

### 1. Update main.py for Production

```python
# Add at the top of main.py
import logging

# Configure logging for Heroku
if os.getenv('ENVIRONMENT') == 'production':
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s %(message)s',
        handlers=[logging.StreamHandler()]
    )
    
    # Disable debug mode
    st.set_option('client.showErrorDetails', False)
```

### 2. Add Health Check Endpoint

```python
# Add to main.py
@st.cache_data
def health_check():
    """Health check for monitoring"""
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}

# Add a health check page
if st.experimental_get_query_params().get("health"):
    st.json(health_check())
    st.stop()
```

## 🎛️ Heroku Configuration Commands

```bash
# View app logs
heroku logs --tail

# View configuration
heroku config

# Open app in browser
heroku open

# Run one-off command
heroku run python migrate_db.py

# Scale dynos
heroku ps:scale web=2

# Restart app
heroku restart

# Connect to database
heroku pg:psql
```

## 🔐 SSL and Custom Domain

### 1. Add Custom Domain

```bash
# Add custom domain
heroku domains:add yourdomain.com
heroku domains:add www.yourdomain.com

# View DNS targets
heroku domains
```

### 2. SSL Certificate (Automatic)

Heroku automatically provides SSL certificates for custom domains.

### 3. DNS Configuration

Add these DNS records:

```
CNAME: www.yourdomain.com → your-app-name.herokuapp.com
CNAME: yourdomain.com → your-app-name.herokuapp.com
```

## 📊 Monitoring and Scaling

### 1. Add Monitoring

```bash
# Add New Relic monitoring
heroku addons:create newrelic:wayne

# Add logging
heroku addons:create papertrail:choklad
```

### 2. Auto-scaling

```bash
# Install autoscaling addon
heroku addons:create scheduler:standard

# Configure scaling rules
heroku autoscaling:enable web
heroku autoscaling:set web --min=1 --max=10 --cpu_threshold=80
```

## 💰 Cost Optimization

### Free Tier Limits

- **750 dyno hours/month** (about 1 app running 24/7)
- **10,000 rows** in PostgreSQL
- **App sleeps** after 30 minutes of inactivity

### Paid Plans

- **Basic ($7/month)**: No sleeping, 1000 dyno hours
- **Standard ($25/month)**: Better performance, more features
- **Performance ($250+/month)**: High-performance dynos

## 🚨 Troubleshooting

### Common Issues

**1. App crashed:**
```bash
heroku logs --tail
heroku restart
```

**2. Build failed:**
- Check requirements.txt versions
- Verify Python version in runtime.txt
- Check for memory issues during build

**3. Database connection errors:**
```bash
heroku pg:info
heroku config:get DATABASE_URL
```

**4. File upload issues:**
- Heroku has ephemeral file system
- Use cloud storage for persistence
- Check file size limits

### Debug Commands

```bash
# Check dyno status
heroku ps

# View recent releases
heroku releases

# Rollback to previous version
heroku rollback v123

# Run bash in dyno
heroku run bash
```

## ✅ Deployment Checklist

- [ ] Procfile created
- [ ] runtime.txt specified
- [ ] requirements.txt updated
- [ ] Environment variables set
- [ ] Database configured
- [ ] File storage configured
- [ ] SSL certificate active
- [ ] Custom domain configured
- [ ] Monitoring enabled
- [ ] Error handling implemented

Your app will be available at: `https://your-app-name.herokuapp.com`
