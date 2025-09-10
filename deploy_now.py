#!/usr/bin/env python3
"""
Quick deployment script for Font Identifier
Automatically detects platform and provides deployment options
"""

import os
import sys
import subprocess
import platform
import webbrowser
from pathlib import Path

def print_banner():
    banner = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                         🚀 Font Identifier Deployment                       ║
║                                                                              ║
║           Deploy your AI-powered font identification app anywhere!           ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""
    print(banner)

def check_requirements():
    """Check if required files exist"""
    required_files = ['main.py', 'requirements.txt', 'Procfile', 'runtime.txt']
    missing_files = []
    
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Missing required files: {', '.join(missing_files)}")
        return False
    
    print("✅ All required files present")
    return True

def check_dependencies():
    """Check if required tools are installed"""
    tools = {
        'python': 'python --version',
        'git': 'git --version',
        'docker': 'docker --version'
    }
    
    available_tools = {}
    
    for tool, command in tools.items():
        try:
            result = subprocess.run(command.split(), capture_output=True, text=True)
            if result.returncode == 0:
                available_tools[tool] = True
                print(f"✅ {tool}: {result.stdout.strip()}")
            else:
                available_tools[tool] = False
                print(f"❌ {tool}: Not available")
        except FileNotFoundError:
            available_tools[tool] = False
            print(f"❌ {tool}: Not installed")
    
    return available_tools

def deploy_local():
    """Deploy locally for testing"""
    print("\n🏠 Starting Local Deployment...")
    
    try:
        # Start Streamlit
        print("Starting Streamlit server...")
        print("📱 App will be available at: http://localhost:8501")
        print("⏹️  Press Ctrl+C to stop the server")
        print("-" * 50)
        
        # Open browser
        webbrowser.open('http://localhost:8501')
        
        # Start Streamlit
        subprocess.run([
            sys.executable, '-m', 'streamlit', 'run', 'main.py',
            '--server.port=8501',
            '--server.address=localhost'
        ])
        
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting local server: {e}")

def deploy_streamlit_cloud():
    """Instructions for Streamlit Cloud deployment"""
    print("\n☁️ Streamlit Cloud Deployment")
    print("=" * 50)
    
    instructions = """
1. 📁 Push your code to GitHub:
   git init
   git add .
   git commit -m "Initial deployment"
   git remote add origin https://github.com/yourusername/font-identifier.git
   git push -u origin main

2. 🌐 Deploy to Streamlit Cloud:
   • Go to: https://share.streamlit.io
   • Sign in with GitHub
   • Click "New app"
   • Select your repository
   • Main file path: main.py
   • Click "Deploy!"

3. 🔐 Add secrets in Streamlit Cloud dashboard:
   SECRET_KEY = "your-production-secret-key"
   ENVIRONMENT = "production"

4. 🎉 Your app will be live at:
   https://your-app-name.streamlit.app
"""
    
    print(instructions)
    
    choice = input("🚀 Open Streamlit Cloud now? (y/n): ").lower()
    if choice == 'y':
        webbrowser.open('https://share.streamlit.io')

def deploy_heroku():
    """Instructions for Heroku deployment"""
    print("\n🚀 Heroku Deployment")
    print("=" * 50)
    
    # Check if Heroku CLI is available
    try:
        subprocess.run(['heroku', '--version'], capture_output=True, check=True)
        heroku_available = True
    except (FileNotFoundError, subprocess.CalledProcessError):
        heroku_available = False
    
    if not heroku_available:
        print("❌ Heroku CLI not found. Please install from:")
        print("   https://devcenter.heroku.com/articles/heroku-cli")
        return
    
    print("✅ Heroku CLI found")
    
    instructions = """
Quick Heroku Deployment:

1. 🔑 Login to Heroku:
   heroku login

2. 🏗️ Create app:
   heroku create your-font-identifier-app

3. 🗄️ Add database:
   heroku addons:create heroku-postgresql:mini

4. 🔧 Set environment variables:
   heroku config:set ENVIRONMENT=production
   heroku config:set SECRET_KEY=$(openssl rand -base64 32)

5. 🚀 Deploy:
   git add .
   git commit -m "Deploy to Heroku"
   git push heroku main

6. 📊 Scale:
   heroku ps:scale web=1

7. 🌐 Open app:
   heroku open
"""
    
    print(instructions)
    
    choice = input("🚀 Start Heroku deployment now? (y/n): ").lower()
    if choice == 'y':
        print("Starting Heroku deployment...")
        try:
            # Login
            subprocess.run(['heroku', 'login'])
            
            # Get app name
            app_name = input("Enter your app name (or press Enter for auto-generated): ").strip()
            if app_name:
                subprocess.run(['heroku', 'create', app_name])
            else:
                subprocess.run(['heroku', 'create'])
            
            # Add database
            subprocess.run(['heroku', 'addons:create', 'heroku-postgresql:mini'])
            
            # Set config
            subprocess.run(['heroku', 'config:set', 'ENVIRONMENT=production'])
            
            print("🎉 Heroku app created! Now run 'git push heroku main' to deploy")
            
        except Exception as e:
            print(f"❌ Error during Heroku setup: {e}")

