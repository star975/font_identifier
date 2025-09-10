#!/bin/bash

echo "================================"
echo "Font Identifier - Build Package"
echo "================================"
echo

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}ERROR: Python 3 is not installed${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Python found${NC}"
echo

# Run the build script
echo "Starting build process..."
python3 build.py "$@"

if [ $? -eq 0 ]; then
    echo
    echo -e "${GREEN}✅ Build completed successfully!${NC}"
    echo "Check the 'dist' folder for packages."
else
    echo
    echo -e "${RED}❌ Build failed!${NC}"
fi

echo
