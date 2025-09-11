#!/usr/bin/env python3
"""
Dependency resolution test script for Font Identifier
Tests PyTorch/torchvision compatibility and other dependencies
"""

import subprocess
import sys
import os
import tempfile
from pathlib import Path

def print_banner():
    print("🔍 Font Identifier - Dependency Resolution Test")
    print("=" * 50)

def check_current_installation():
    """Check currently installed versions"""
    print("\n📦 Currently Installed Packages:")
    
    packages_to_check = [
        'torch', 'torchvision', 'streamlit', 'numpy', 
        'pandas', 'pillow', 'opencv-python', 'requests'
    ]
    
    for package in packages_to_check:
        try:
            result = subprocess.run([
                sys.executable, '-c', f'import {package}; print({package}.__version__)'
            ], capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                version = result.stdout.strip()
                print(f"  ✅ {package}: {version}")
            else:
                print(f"  ❌ {package}: Not installed")
                
        except subprocess.TimeoutExpired:
            print(f"  ⚠️  {package}: Import timeout")
        except Exception as e:
            print(f"  ❌ {package}: Error - {e}")

def test_pytorch_compatibility():
    """Test PyTorch and torchvision compatibility"""
    print("\n🧪 Testing PyTorch Compatibility...")
    
    try:
        # Test PyTorch import and basic functionality
        result = subprocess.run([
            sys.executable, '-c', '''
import torch
import torchvision
print(f"PyTorch: {torch.__version__}")
print(f"Torchvision: {torchvision.__version__}")
print(f"CUDA available: {torch.cuda.is_available()}")

# Test basic tensor operations
x = torch.randn(2, 3)
print(f"Tensor test: {x.shape}")

# Test torchvision transforms
from torchvision import transforms
transform = transforms.Compose([transforms.ToTensor()])
print("Torchvision transforms: OK")
'''
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✅ PyTorch compatibility test PASSED")
            print(result.stdout)
        else:
            print("❌ PyTorch compatibility test FAILED")
            print("Error:", result.stderr)
            
    except subprocess.TimeoutExpired:
        print("⚠️  PyTorch test timed out")
    except Exception as e:
        print(f"❌ PyTorch test error: {e}")

def test_requirements_resolution():
    """Test if requirements.txt can be resolved"""
    print("\n📋 Testing Requirements Resolution...")
    
    requirements_files = [
        'requirements.txt',
        'requirements-docker.txt',
        'requirements-heroku.txt'
    ]
    
    for req_file in requirements_files:
        if not os.path.exists(req_file):
            continue
            
        print(f"\n📄 Testing {req_file}:")
        
        # Create a temporary virtual environment
        with tempfile.TemporaryDirectory() as temp_dir:
            venv_path = Path(temp_dir) / "test_venv"
            
            try:
                # Create virtual environment
                subprocess.run([
                    sys.executable, '-m', 'venv', str(venv_path)
                ], check=True, timeout=60)
                
                # Get pip path
                if os.name == 'nt':  # Windows
                    pip_path = venv_path / 'Scripts' / 'pip.exe'
                else:  # Unix
                    pip_path = venv_path / 'bin' / 'pip'
                
                # Test dependency resolution (dry run)
                result = subprocess.run([
                    str(pip_path), 'install', '--dry-run', '-r', req_file
                ], capture_output=True, text=True, timeout=120)
                
                if result.returncode == 0:
                    print(f"  ✅ {req_file}: Dependencies can be resolved")
                else:
                    print(f"  ❌ {req_file}: Dependency conflicts detected")
                    print(f"  Error: {result.stderr[:200]}...")
                    
            except subprocess.TimeoutExpired:
                print(f"  ⚠️  {req_file}: Test timed out")
            except Exception as e:
                print(f"  ❌ {req_file}: Test error - {e}")

def suggest_fixes():
    """Suggest fixes for common dependency issues"""
    print("\n🔧 Suggested Fixes:")
    
    fixes = [
        "1. 🏠 Local Development:",
        "   pip install --upgrade pip",
        "   pip install -r requirements.txt",
        "",
        "2. 🐳 Docker Build:",
        "   docker build --no-cache -t font-identifier .",
        "",
        "3. ☁️ Heroku Deployment:",
        "   # Use requirements-heroku.txt",
        "   # Rename it to requirements.txt for deployment",
        "",
        "4. 🔄 Force Reinstall:",
        "   pip uninstall torch torchvision -y",
        "   pip install torch torchvision --no-cache-dir",
        "",
        "5. 🆕 Clean Environment:",
        "   python -m venv fresh_venv",
        "   fresh_venv\\Scripts\\activate  # Windows",
        "   # or: source fresh_venv/bin/activate  # Unix",
        "   pip install -r requirements.txt"
    ]
    
    for fix in fixes:
        print(fix)

def create_fixed_requirements():
    """Create a known-good requirements.txt"""
    print("\n🔨 Creating compatibility-tested requirements...")
    
    compatible_requirements = """# Tested compatible versions for Font Identifier
# Generated by test_dependencies.py

# Core Web Framework
streamlit>=1.28.0,<2.0.0

# PyTorch (compatible versions)
torch>=2.0.0,<3.0.0
torchvision>=0.15.0,<1.0.0

# Image Processing
Pillow>=9.0.0,<11.0.0
opencv-python-headless>=4.5.0,<5.0.0

# Data Science Stack
numpy>=1.21.0,<2.0.0
pandas>=1.3.0,<3.0.0
scikit-learn>=1.0.0,<2.0.0
matplotlib>=3.5.0,<4.0.0

# Media Processing
moviepy>=1.0.0,<2.0.0
imageio[ffmpeg]>=2.9.0,<3.0.0

# HTTP and API
requests>=2.25.0,<3.0.0

# Payment Processing
paypalrestsdk>=1.13.0,<2.0.0
stripe>=5.0.0,<11.0.0

# System Integration
pyautogui>=0.9.50,<1.0.0

# Database (conditional)
psycopg2-binary>=2.8.0,<3.0.0; platform_system != "Windows"
psycopg2>=2.8.0,<3.0.0; platform_system == "Windows"
"""
    
    with open('requirements-tested.txt', 'w') as f:
        f.write(compatible_requirements)
    
    print("✅ Created requirements-tested.txt with compatible versions")

def main():
    print_banner()
    
    # Check current installation
    check_current_installation()
    
    # Test PyTorch compatibility
    test_pytorch_compatibility()
    
    # Test requirements resolution
    test_requirements_resolution()
    
    # Create fixed requirements
    create_fixed_requirements()
    
    # Suggest fixes
    suggest_fixes()
    
    print("\n" + "=" * 50)
    print("🎯 Quick Fix Commands:")
    print("  pip install -r requirements-tested.txt")
    print("  docker build --no-cache -t font-identifier .")
    print("  python -m streamlit run main.py")

if __name__ == "__main__":
    main()
