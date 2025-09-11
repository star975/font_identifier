#!/usr/bin/env python3
"""
Create cPanel Deployment Package
Creates a ZIP file ready for upload to cPanel hosting
"""

import os
import sys
import shutil
from pathlib import Path
from zipfile import ZipFile
from datetime import datetime

class CPanelPackager:
    def __init__(self):
        self.current_dir = Path.cwd()
        self.package_name = f"font_identifier_cpanel_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
        
    def print_header(self, message):
        print(f"\n{'='*60}")
        print(f"📦 {message}")
        print(f"{'='*60}")
        
    def create_deployment_package(self):
        """Create deployment package for cPanel"""
        self.print_header("Creating cPanel Deployment Package")
        
        # Files to include in the package
        essential_files = [
            'main_full.py',           # Full application (backup)
            'main.py',                # Production application
            'requirements_full.txt',   # Full dependencies
            'requirements.txt',        # Production requirements
            'setup_cpanel.py',         # Setup script
            'CPANEL_DEPLOYMENT.md',    # Documentation
            'model_config.py',         # Model configuration
            'app_users.db',           # Database (if exists)
            'model.pth',              # Model file (if exists)
        ]
        
        # Directories to include
        essential_dirs = [
            '.streamlit',
            'data',
            'static',
            'config'
        ]
        
        # Files to exclude (will be created during setup)
        exclude_patterns = [
            '__pycache__',
            '*.pyc', 
            '.git',
            'venv',
            'node_modules',
            'recordings',
            'logs',
            '.DS_Store',
            'Thumbs.db',
            '*.log'
        ]
        
        package_path = self.current_dir / self.package_name
        
        print(f"Creating package: {self.package_name}")
        
        with ZipFile(package_path, 'w') as zipf:
            # Add essential files
            for file_name in essential_files:
                file_path = self.current_dir / file_name
                if file_path.exists():
                    zipf.write(file_path, file_name)
                    print(f"   ✅ Added: {file_name}")
                else:
                    print(f"   ⚠️  Skipped (not found): {file_name}")
            
            # Add essential directories
            for dir_name in essential_dirs:
                dir_path = self.current_dir / dir_name
                if dir_path.exists() and dir_path.is_dir():
                    for file_path in dir_path.rglob('*'):
                        if file_path.is_file():
                            # Check if file should be excluded
                            should_exclude = any(
                                pattern in str(file_path) for pattern in exclude_patterns
                            )
                            if not should_exclude:
                                arc_name = file_path.relative_to(self.current_dir)
                                zipf.write(file_path, arc_name)
                    print(f"   ✅ Added directory: {dir_name}")
                else:
                    print(f"   ⚠️  Skipped (not found): {dir_name}")
        
        print(f"\n✅ Package created: {package_path}")
        print(f"   Size: {package_path.stat().st_size / 1024 / 1024:.2f} MB")
        
        return package_path
        
    def create_installation_instructions(self):
        """Create step-by-step installation instructions"""
        instructions = f"""
# 🚀 Font Identifier - cPanel Installation Instructions

## Package Information
- **Package**: {self.package_name}
- **Created**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **Version**: Font Identifier v1.0

## 📋 Installation Steps

### Step 1: Upload Package
1. **Login to cPanel**
2. **Go to File Manager**
3. **Navigate** to your domain directory (e.g., `public_html/yourdomain.com`)
4. **Upload** the ZIP package: `{self.package_name}`
5. **Extract** the ZIP file
6. **Delete** the ZIP file after extraction

### Step 2: Connect via SSH (Recommended)
```bash
# Connect to your server
ssh username@yourdomain.com

# Navigate to your app directory
cd public_html/yourdomain.com/font_identifier

# Run the setup script
python3 setup_cpanel.py
```

### Step 3: Alternative - Manual Setup
If SSH is not available:
1. **cPanel → Software → Python**
2. **Create New Python App**
3. **Set Python Version**: 3.9+
4. **Set App Directory**: `/home/username/public_html/yourdomain.com/font_identifier`
5. **Set Startup File**: `wsgi.py`
6. **Install Dependencies** via cPanel Python interface

### Step 4: Configure Domain
1. **Point domain/subdomain** to the font_identifier directory
2. **Or configure as subdirectory**: `yourdomain.com/font_identifier`

### Step 5: Test Installation
1. **Visit your domain** in browser
2. **Check for errors** in cPanel Error Logs
3. **View application logs** in `logs/` directory

## 🔧 Configuration Options

### Environment Variables (Optional)
Set these in cPanel or hosting control panel:
- `MODEL_DOWNLOAD_URL`: URL to download trained model
- `STREAMLIT_SERVER_PORT`: Port number (default: 8501)
- `PYTHONPATH`: Application directory path

### Database Configuration
- Default: SQLite (`app_users.db`)
- Production: Configure PostgreSQL in cPanel if available

## 📞 Troubleshooting

### Common Issues:
1. **Python version mismatch**: Ensure Python 3.9+ is available
2. **Permission errors**: Run `chmod +x setup_cpanel.py`
3. **Module not found**: Ensure virtual environment is activated
4. **Memory limits**: Contact hosting provider about Python app resources

### Support Resources:
- **Hosting Documentation**: Check your provider's Python app guide
- **Application Logs**: Check `logs/font_identifier.log`
- **cPanel Logs**: Error logs in cPanel interface

## 🎯 Next Steps After Installation

1. **Test basic functionality** with production version
2. **Restore full application** by using `main_full.py`
3. **Configure model file** or set `MODEL_DOWNLOAD_URL`
4. **Set up user authentication** and customize as needed

## 📚 Additional Resources

- **Full Documentation**: `CPANEL_DEPLOYMENT.md`
- **Model Configuration**: `model_config.py`
- **Startup Script**: `start.sh`

---
**Created by Font Identifier cPanel Packager**
"""
        
        instructions_path = self.current_dir / f"INSTALLATION_INSTRUCTIONS_{datetime.now().strftime('%Y%m%d')}.md"
        instructions_path.write_text(instructions, encoding='utf-8')
        print(f"✅ Instructions created: {instructions_path}")
        return instructions_path

def main():
    print("🚀 Font Identifier - cPanel Package Creator")
    print("This script creates a deployment package for cPanel hosting")
    
    packager = CPanelPackager()
    
    # Create the deployment package
    package_path = packager.create_deployment_package()
    
    # Create installation instructions
    instructions_path = packager.create_installation_instructions()
    
    print(f"\n{'='*60}")
    print("📦 Package Creation Complete!")
    print(f"{'='*60}")
    print(f"\n📁 Files created:")
    print(f"   - {package_path.name}")
    print(f"   - {instructions_path.name}")
    
    print(f"\n🚀 Next steps:")
    print(f"   1. Download: {package_path.name}")
    print(f"   2. Read: {instructions_path.name}")
    print(f"   3. Upload to your cPanel hosting")
    print(f"   4. Extract and run setup_cpanel.py")
    
    print(f"\n💡 Hosting providers that support Python:")
    print("   - A2 Hosting, SiteGround, InMotion Hosting")
    print("   - Hostinger, Bluehost (check plan)")
    print("   - Any shared host with Python 3.9+ support")

if __name__ == "__main__":
    main()
