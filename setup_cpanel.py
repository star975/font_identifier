#!/usr/bin/env python3
"""
Font Identifier - cPanel Setup Script
Automated deployment script for cPanel shared hosting
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
import json

class CPanelSetup:
    def __init__(self):
        self.app_name = "font_identifier"
        self.current_dir = Path.cwd()
        self.home_dir = Path.home()
        
    def print_header(self, message):
        print(f"\n{'='*60}")
        print(f"🚀 {message}")
        print(f"{'='*60}")
        
    def print_step(self, step, message):
        print(f"\n[{step}] {message}")
        
    def run_command(self, command, check=True):
        """Run shell command and return output"""
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True, check=check)
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            print(f"❌ Command failed: {command}")
            print(f"Error: {e.stderr}")
            return None
            
    def detect_environment(self):
        """Detect cPanel hosting environment"""
        self.print_header("Detecting Hosting Environment")
        
        # Common cPanel paths
        cpanel_paths = [
            '/usr/local/cpanel',
            '/var/cpanel',
            self.home_dir / 'public_html'
        ]
        
        self.is_cpanel = any(Path(path).exists() for path in cpanel_paths)
        
        # Get Python version
        python_version = self.run_command("python3 --version")
        self.python_version = python_version
        
        # Get current user
        self.username = self.run_command("whoami")
        
        # Detect public_html directory
        if (self.home_dir / 'public_html').exists():
            self.public_html = self.home_dir / 'public_html'
        else:
            self.public_html = self.current_dir
            
        print(f"✅ Environment detected:")
        print(f"   - cPanel hosting: {'Yes' if self.is_cpanel else 'No'}")
        print(f"   - Python version: {python_version}")
        print(f"   - Username: {self.username}")
        print(f"   - Public HTML: {self.public_html}")
        
    def create_directories(self):
        """Create necessary directories"""
        self.print_step("1", "Creating directory structure")
        
        directories = [
            'recordings',
            'config', 
            'static',
            'data',
            'logs',
            'backend/recordings'
        ]
        
        for dir_name in directories:
            dir_path = self.current_dir / dir_name
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"   ✅ Created: {dir_name}")
            
        # Set proper permissions
        self.run_command(f"chmod 755 recordings config static data logs")
        self.run_command(f"chmod 755 backend/recordings")
        
    def setup_virtual_environment(self):
        """Set up Python virtual environment"""
        self.print_step("2", "Setting up virtual environment")
        
        venv_path = self.current_dir / 'venv'
        
        if venv_path.exists():
            print("   ⚠️  Virtual environment already exists")
            return
            
        # Create virtual environment
        cmd = f"python3 -m venv {venv_path}"
        if self.run_command(cmd):
            print("   ✅ Virtual environment created")
            
            # Activate and upgrade pip
            pip_path = venv_path / 'bin' / 'pip'
            self.run_command(f"{pip_path} install --upgrade pip setuptools wheel")
            print("   ✅ Pip upgraded")
        else:
            print("   ❌ Failed to create virtual environment")
            
    def install_dependencies(self):
        """Install Python dependencies"""
        self.print_step("3", "Installing dependencies")
        
        venv_pip = self.current_dir / 'venv' / 'bin' / 'pip'
        
        # Choose requirements file
        if (self.current_dir / 'requirements_full.txt').exists():
            requirements_file = 'requirements_full.txt'
        elif (self.current_dir / 'requirements.txt').exists():
            requirements_file = 'requirements.txt'
        else:
            print("   ❌ No requirements file found")
            return
            
        print(f"   📦 Installing from {requirements_file}...")
        
        # Install with timeout for shared hosting
        cmd = f"timeout 300 {venv_pip} install --no-cache-dir -r {requirements_file}"
        result = self.run_command(cmd, check=False)
        
        if result is not None:
            print("   ✅ Dependencies installed")
        else:
            print("   ⚠️  Some dependencies may have failed - check logs")
            
    def create_wsgi_file(self):
        """Create WSGI entry point"""
        self.print_step("4", "Creating WSGI configuration")
        
        wsgi_content = f'''#!/usr/bin/env python3
"""
WSGI Entry Point for Font Identifier
Optimized for cPanel shared hosting
"""

import sys
import os
from pathlib import Path

# Add application directory to Python path
app_dir = Path(__file__).parent
sys.path.insert(0, str(app_dir))

# Activate virtual environment
activate_this = app_dir / 'venv' / 'bin' / 'activate_this.py'
if activate_this.exists():
    exec(open(activate_this).read(), {{'__file__': str(activate_this)}})

# Set environment variables for shared hosting
os.environ.update({{
    'STREAMLIT_SERVER_HEADLESS': 'true',
    'STREAMLIT_SERVER_PORT': '8501', 
    'STREAMLIT_SERVER_ADDRESS': '127.0.0.1',
    'STREAMLIT_BROWSER_GATHER_USAGE_STATS': 'false',
    'STREAMLIT_SERVER_ENABLE_CORS': 'true',
    'STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION': 'false',
    'PYTHONPATH': str(app_dir),
    'TORCH_HOME': str(app_dir / 'torch_cache'),
    'MPLBACKEND': 'Agg',
    'OMP_NUM_THREADS': '1'
}})

def application(environ, start_response):
    """WSGI application entry point"""
    try:
        # Import Streamlit (must be after env vars are set)
        import streamlit.web.cli as stcli
        from streamlit import config as st_config
        
        # Configure Streamlit for shared hosting
        st_config.set_option('server.headless', True)
        st_config.set_option('server.enableCORS', True)
        st_config.set_option('server.enableXsrfProtection', False)
        st_config.set_option('browser.gatherUsageStats', False)
        st_config.set_option('server.maxUploadSize', 10)  # 10MB limit
        
        # Determine which main file to use
        main_file = 'main_full.py' if (app_dir / 'main_full.py').exists() else 'main.py'
        
        # Start Streamlit app
        sys.argv = ['streamlit', 'run', str(app_dir / main_file)]
        stcli.main()
        
    except Exception as e:
        # Fallback error response
        status = '500 Internal Server Error'
        headers = [('Content-type', 'text/html')]
        start_response(status, headers)
        
        error_html = f"""
        <html><body>
        <h1>Application Error</h1>
        <p>Error: {{str(e)}}</p>
        <p>Please check the application logs.</p>
        </body></html>
        """
        return [error_html.encode('utf-8')]
        
    # Should not reach here, but just in case
    status = '200 OK'
    headers = [('Content-type', 'text/plain')]
    start_response(status, headers)
    return [b'Font Identifier Starting...']

# For testing
if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    httpd = make_server('', 8000, application)
    print("Serving on port 8000...")
    httpd.serve_forever()
'''
        
        wsgi_path = self.current_dir / 'wsgi.py'
        wsgi_path.write_text(wsgi_content)
        self.run_command(f"chmod 644 {wsgi_path}")
        print("   ✅ WSGI file created")
        
    def create_htaccess(self):
        """Create .htaccess for URL rewriting"""
        self.print_step("5", "Creating .htaccess configuration")
        
        htaccess_content = '''# Font Identifier - cPanel Configuration
RewriteEngine On

# Redirect to WSGI application
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule ^(.*)$ /font_identifier/wsgi.py/$1 [QSA,L]

# Security headers
<IfModule mod_headers.c>
    Header always set X-Frame-Options DENY
    Header always set X-Content-Type-Options nosniff
    Header always set X-XSS-Protection "1; mode=block"
    Header always set Referrer-Policy "strict-origin-when-cross-origin"
</IfModule>

# Prevent access to sensitive files
<FilesMatch "\\.(db|log|pth|py)$">
    Order allow,deny
    Deny from all
</FilesMatch>

# Allow static files
<FilesMatch "\\.(css|js|png|jpg|jpeg|gif|ico|svg)$">
    Order allow,deny
    Allow from all
</FilesMatch>
'''
        
        htaccess_path = self.current_dir / '.htaccess'
        htaccess_path.write_text(htaccess_content)
        print("   ✅ .htaccess created")
        
    def create_config_files(self):
        """Create application configuration files"""
        self.print_step("6", "Creating configuration files")
        
        # Create a simple font list if it doesn't exist
        fontlist_path = self.current_dir / 'data' / 'fontlist.txt'
        if not fontlist_path.exists():
            fonts = [
                "Arial", "Helvetica", "Times New Roman", "Calibri", "Verdana",
                "Georgia", "Comic Sans MS", "Trebuchet MS", "Impact", "Palatino"
            ]
            fontlist_path.write_text('\\n'.join(fonts))
            print("   ✅ Default font list created")
            
        # Create empty model file if needed  
        model_path = self.current_dir / 'model.pth'
        if not model_path.exists():
            model_path.touch()
            print("   ✅ Empty model file created")
            
        # Create database file if needed
        db_path = self.current_dir / 'app_users.db'
        if not db_path.exists():
            db_path.touch()
            self.run_command(f"chmod 600 {db_path}")
            print("   ✅ Database file created")
            
    def create_startup_script(self):
        """Create startup script for the application"""
        self.print_step("7", "Creating startup script")
        
        startup_content = f'''#!/bin/bash
# Font Identifier Startup Script for cPanel

SCRIPT_DIR="$(cd "$(dirname "${{BASH_SOURCE[0]}}")" && pwd)"
cd "$SCRIPT_DIR"

# Activate virtual environment
source venv/bin/activate

# Set environment variables
export STREAMLIT_SERVER_HEADLESS=true
export STREAMLIT_SERVER_PORT=8501
export STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
export PYTHONPATH="$SCRIPT_DIR"

# Choose main file
if [ -f "main_full.py" ]; then
    MAIN_FILE="main_full.py"
else
    MAIN_FILE="main.py"
fi

echo "Starting Font Identifier..."
echo "Using file: $MAIN_FILE"

# Start the application
python -m streamlit run "$MAIN_FILE" \\
    --server.address=0.0.0.0 \\
    --server.port=8501 \\
    --server.headless=true \\
    --server.enableCORS=true \\
    --browser.gatherUsageStats=false

'''
        
        startup_path = self.current_dir / 'start.sh'
        startup_path.write_text(startup_content)
        self.run_command(f"chmod +x {startup_path}")
        print("   ✅ Startup script created")
        
    def finalize_setup(self):
        """Final setup steps"""
        self.print_step("8", "Finalizing setup")
        
        # Set final permissions
        self.run_command("find . -type f -name '*.py' -exec chmod 644 {} \\;")
        self.run_command("find . -type d -exec chmod 755 {} \\;")
        
        # Create logs directory
        logs_dir = self.current_dir / 'logs'
        logs_dir.mkdir(exist_ok=True)
        self.run_command(f"chmod 755 {logs_dir}")
        
        print("   ✅ Permissions set")
        print("   ✅ Setup completed!")
        
    def print_summary(self):
        """Print deployment summary"""
        self.print_header("Deployment Summary")
        
        print("✅ Font Identifier has been set up for cPanel hosting!")
        print("\\n📁 Files created:")
        print("   - wsgi.py (WSGI entry point)")
        print("   - .htaccess (URL configuration)")  
        print("   - start.sh (startup script)")
        print("   - venv/ (virtual environment)")
        print("\\n🚀 Next steps:")
        print("   1. Configure your domain to point to this directory")
        print("   2. Set up Python app in cPanel (if available)")
        print("   3. Or run: ./start.sh")
        print("   4. Access your app via your domain")
        print("\\n📚 For detailed instructions, see: CPANEL_DEPLOYMENT.md")
        
    def run(self):
        """Run the complete setup process"""
        try:
            self.print_header("Font Identifier - cPanel Setup")
            print("This script will configure your app for cPanel hosting")
            
            self.detect_environment()
            self.create_directories()
            self.setup_virtual_environment()
            self.install_dependencies()
            self.create_wsgi_file()
            self.create_htaccess()
            self.create_config_files()
            self.create_startup_script()
            self.finalize_setup()
            self.print_summary()
            
        except KeyboardInterrupt:
            print("\\n❌ Setup cancelled by user")
        except Exception as e:
            print(f"\\n❌ Setup failed: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    setup = CPanelSetup()
    setup.run()
