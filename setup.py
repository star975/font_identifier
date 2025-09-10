"""
Setup script for Font Identifier application
"""

from setuptools import setup, find_packages
from pathlib import Path
import os

# Read README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

# Read requirements
requirements_path = this_directory / "requirements.txt"
if requirements_path.exists():
    with open(requirements_path, 'r', encoding='utf-8') as f:
        requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]
else:
    requirements = [
        'streamlit>=1.38.0',
        'torch>=2.2.2',
        'torchvision>=0.17',
        'Pillow>=10.4.0',
        'opencv-python>=4.10.0.84',
        'pyautogui>=0.9.54',
        'numpy>=1.26.4',
        'pandas>=2.2.2',
        'scikit-learn>=1.5.2',
        'matplotlib>=3.9.2',
        'moviepy>=1.0.3',
        'requests>=2.31.0',
        'imageio[ffmpeg]',
    ]

# Development requirements
dev_requirements = [
    'pytest>=7.0.0',
    'pytest-cov>=4.0.0',
    'black>=22.0.0',
    'flake8>=5.0.0',
    'mypy>=0.991',
    'pre-commit>=2.20.0',
]

setup(
    name="font-identifier",
    version="1.0.0",
    author="Font Identifier Team",
    author_email="contact@fontidentifier.com",
    description="AI-powered font identification with screen recording capabilities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/font-identifier",
    project_urls={
        "Bug Reports": "https://github.com/your-username/font-identifier/issues",
        "Source": "https://github.com/your-username/font-identifier",
        "Documentation": "https://github.com/your-username/font-identifier/wiki",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Multimedia :: Graphics",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: User Interfaces",
        "Topic :: Utilities",
        "Environment :: Web Environment",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": dev_requirements,
        "gpu": ["torch[cuda]", "torchvision[cuda]"],
        "payment": ["paypalrestsdk>=1.13.1", "stripe>=10.6.0"],
    },
    entry_points={
        "console_scripts": [
            "font-identifier=main:main",
            "fontid=main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": [
            "data/*.txt",
            "data/*.json",
            "static/**/*",
            "config/*.toml",
            "config/*.json",
            "*.md",
            "*.txt",
            "*.yml",
            "*.yaml",
        ],
    },
    exclude_package_data={
        "": [
            "*.pyc",
            "__pycache__/*",
            "*.log",
            "*.db",
            "recordings/*",
            "build/*",
            "dist/*",
            ".git/*",
            ".vscode/*",
            ".idea/*",
            "venv/*",
            "env/*",
            "model.pth",  # Too large for package
        ]
    },
    zip_safe=False,
    keywords=[
        "font", "identification", "ai", "machine learning", "computer vision",
        "streamlit", "web app", "screen recording", "typography", "design tools"
    ],
    platforms=["any"],
    license="MIT",
    
    # Metadata for PyPI
    download_url="https://github.com/your-username/font-identifier/archive/v1.0.0.tar.gz",
    
    # Additional metadata
    maintainer="Font Identifier Team",
    maintainer_email="maintainers@fontidentifier.com",
    
    # Command line scripts
    scripts=[
        "install.sh",
        "package.sh",
    ] if os.name != 'nt' else [
        "install.bat",
        "package.bat",
    ],
)

# Post-install message
print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                          Font Identifier Installed!                         ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  🎉 Installation completed successfully!                                     ║
║                                                                              ║
║  Quick Start:                                                                ║
║  1. Run: streamlit run main.py                                              ║
║  2. Open: http://localhost:8501                                             ║
║                                                                              ║
║  📱 Mobile PWA:                                                              ║
║  Open the app in your mobile browser and "Add to Home Screen"               ║
║                                                                              ║
║  🐳 Docker:                                                                  ║
║  docker-compose up -d                                                        ║
║                                                                              ║
║  📖 Documentation: README.md                                                 ║
║  🆘 Support: https://github.com/your-username/font-identifier/issues        ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
""")
