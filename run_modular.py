#!/usr/bin/env python3
"""
Run script for the modular Simple Wake-on-LAN application.
"""

import sys
import os

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import and run the application
from simple_wol.app import main

if __name__ == "__main__":
    main()
