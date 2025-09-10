@echo off
echo ================================
echo Font Identifier - Build Package
echo ================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    pause
    exit /b 1
)

echo ✓ Python found
echo.

REM Run the build script
echo Starting build process...
python build.py %*

if %errorlevel% equ 0 (
    echo.
    echo ✅ Build completed successfully!
    echo Check the 'dist' folder for packages.
) else (
    echo.
    echo ❌ Build failed!
)

echo.
pause
