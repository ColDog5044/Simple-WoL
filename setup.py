#!/usr/bin/env python3
"""
Setup script for Simple Wake-on-LAN application
"""

from setuptools import setup, find_packages
import os

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read version from __init__.py
def read_version():
    try:
        with open("src/simple_wol/__init__.py", "r", encoding="utf-8") as fh:
            for line in fh:
                if line.startswith("__version__"):
                    return line.split("=")[1].strip().strip('"').strip("'")
    except FileNotFoundError:
        pass
    return "0.1.0"

setup(
    name="simple-wol",
    version=read_version(),
    author="Simple-WoL Team",
    description="A simple cross-platform Wake-on-LAN application with GUI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ColDog5044/Simple-WoL",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: System :: Networking",
        "Topic :: Utilities",
    ],
    python_requires=">=3.7",
    install_requires=[
        "wakeonlan>=3.1.0",
    ],
    extras_require={
        "build": [
            "pyinstaller>=5.0",
            "pillow>=8.0.0",  # For better icon support
        ],
        "dev": [
            "pytest>=6.0",
            "black",
            "flake8",
        ],
    },
    entry_points={
        "console_scripts": [
            "simple-wol=simple_wol.app:main",
        ],
        "gui_scripts": [
            "simple-wol-gui=simple_wol.app:main",
        ],
    },
    include_package_data=True,
    package_data={
        "simple_wol": ["assets/*"],
    },
    zip_safe=False,
)
