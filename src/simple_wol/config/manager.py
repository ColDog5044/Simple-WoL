"""
Configuration management for device storage and import/export.
"""

import json
import os
from typing import List

from ..device import Device


class ConfigManager:
    """Manages saving and loading device configurations."""
    
    def __init__(self, config_file: str = 'devices.json'):
        """
        Initialize ConfigManager.
        
        Args:
            config_file: Path to the configuration file
        """
        self.config_file = config_file
    
    def save_devices(self, devices: List[Device]) -> None:
        """
        Save devices to config file.
        
        Args:
            devices: List of Device objects to save
            
        Raises:
            Exception: If saving fails
        """
        try:
            data = [device.to_dict() for device in devices]
            with open(self.config_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            raise Exception(f"Failed to save devices: {str(e)}")
    
    def load_devices(self) -> List[Device]:
        """
        Load devices from config file.
        
        Returns:
            List of Device objects
            
        Raises:
            Exception: If loading fails
        """
        if not os.path.exists(self.config_file):
            return []
        
        try:
            with open(self.config_file, 'r') as f:
                data = json.load(f)
            return [Device.from_dict(item) for item in data]
        except Exception as e:
            raise Exception(f"Failed to load devices: {str(e)}")
    
    def export_devices(self, devices: List[Device], export_path: str) -> None:
        """
        Export devices to a specified file.
        
        Args:
            devices: List of Device objects to export
            export_path: Path to export file
            
        Raises:
            Exception: If export fails
        """
        try:
            data = [device.to_dict() for device in devices]
            with open(export_path, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            raise Exception(f"Failed to export devices: {str(e)}")
    
    def import_devices(self, import_path: str) -> List[Device]:
        """
        Import devices from a specified file.
        
        Args:
            import_path: Path to import file
            
        Returns:
            List of imported Device objects
            
        Raises:
            Exception: If import fails
        """
        try:
            with open(import_path, 'r') as f:
                data = json.load(f)
            return [Device.from_dict(item) for item in data]
        except Exception as e:
            raise Exception(f"Failed to import devices: {str(e)}")
    
    def config_exists(self) -> bool:
        """Check if config file exists."""
        return os.path.exists(self.config_file)
    
    def get_config_path(self) -> str:
        """Get the full path to the config file."""
        return os.path.abspath(self.config_file)
