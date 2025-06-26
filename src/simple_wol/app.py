"""
Main application class for the Simple Wake-on-LAN application.
"""

import tkinter as tk
from tkinter import messagebox
from typing import List

from .device import Device
from .config import ConfigManager
from .ui.main_window import MainWindow
from . import __version__


class WakeOnLanApp:
    """Main Wake-on-LAN application with GUI."""
    
    def __init__(self, root: tk.Tk):
        """
        Initialize the application.
        
        Args:
            root: The root Tkinter window
        """
        self.root = root
        self.config_manager = ConfigManager()
        self.devices: List[Device] = []
        
        # Create main window
        self.main_window = MainWindow(root)
        self.main_window.set_device_changed_callback(self.on_devices_changed)
        
        # Load devices from config
        self.load_devices()
    
    def load_devices(self):
        """Load devices from config file and populate the UI."""
        try:
            self.devices = self.config_manager.load_devices()
            self.main_window.set_devices(self.devices)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load devices: {str(e)}")
            self.devices = []
            self.main_window.set_devices(self.devices)
    
    def save_devices(self):
        """Save current devices to config file."""
        try:
            self.config_manager.save_devices(self.devices)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save devices: {str(e)}")
    
    def on_devices_changed(self, export_path=None, import_path=None):
        """
        Handle device list changes.
        
        Args:
            export_path: Path to export devices to (if provided)
            import_path: Path to import devices from (if provided)
        """
        if export_path:
            self.export_devices(export_path)
        elif import_path:
            self.import_devices(import_path)
        else:
            # Regular device list change
            self.devices = self.main_window.devices
            self.save_devices()
    
    def export_devices(self, export_path: str):
        """Export devices to a file."""
        if not self.devices:
            messagebox.showwarning("No Devices", "No devices to export.")
            return
        
        try:
            self.config_manager.export_devices(self.devices, export_path)
            messagebox.showinfo("Success", f"Devices exported to {export_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export devices: {str(e)}")
    
    def import_devices(self, import_path: str):
        """Import devices from a file."""
        try:
            imported_devices = self.config_manager.import_devices(import_path)
            
            if messagebox.askyesno("Import Devices", 
                                 f"Import {len(imported_devices)} device(s)? "
                                 "This will replace your current device list."):
                self.devices = imported_devices
                self.main_window.set_devices(self.devices)
                self.save_devices()
                messagebox.showinfo("Success", f"Imported {len(imported_devices)} device(s)")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to import devices: {str(e)}")
    
    def run(self):
        """Run the application main loop."""
        self.root.mainloop()


def main():
    """Main function to run the application."""
    root = tk.Tk()
    app = WakeOnLanApp(root)
    app.run()


if __name__ == "__main__":
    main()
