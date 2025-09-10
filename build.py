#!/usr/bin/env python3
"""
Build script for Font Identifier application
Creates distributable packages for different platforms
"""

import os
import shutil
import zipfile
import tarfile
import sys
import subprocess
from pathlib import Path
import argparse
from datetime import datetime

# Configuration
APP_NAME = "font-identifier"
VERSION = "1.0.0"
BUILD_DIR = "build"
DIST_DIR = "dist"

# Files to include in distribution
INCLUDE_FILES = [
    "main.py",
    "utils.py", 
    "requirements.txt",
    "README.md",
    "LICENSE",
    "data/",
    "static/",
    "config/",
    "install.bat",
    "install.sh",
    "Dockerfile",
    "docker-compose.yml",
    ".env.example"
]

# Files to exclude
EXCLUDE_PATTERNS = [
    "__pycache__/",
    "*.pyc",
    "*.pyo",
    ".git/",
    ".vscode/",
    ".idea/",
    "venv/",
    "env/",
    "build/",
    "dist/",
    "*.log",
    "app_users.db",
    "recordings/",
    "model.pth"  # Too large, user should download separately
]

def clean_build():
    """Clean build and dist directories"""
    print("🧹 Cleaning build directories...")
    
    for dir_path in [BUILD_DIR, DIST_DIR]:
        if os.path.exists(dir_path):
            shutil.rmtree(dir_path)
            print(f"   Removed {dir_path}/")
    
    os.makedirs(BUILD_DIR, exist_ok=True)
    os.makedirs(DIST_DIR, exist_ok=True)
    print("   Created fresh directories")

def should_include_file(file_path):
    """Check if file should be included in distribution"""
    file_str = str(file_path)
    
    for pattern in EXCLUDE_PATTERNS:
        if pattern.endswith('/'):
            if pattern[:-1] in file_str:
                return False
        else:
            if file_str.endswith(pattern) or pattern in file_str:
                return False
    
    return True

def copy_files():
    """Copy application files to build directory"""
    print("📁 Copying application files...")
    
    src_dir = Path(".")
    build_path = Path(BUILD_DIR) / APP_NAME
    
    # Create app directory in build
    build_path.mkdir(parents=True, exist_ok=True)
    
    copied_count = 0
    
    for item in INCLUDE_FILES:
        src_path = src_dir / item
        
        if src_path.is_file():
            dest_path = build_path / item
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src_path, dest_path)
            print(f"   📄 {item}")
            copied_count += 1
            
        elif src_path.is_dir():
            for file_path in src_path.rglob("*"):
                if file_path.is_file() and should_include_file(file_path):
                    rel_path = file_path.relative_to(src_dir)
                    dest_path = build_path / rel_path
                    dest_path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(file_path, dest_path)
                    copied_count += 1
            print(f"   📁 {item}/ ({len(list(src_path.rglob('*')))} files)")
    
    print(f"   Total: {copied_count} files copied")
    return build_path

def create_setup_files(build_path):
    """Create additional setup files"""
    print("⚙️  Creating setup files...")
    
    # Create .env.example if it doesn't exist
    env_example = build_path / ".env.example"
    if not env_example.exists():
        with open(env_example, "w") as f:
            f.write("""# Font Identifier Configuration
# Copy this file to .env and modify as needed

# Database
DB_PATH=app_users.db

# Model
MODEL_PATH=model.pth

# Server
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0

# Recording
RECORDINGS_DIR=recordings

# Payment Integration (Optional)
STRIPE_SECRET_KEY=
PAYPAL_CLIENT_ID=
PAYPAL_CLIENT_SECRET=

# Security (Change in production)
SECRET_KEY=your-secret-key-here
""")
    
    # Create LICENSE if it doesn't exist
    license_file = build_path / "LICENSE"
    if not license_file.exists():
        with open(license_file, "w") as f:
            f.write("""MIT License

Copyright (c) 2025 Font Identifier

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
""")
    
    # Create VERSION file
    version_file = build_path / "VERSION"
    with open(version_file, "w") as f:
        f.write(f"{VERSION}\n{datetime.now().isoformat()}\n")
    
    print("   ✓ Created setup files")

def create_zip_package(build_path):
    """Create ZIP package for Windows"""
    print("📦 Creating ZIP package...")
    
    zip_name = f"{APP_NAME}-{VERSION}-windows.zip"
    zip_path = Path(DIST_DIR) / zip_name
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in build_path.rglob("*"):
            if file_path.is_file():
                arcname = file_path.relative_to(Path(BUILD_DIR))
                zipf.write(file_path, arcname)
    
    size_mb = zip_path.stat().st_size / (1024 * 1024)
    print(f"   📦 {zip_name} ({size_mb:.1f} MB)")
    return zip_path

def create_tar_package(build_path):
    """Create TAR.GZ package for Linux/macOS"""
    print("📦 Creating TAR.GZ package...")
    
    tar_name = f"{APP_NAME}-{VERSION}-unix.tar.gz"
    tar_path = Path(DIST_DIR) / tar_name
    
    with tarfile.open(tar_path, 'w:gz') as tarf:
        tarf.add(build_path, arcname=APP_NAME)
    
    size_mb = tar_path.stat().st_size / (1024 * 1024)
    print(f"   📦 {tar_name} ({size_mb:.1f} MB)")
    return tar_path

