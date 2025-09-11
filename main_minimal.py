#!/usr/bin/env python3
"""
Minimal Font Identifier App - Diagnostic Version
This version tests basic functionality without complex dependencies
"""

import streamlit as st
import os
import sys
from datetime import datetime

# Basic page config
st.set_page_config(
    page_title="Font Identifier - Minimal", 
    layout="wide",
    page_icon="🖋️"
)

def main():
    st.title("🖋️ Font Identifier - Diagnostic Mode")
    st.success("✅ App is running successfully!")
    
    # System information
    st.subheader("System Information")
    col1, col2 = st.columns(2)
    
    with col1:
        st.info(f"Python Version: {sys.version}")
        st.info(f"Current Time: {datetime.now()}")
        st.info(f"Working Directory: {os.getcwd()}")
    
    with col2:
        st.info(f"Streamlit Version: {st.__version__}")
        st.info(f"OS: {os.name}")
        st.info(f"Environment: {'Cloud' if os.environ.get('STREAMLIT_CLOUD') else 'Local'}")
    
    # Test basic functionality
    st.subheader("Basic Functionality Test")
    
    if st.button("Test Button"):
        st.success("Button works!")
    
    test_input = st.text_input("Test Input", "Hello World")
    if test_input:
        st.write(f"Input received: {test_input}")
    
    # File upload test
    st.subheader("File Upload Test")
    uploaded_file = st.file_uploader("Choose a file", type=['txt', 'png', 'jpg'])
    if uploaded_file:
        st.success(f"File uploaded: {uploaded_file.name}")
    
    # Show environment variables (safe ones only)
    st.subheader("Environment Variables")
    safe_vars = [
        'STREAMLIT_SERVER_PORT', 'STREAMLIT_SERVER_ADDRESS', 
        'PYTHONPATH', 'PATH', 'USER', 'HOME'
    ]
    
    for var in safe_vars:
        value = os.environ.get(var, 'Not set')
        st.text(f"{var}: {value[:100]}...")  # Truncate long values

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        st.error(f"Error occurred: {str(e)}")
        st.text(f"Error type: {type(e).__name__}")
        import traceback
        st.code(traceback.format_exc())
