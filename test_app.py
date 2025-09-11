#!/usr/bin/env python3
"""
Minimal test script to identify app startup issues
"""

import sys
import traceback

def test_imports():
    """Test all critical imports"""
    try:
        print("Testing imports...")
        
        # Basic imports
        import os
        import sqlite3
        import hashlib
        import base64
        from datetime import datetime, timedelta
        from typing import Tuple, Optional
        print("✓ Basic imports successful")
        
        # Streamlit
        import streamlit as st
        print("✓ Streamlit import successful")
        
        # PyTorch
        import torch
        import torch.nn as nn
        import torchvision.models as tv_models
        from PIL import Image
        print("✓ PyTorch imports successful")
        
        # Other libraries
        import numpy as np
        import pandas as pd
        import requests
        print("✓ Other libraries successful")
        
        return True
        
    except Exception as e:
        print(f"❌ Import failed: {e}")
        traceback.print_exc()
        return False

def test_streamlit_config():
    """Test Streamlit configuration"""
    try:
        import streamlit as st
        
        # Test basic streamlit functions (won't actually render)
        st.set_page_config(page_title="Test")
        print("✓ Streamlit configuration successful")
        return True
        
    except Exception as e:
        print(f"❌ Streamlit config failed: {e}")
        traceback.print_exc()
        return False

def test_main_functions():
    """Test main application functions"""
    try:
        # Import main module
        sys.path.append('.')
        import main
        
        # Test key functions exist
        assert hasattr(main, 'main'), "main() function missing"
        assert hasattr(main, 'load_model_and_classes'), "load_model_and_classes() function missing"
        assert hasattr(main, 'init_db'), "init_db() function missing"
        
        print("✓ Main functions exist")
        return True
        
    except Exception as e:
        print(f"❌ Main functions test failed: {e}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🔍 Running Font Identifier startup diagnostics...\n")
    
    tests = [
        ("Import Tests", test_imports),
        ("Streamlit Config", test_streamlit_config), 
        ("Main Functions", test_main_functions),
    ]
    
    all_passed = True
    for test_name, test_func in tests:
        print(f"Running {test_name}...")
        if test_func():
            print(f"✅ {test_name} passed\n")
        else:
            print(f"❌ {test_name} failed\n")
            all_passed = False
    
    if all_passed:
        print("🎉 All tests passed! App should start successfully.")
    else:
        print("💥 Some tests failed. Check the errors above.")
        sys.exit(1)