def create_docker_package(build_path):
    """Create Docker image and save as tar"""
    print("🐳 Creating Docker package...")
    
    try:
        # Build Docker image
        result = subprocess.run([
            "docker", "build", 
            "-t", f"{APP_NAME}:{VERSION}", 
            "-f", "Dockerfile",
            "."
        ], capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"   ❌ Docker build failed: {result.stderr}")
            return None
        
        # Save Docker image as tar
        tar_name = f"{APP_NAME}-{VERSION}-docker.tar"
        tar_path = Path(DIST_DIR) / tar_name
        
        result = subprocess.run([
            "docker", "save",
            "-o", str(tar_path),
            f"{APP_NAME}:{VERSION}"
        ], capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"   ❌ Docker save failed: {result.stderr}")
            return None
        
        size_mb = tar_path.stat().st_size / (1024 * 1024)
        print(f"   🐳 {tar_name} ({size_mb:.1f} MB)")
        return tar_path
        
    except FileNotFoundError:
        print("   ⚠️  Docker not found, skipping Docker package")
        return None

def generate_checksums():
    """Generate checksums for all packages"""
    print("🔐 Generating checksums...")
    
    import hashlib
    
    checksums = {}
    
    for file_path in Path(DIST_DIR).glob("*"):
        if file_path.is_file() and not file_path.name.endswith(".md5"):
            with open(file_path, "rb") as f:
                content = f.read()
                md5_hash = hashlib.md5(content).hexdigest()
                sha256_hash = hashlib.sha256(content).hexdigest()
                
                checksums[file_path.name] = {
                    "md5": md5_hash,
                    "sha256": sha256_hash,
                    "size": len(content)
                }
    
    # Write checksums file
    checksums_file = Path(DIST_DIR) / "checksums.txt"
    with open(checksums_file, "w") as f:
        f.write(f"# Font Identifier {VERSION} - Package Checksums\n")
        f.write(f"# Generated: {datetime.now().isoformat()}\n\n")
        
        for filename, data in checksums.items():
            f.write(f"## {filename}\n")
            f.write(f"Size: {data['size']} bytes\n")
            f.write(f"MD5:  {data['md5']}\n")
            f.write(f"SHA256: {data['sha256']}\n\n")
    
    print(f"   ✓ Checksums written to checksums.txt")

def create_release_notes():
    """Create release notes"""
    print("📝 Creating release notes...")
    
    notes_file = Path(DIST_DIR) / "RELEASE_NOTES.md"
    with open(notes_file, "w") as f:
        f.write(f"""# Font Identifier {VERSION} - Release Notes

## 🚀 Installation Options

### 1. Quick Install (Recommended)
- **Windows**: Download `{APP_NAME}-{VERSION}-windows.zip`, extract and run `install.bat`
- **Linux/macOS**: Download `{APP_NAME}-{VERSION}-unix.tar.gz`, extract and run `./install.sh`

### 2. Docker
- **All Platforms**: `docker load < {APP_NAME}-{VERSION}-docker.tar`
- Then: `docker run -p 8501:8501 {APP_NAME}:{VERSION}`

### 3. Manual Installation
1. Extract the archive
2. Install Python 3.8+
3. Run: `pip install -r requirements.txt`
4. Run: `streamlit run main.py`

## 📱 Mobile Installation (PWA)
1. Open the app in your mobile browser
2. Add to Home Screen:
   - **iOS**: Tap share → "Add to Home Screen"
   - **Android**: Tap menu → "Add to Home Screen"

## ✨ What's New in {VERSION}

- 🎯 AI-powered font identification
- 🎥 Screen recording with audio
- 📱 Progressive Web App support
- 🐳 Docker containerization
- 💳 Payment integration
- 🔐 Secure user authentication
- 📊 Usage analytics and reporting

## 🛠️ System Requirements

- **OS**: Windows 10+, macOS 10.14+, Ubuntu 18.04+
- **Python**: 3.8 or higher
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 2GB free space

## 🆘 Support

- **Issues**: https://github.com/your-repo/issues
- **Email**: support@your-domain.com
- **Documentation**: Check the README.md file

## 🔐 Security

All packages have been verified with checksums. See `checksums.txt` for verification.

---

**Generated**: {datetime.now().isoformat()}
""")
    
    print("   📝 Release notes created")

def main():
    parser = argparse.ArgumentParser(description="Build Font Identifier packages")
    parser.add_argument("--clean", action="store_true", help="Clean build directories only")
    parser.add_argument("--no-docker", action="store_true", help="Skip Docker package creation")
    parser.add_argument("--zip-only", action="store_true", help="Create ZIP package only")
    parser.add_argument("--tar-only", action="store_true", help="Create TAR package only")
    
    args = parser.parse_args()
    
    print(f"🚀 Building Font Identifier {VERSION}")
    print("=" * 50)
    
    # Clean build directories
    clean_build()
    
    if args.clean:
        print("✅ Clean completed")
        return
    
    # Copy files to build directory
    build_path = copy_files()
    
    # Create additional setup files
    create_setup_files(build_path)
    
    # Create packages
    packages_created = []
    
    if not args.tar_only:
        zip_path = create_zip_package(build_path)
        if zip_path:
            packages_created.append(zip_path)
    
    if not args.zip_only:
        tar_path = create_tar_package(build_path)
        if tar_path:
            packages_created.append(tar_path)
    
    if not args.no_docker and not (args.zip_only or args.tar_only):
        docker_path = create_docker_package(build_path)
        if docker_path:
            packages_created.append(docker_path)
    
    # Generate checksums and release notes
    if packages_created:
        generate_checksums()
        create_release_notes()
    
    print("\n" + "=" * 50)
    print("✅ Build completed successfully!")
    print(f"📦 Packages created in {DIST_DIR}/:")
    
    for package_path in packages_created:
        size_mb = package_path.stat().st_size / (1024 * 1024)
        print(f"   • {package_path.name} ({size_mb:.1f} MB)")
    
    print(f"\n📋 Next steps:")
    print(f"   1. Test the packages on different platforms")
    print(f"   2. Upload to release platform (GitHub, etc.)")
    print(f"   3. Update download links in documentation")

if __name__ == "__main__":
    main()
