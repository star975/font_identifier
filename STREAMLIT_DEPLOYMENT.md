# 🚀 Streamlit Cloud Deployment Guide - Font Identifier

## 📋 Quick Setup Checklist

### 1. Repository Preparation
- [x] Code is ready in GitHub repository
- [x] `.streamlit/config.toml` configured
- [x] Production configuration added to `main.py`
- [x] `.gitignore` created to exclude secrets

### 2. Handle Large Model File (103MB)

**Option A: Upload to Cloud Storage (Recommended)**
```bash
# Upload model.pth to Google Drive, Dropbox, or AWS S3
# Get a direct download URL
# Example for Google Drive: 
# https://drive.google.com/uc?export=download&id=YOUR_FILE_ID
```

**Option B: Use Git LFS (if repository supports it)**
```bash
git lfs track "*.pth"
git add .gitattributes
git add model.pth
git commit -m "Add model with Git LFS"
```

**Option C: Deploy without model (uses dummy model)**
- The app will automatically use a dummy model for demonstration
- Font identification will show placeholder results

### 3. Deploy to Streamlit Cloud

1. **Go to** [share.streamlit.io](https://share.streamlit.io)
2. **Sign in** with your GitHub account
3. **Click** "New app"
4. **Select repository**: `star975/font_identifier`
5. **Set main file path**: `main.py`
6. **Click** "Advanced settings" and configure:

### 4. Configure Secrets in Streamlit Cloud

In the "Advanced settings" → "Secrets" section, add:

```toml
ENVIRONMENT = "production"
SECRET_KEY = "your-random-secret-key-here"

# Optional: If you uploaded model to cloud storage
MODEL_URL = "https://your-cloud-storage-url/model.pth"

# Optional: Database for production (SQLite will reset on each deployment)
DATABASE_URL = "postgresql://user:pass@host:port/dbname"

# Optional: Payment integration
STRIPE_SECRET_KEY = "sk_live_..."
PAYPAL_CLIENT_SECRET = "..."
```

### 5. Deploy!

Click **"Deploy!"** and wait for the deployment to complete.

## 🔧 Configuration Details

### Environment Variables Available

| Variable | Description | Required |
|----------|-------------|----------|
| `ENVIRONMENT` | Set to "production" for cloud deployment | Yes |
| `SECRET_KEY` | Random secret key for sessions | Yes |
| `MODEL_URL` | Direct URL to download model.pth | No* |
| `DATABASE_URL` | PostgreSQL connection string | No |
| `STRIPE_SECRET_KEY` | Stripe payment integration | No |
| `PAYPAL_CLIENT_SECRET` | PayPal payment integration | No |

*Required only if model.pth is not in the repository

### Local Development

For local development, copy `.streamlit/secrets.toml.example`:

```bash
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# Edit the values as needed
```

## 🎯 Production Optimizations

The app automatically enables these optimizations in production:
- ✅ Headless mode
- ✅ File watcher disabled
- ✅ CORS disabled
- ✅ Optimized for cloud environment

## 🔗 Your Live App

After deployment, your app will be available at:
```
https://font-identifier-[random-hash].streamlit.app
```

## 🆘 Troubleshooting

### Common Issues

1. **Model not loading**
   - Check if MODEL_URL is correctly set in secrets
   - Verify the URL is a direct download link
   - App will use dummy model if real model fails to load

2. **Database resets on deployment**
   - This is normal with SQLite on Streamlit Cloud
   - Use PostgreSQL DATABASE_URL for persistent storage

3. **App won't start**
   - Check the logs in Streamlit Cloud dashboard
   - Verify all required dependencies are in requirements.txt

4. **Memory issues**
   - Model loading uses significant memory
   - Consider using model quantization for smaller model size

### Support

For deployment issues:
- Check Streamlit Cloud dashboard logs
- Visit [Streamlit Community Forum](https://discuss.streamlit.io/)
- Create an issue in this repository

## 📊 Monitoring

Monitor your deployed app:
- **Streamlit Cloud Dashboard**: View logs, resource usage
- **GitHub**: Track repository activity and issues
- **User Analytics**: Monitor app usage patterns

---

**Deployment Date**: Generated automatically
**Last Updated**: Check git commit history