#!/usr/bin/env python3
"""
Setup script for Simple Wake-on-LAN application
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="simple-wol",
    version="1.0.0",
    author="Simple-WoL",
    description="A simple cross-platform Wake-on-LAN application with GUI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ColDog5044/Simple-WoL",
    packages=find_packages(),
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
        "Topic :: System :: Networking",
        "Topic :: Utilities",
    ],
    python_requires=">=3.7",
    install_requires=[
        "wakeonlan>=3.1.0",
    ],
    entry_points={
        "console_scripts": [
            "simple-wol=simple_wol:main",
        ],
    },
)
