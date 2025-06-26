"""
Simple Wake-on-LAN Application

A cross-platform Wake-on-LAN application with GUI for managing and waking network devices.
"""

__version__ = "0.1.0"
__author__ = "Simple-WoL Team"
__description__ = "Simple Wake-on-LAN Application"

from .app import WakeOnLanApp
from .device import Device
from .config import ConfigManager

__all__ = ['WakeOnLanApp', 'Device', 'ConfigManager', '__version__']
