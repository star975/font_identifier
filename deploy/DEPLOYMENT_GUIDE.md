# 🚀 Font Identifier - Complete Deployment Guide

This guide covers all deployment options for your Font Identifier application, from local testing to production deployment.

## 📋 Quick Deployment Options

| Platform | Difficulty | Cost | Best For |
|----------|------------|------|----------|
| [Streamlit Cloud](#streamlit-cloud) | ⭐ Easy | Free | Quick demos, prototypes |
| [Heroku](#heroku) | ⭐⭐ Medium | Free/Paid | Small to medium apps |
| [Railway](#railway) | ⭐⭐ Medium | Free/Paid | Modern cloud deployment |
| [Docker](#docker-deployment) | ⭐⭐⭐ Hard | Variable | Any platform, full control |
| [VPS/Server](#vps-deployment) | ⭐⭐⭐⭐ Expert | $5+/month | Production, full control |

## 🌩️ Streamlit Cloud Deployment

**Perfect for**: Quick deployment, demos, free hosting

### Prerequisites
- GitHub account
- GitHub repository with your code

### Quick Steps
1. **Push to GitHub**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/star975/font-identifier.git
   git push -u origin main
   ```

2. **Deploy**:
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub
   - Click "New app"
   - Select your repository
   - Click "Deploy!"

3. **Configure Secrets** (in Streamlit Cloud dashboard):
   ```toml
   SECRET_KEY = "your-production-secret-key"
   ENVIRONMENT = "production"
   ```

**Your app will be at**: `https://your-app-name.streamlit.app`

---

## 🚀 Heroku Deployment

**Perfect for**: Production apps, custom domains, databases

### Prerequisites
- [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)
- Git repository

### Quick Steps

1. **Create Required Files** (already created for you):
   - `Procfile`
   - `runtime.txt`
   - Updated `requirements.txt`

2. **Deploy**:
   ```bash
   # Login to Heroku
   heroku login
   
   # Create app
   heroku create your-font-identifier-app
   
   # Add database
   heroku addons:create heroku-postgresql:mini
   
   # Set environment variables
   heroku config:set ENVIRONMENT=production
   heroku config:set SECRET_KEY=$(openssl rand -base64 32)
   
   # Deploy
   git push heroku main
   
   # Scale
   heroku ps:scale web=1
   ```

3. **Add Custom Domain** (optional):
   ```bash
   heroku domains:add yourdomain.com
   heroku domains:add www.yourdomain.com
   ```

**Your app will be at**: `https://your-app-name.herokuapp.com`

---

## 🐳 Docker Deployment

**Perfect for**: Any platform, local development, full control

### Option 1: Simple Docker

```bash
# Build and run locally
docker build -t font-identifier .
docker run -p 8501:8501 font-identifier
```

### Option 2: Docker Compose (Development)

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

### Option 3: Production Docker (Full Stack)

```bash
# Copy production compose file
cp deploy/docker-compose.production.yml docker-compose.yml

# Create environment file
cp .env.example .env
# Edit .env with your settings

# Start production stack
docker-compose up -d

# Check status
docker-compose ps
```

**Your app will be at**: `http://localhost` (or your domain)

---

## 🖥️ VPS/Server Deployment

**Perfect for**: Production, full control, custom configurations

### Supported Systems
- Ubuntu 18.04+
- CentOS 7+
- Debian 9+
- Any systemd-based Linux

### One-Command Deployment

```bash
# Copy deployment script to your server
scp deploy/vps_deploy.sh user@your-server.com:~/

# SSH to your server
ssh user@your-server.com

# Run deployment (replace with your domain)
sudo bash vps_deploy.sh --domain yourdomain.com --email your-email@domain.com

# For localhost deployment
sudo bash vps_deploy.sh
```

### Manual VPS Setup

If you prefer manual setup, follow the detailed instructions in `deploy/vps_deploy.sh`.

**Your app will be at**: `https://yourdomain.com`

---

## 🎯 Railway Deployment

**Perfect for**: Modern cloud deployment, GitHub integration

### Quick Steps

1. **Connect GitHub**:
   - Go to [railway.app](https://railway.app)
   - Sign in with GitHub
   - Import your repository

2. **Configure**:
   - Add environment variables
   - Set build command: `pip install -r requirements.txt`
   - Set start command: `streamlit run main.py --server.port=$PORT`

3. **Deploy**:
   - Railway automatically deploys on git push

**Your app will be at**: `https://your-app.railway.app`

---

## ⚙️ Environment Configuration

### Required Environment Variables

```env
# Basic Configuration
ENVIRONMENT=production
SECRET_KEY=your-secret-key-here

# Server Settings
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
STREAMLIT_SERVER_HEADLESS=true

# Database (for production)
DATABASE_URL=postgresql://user:pass@host:port/dbname

# Optional: Payment Integration
STRIPE_SECRET_KEY=sk_live_...
PAYPAL_CLIENT_SECRET=...

# Optional: File Storage
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
S3_BUCKET_NAME=your-bucket
```

### Creating Environment Files

```bash
# Copy template
cp .env.example .env

# Edit with your settings
nano .env
```

---

## 📊 Monitoring & Maintenance

### Health Checks

All deployments include health check endpoints:
- `/_stcore/health` - Streamlit health
- `/_health` - Custom health check

### Monitoring Options

1. **Built-in Logs**:
   ```bash
   # Heroku
   heroku logs --tail
   
   # Docker
   docker-compose logs -f
   
   # VPS/SystemD
   journalctl -u font-identifier -f
   ```

2. **External Monitoring**:
   - [UptimeRobot](https://uptimerobot.com) - Free uptime monitoring
   - [Pingdom](https://pingdom.com) - Advanced monitoring
   - [New Relic](https://newrelic.com) - APM monitoring

### Backups

For production deployments:

```bash
# VPS - Manual backup
/opt/font-identifier/backup.sh

# Docker - Backup volumes
docker-compose exec postgres pg_dump -U font_user font_identifier > backup.sql

# Heroku - Database backup
heroku pg:backups:capture
heroku pg:backups:download
```

---

## 🔒 Security Checklist

### Before Going Live

- [ ] Change default SECRET_KEY
- [ ] Use strong database passwords
- [ ] Enable SSL/HTTPS
- [ ] Configure firewall rules
- [ ] Set up fail2ban (VPS)
- [ ] Enable rate limiting
- [ ] Remove debug flags
- [ ] Set up regular backups
- [ ] Configure monitoring

### Production Environment Variables

```env
# Security
SECRET_KEY=complex-random-key-here
ENVIRONMENT=production
DEBUG=false

# SSL/Security Headers (handled by reverse proxy)
FORCE_HTTPS=true
SESSION_COOKIE_SECURE=true
```

---

## 🚨 Troubleshooting

### Common Issues

**1. App won't start**
```bash
# Check logs
docker-compose logs font-identifier
heroku logs --tail
journalctl -u font-identifier -f

# Common fixes
- Check requirements.txt
- Verify Python version
- Check environment variables
```

**2. Database connection errors**
```bash
# Check database URL
echo $DATABASE_URL

# Test connection
psql $DATABASE_URL
```

**3. Static files not loading**
```bash
# Check static file paths
ls -la static/
# Update Nginx configuration
# Clear browser cache
```

**4. High memory usage**
```bash
# Optimize PyTorch model
- Use CPU-only version
- Enable model quantization
- Add memory limits
```

### Performance Optimization

```python
# Add to main.py for production
@st.cache_resource
def load_model():
    # Your model loading code
    return model

@st.cache_data
def preprocess_image(image):
    # Your preprocessing code
    return processed_image

# Memory management
import gc
gc.collect()
```

---

## 📈 Scaling Options

### Horizontal Scaling

1. **Load Balancer + Multiple Instances**:
   ```bash
   # Docker Swarm
   docker service create --replicas 3 font-identifier
   
   # Heroku
   heroku ps:scale web=3
   ```

2. **Database Scaling**:
   - Read replicas
   - Connection pooling
   - Redis caching

### Vertical Scaling

1. **Increase Resources**:
   ```bash
   # Heroku
   heroku ps:resize web=standard-2x
   
   # Docker
   docker-compose up --scale font-identifier=2
   ```

---

## 📞 Support

### Getting Help

- **Issues**: [GitHub Issues](https://github.com/your-username/font-identifier/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-username/font-identifier/discussions)
- **Email**: support@yourdomain.com

### Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -m 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Submit pull request

---

## 🎉 Success!

Your Font Identifier app is now deployed! 

### Next Steps

1. **Test thoroughly** on different devices
2. **Set up monitoring** and alerts
3. **Configure backups** for production
4. **Add custom domain** and SSL
5. **Monitor performance** and optimize as needed

**Happy deploying! 🚀**