def deploy_docker():
    """Docker deployment options"""
    print("\n🐳 Docker Deployment")
    print("=" * 50)
    
    # Check if Docker is available
    try:
        subprocess.run(['docker', '--version'], capture_output=True, check=True)
        docker_available = True
    except (FileNotFoundError, subprocess.CalledProcessError):
        docker_available = False
    
    if not docker_available:
        print("❌ Docker not found. Please install Docker Desktop:")
        print("   https://www.docker.com/products/docker-desktop")
        return
    
    print("✅ Docker found")
    
    options = """
Docker Deployment Options:

1. 🏠 Simple Local Docker:
   docker build -t font-identifier .
   docker run -p 8501:8501 font-identifier

2. 🔧 Docker Compose (Development):
   docker-compose up -d

3. 🏭 Production Docker (Full Stack):
   cp deploy/docker-compose.production.yml docker-compose.yml
   cp .env.production .env
   # Edit .env with your settings
   docker-compose up -d
"""
    
    print(options)
    
    choice = input("Choose option (1/2/3) or press Enter to skip: ").strip()
    
    if choice == '1':
        print("🔨 Building Docker image...")
        try:
            subprocess.run(['docker', 'build', '-t', 'font-identifier', '.'], check=True)
            print("🚀 Starting container...")
            print("📱 App will be available at: http://localhost:8501")
            webbrowser.open('http://localhost:8501')
            subprocess.run(['docker', 'run', '-p', '8501:8501', 'font-identifier'])
        except Exception as e:
            print(f"❌ Docker deployment failed: {e}")
    
    elif choice == '2':
        print("🔨 Starting Docker Compose...")
        try:
            subprocess.run(['docker-compose', 'up', '-d'], check=True)
            print("✅ Services started!")
            print("📱 App available at: http://localhost:8501")
            webbrowser.open('http://localhost:8501')
        except Exception as e:
            print(f"❌ Docker Compose failed: {e}")
    
    elif choice == '3':
        print("🏭 Setting up production Docker...")
        try:
            # Copy production files
            import shutil
            if os.path.exists('deploy/docker-compose.production.yml'):
                shutil.copy('deploy/docker-compose.production.yml', 'docker-compose.yml')
            if os.path.exists('.env.production'):
                shutil.copy('.env.production', '.env')
            
            print("✅ Production files copied")
            print("⚙️  Please edit .env file with your production settings")
            print("🚀 Then run: docker-compose up -d")
            
        except Exception as e:
            print(f"❌ Production setup failed: {e}")

def show_deployment_status():
    """Show current deployment status and options"""
    print("\n📊 Deployment Status")
    print("=" * 50)
    
    # Check if app is running locally
    try:
        import requests
        response = requests.get('http://localhost:8501', timeout=2)
        print("✅ Local app is running at http://localhost:8501")
    except:
        print("⭕ Local app is not running")
    
    # Check for deployment files
    deployment_files = {
        'Heroku': ['Procfile', 'runtime.txt'],
        'Docker': ['Dockerfile', 'docker-compose.yml'],
        'Streamlit Cloud': ['.streamlit/config.toml']
    }
    
    print("\n📁 Deployment Files:")
    for platform, files in deployment_files.items():
        all_exist = all(os.path.exists(f) for f in files)
        status = "✅" if all_exist else "⭕"
        print(f"  {status} {platform}: {', '.join(files)}")

def main():
    """Main deployment menu"""
    print_banner()
    
    # Check requirements
    if not check_requirements():
        print("\n❌ Please ensure all required files are present before deployment")
        sys.exit(1)
    
    # Check available tools
    print("\n🔍 Checking available deployment tools...")
    tools = check_dependencies()
    
    # Show current status
    show_deployment_status()
    
    # Deployment menu
    print("\n🚀 Deployment Options:")
    print("1. 🏠 Local Development (Start immediately)")
    print("2. ☁️ Streamlit Cloud (Free hosting)")
    print("3. 🚀 Heroku (Production ready)")
    print("4. 🐳 Docker (Any platform)")
    print("5. 📊 Show deployment status")
    print("6. 📖 Open deployment guide")
    print("0. ❌ Exit")
    
    while True:
        try:
            choice = input("\n👉 Select deployment option (0-6): ").strip()
            
            if choice == '0':
                print("👋 Goodbye!")
                break
            elif choice == '1':
                deploy_local()
            elif choice == '2':
                deploy_streamlit_cloud()
            elif choice == '3':
                deploy_heroku()
            elif choice == '4':
                deploy_docker()
            elif choice == '5':
                show_deployment_status()
            elif choice == '6':
                guide_path = Path('deploy/DEPLOYMENT_GUIDE.md')
                if guide_path.exists():
                    print(f"📖 Opening deployment guide: {guide_path.absolute()}")
                    if platform.system() == "Windows":
                        os.startfile(str(guide_path))
                    else:
                        subprocess.run(['open', str(guide_path)])
                else:
                    print("❌ Deployment guide not found")
            else:
                print("❌ Invalid option. Please choose 0-6.")
                
        except KeyboardInterrupt:
            print("\n\n👋 Deployment cancelled by user")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
