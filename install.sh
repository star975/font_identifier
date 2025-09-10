#!/bin/bash

echo "================================"
echo "Font Identifier Installation"
echo "================================"
echo

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}ERROR: Python 3 is not installed${NC}"
    echo "Please install Python 3.8+ from https://python.org"
    echo "Or use your system package manager:"
    echo "  macOS: brew install python3"
    echo "  Ubuntu: sudo apt install python3 python3-pip python3-venv"
    echo "  CentOS: sudo yum install python3 python3-pip"
    exit 1
fi

echo -e "${GREEN}✓ Python found${NC}"
echo

# Check Python version
python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
min_version="3.8"

if [ "$(printf '%s\n' "$min_version" "$python_version" | sort -V | head -n1)" != "$min_version" ]; then
    echo -e "${RED}ERROR: Python $python_version found, but Python $min_version or higher is required${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Python $python_version is compatible${NC}"
echo

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo -e "${RED}ERROR: Failed to create virtual environment${NC}"
    echo "You might need to install python3-venv:"
    echo "  Ubuntu: sudo apt install python3-venv"
    exit 1
fi

echo -e "${GREEN}✓ Virtual environment created${NC}"
echo

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
python -m pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo -e "${RED}ERROR: Failed to install dependencies${NC}"
    echo "Try running: pip install -r requirements.txt --no-cache-dir"
    exit 1
fi

echo -e "${GREEN}✓ Dependencies installed${NC}"
echo

# Create necessary directories
echo "Creating directories..."
mkdir -p recordings config static

echo -e "${GREEN}✓ Directories created${NC}"
echo

# Check if model file exists
if [ ! -f "model.pth" ]; then
    echo -e "${YELLOW}WARNING: model.pth not found${NC}"
    echo "The app will create a dummy model, but you should add your trained model"
    echo
fi

echo "================================"
echo -e "${GREEN}Installation Complete!${NC}"
echo "================================"
echo
echo "To start the application:"
echo "1. Run: source venv/bin/activate"
echo "2. Run: streamlit run main.py"
echo "3. Open http://localhost:8501 in your browser"
echo
echo "Or simply run: ./start.sh"
echo

# Create start script
cat > start.sh << 'EOF'
#!/bin/bash
source venv/bin/activate
echo "Starting Font Identifier..."
echo "Open http://localhost:8501 in your browser"
streamlit run main.py
EOF

chmod +x start.sh

echo -e "${GREEN}✓ Start script created (start.sh)${NC}"
echo

# Create uninstall script
cat > uninstall.sh << 'EOF'
#!/bin/bash
echo "Uninstalling Font Identifier..."
rm -rf venv/
rm -f start.sh
echo "✓ Uninstalled (project files preserved)"
EOF

chmod +x uninstall.sh

echo -e "${GREEN}✓ Uninstall script created (uninstall.sh)${NC}"
echo

echo "Installation completed successfully!"
