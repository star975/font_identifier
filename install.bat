@echo off
echo ================================
echo Font Identifier Installation
echo ================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo ✓ Python found
echo.

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv
if %errorlevel% neq 0 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)

echo ✓ Virtual environment created
echo.

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies
    echo Try running: pip install -r requirements.txt --no-cache-dir
    pause
    exit /b 1
)

echo ✓ Dependencies installed
echo.

REM Create necessary directories
echo Creating directories...
if not exist "recordings" mkdir recordings
if not exist "config" mkdir config
if not exist "static" mkdir static

echo ✓ Directories created
echo.

REM Check if model file exists
if not exist "model.pth" (
    echo WARNING: model.pth not found
    echo The app will create a dummy model, but you should add your trained model
    echo.
)

echo ================================
echo Installation Complete!
echo ================================
echo.
echo To start the application:
echo 1. Run: venv\Scripts\activate.bat
echo 2. Run: streamlit run main.py
echo 3. Open http://localhost:8501 in your browser
echo.
echo Or simply run: start.bat
echo.

REM Create start script
echo @echo off > start.bat
echo call venv\Scripts\activate.bat >> start.bat
echo echo Starting Font Identifier... >> start.bat
echo echo Open http://localhost:8501 in your browser >> start.bat
echo streamlit run main.py >> start.bat

echo ✓ Start script created (start.bat)
echo.

pause
