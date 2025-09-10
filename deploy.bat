@echo off
title Font Identifier - One-Click Deployment
color 0A

echo.
echo ╔══════════════════════════════════════════════════════════════════════════════╗
echo ║                         🚀 Font Identifier Deployment                       ║
echo ║                                                                              ║
echo ║           Deploy your AI-powered font identification app anywhere!           ║
echo ╚══════════════════════════════════════════════════════════════════════════════╝
echo.

echo 🔍 Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python not found! Please install Python 3.8+ from https://python.org
    echo.
    pause
    exit /b 1
)
echo ✅ Python found

echo.
echo 📦 Installing/updating dependencies...
pip install -r requirements.txt >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️  Some dependencies might have issues, but continuing...
)
echo ✅ Dependencies ready

echo.
echo 🚀 Deployment Options:
echo.
echo 1. 🏠 Local Development (Start immediately)
echo 2. 🌐 Open Streamlit Cloud (Free hosting)
echo 3. 🚀 Open Heroku Dashboard (Production)
echo 4. 📖 View Deployment Guide
echo 5. ❌ Exit
echo.

set /p choice="👉 Choose option (1-5): "

if "%choice%"=="1" goto local
if "%choice%"=="2" goto streamlit_cloud  
if "%choice%"=="3" goto heroku
if "%choice%"=="4" goto guide
if "%choice%"=="5" goto exit
goto invalid

:local
echo.
echo 🏠 Starting Local Deployment...
echo.
echo 📱 Your app will be available at: http://localhost:8501
echo ⏹️  Press Ctrl+C in the terminal to stop
echo.
echo 🌐 Opening browser...
timeout /t 2 >nul
start http://localhost:8501
echo.
echo 🚀 Starting Streamlit server...
python -m streamlit run main.py
goto end

:streamlit_cloud
echo.
echo ☁️ Opening Streamlit Cloud...
start https://share.streamlit.io
echo.
echo 📋 Quick Instructions:
echo 1. Sign in with GitHub
echo 2. Click "New app"
echo 3. Select your repository
echo 4. Set main file: main.py
echo 5. Click "Deploy!"
echo.
echo 💡 Don't forget to add secrets:
echo    SECRET_KEY = "your-secret-key-123"
echo    ENVIRONMENT = "production"
echo.
pause
goto end

:heroku
echo.
echo 🚀 Opening Heroku Dashboard...
start https://dashboard.heroku.com
echo.
echo 📋 Quick Instructions:
echo 1. Create new app
echo 2. Connect to GitHub repository
echo 3. Enable automatic deploys
echo 4. Add Heroku PostgreSQL addon
echo 5. Set environment variables in Settings
echo.
echo 💻 Or use Heroku CLI:
echo    heroku create your-app-name
echo    heroku addons:create heroku-postgresql:mini
echo    git push heroku main
echo.
pause
goto end

:guide
echo.
echo 📖 Opening Deployment Guide...
if exist "DEPLOY_NOW.md" (
    start DEPLOY_NOW.md
) else if exist "deploy\DEPLOYMENT_GUIDE.md" (
    start deploy\DEPLOYMENT_GUIDE.md
) else (
    echo ❌ Guide not found. Check the README.md file.
)
pause
goto end

:invalid
echo.
echo ❌ Invalid choice. Please select 1-5.
echo.
pause
goto start

:exit
echo.
echo 👋 Goodbye! Your Font Identifier app is ready to deploy anytime.
goto end

:end
echo.
echo ✅ Done! Thank you for using Font Identifier Deployment Tool.
echo.
pause
