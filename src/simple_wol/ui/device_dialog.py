"""
Device add/edit dialog window.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import socket
from typing import Optional, Callable

from ..device import Device
from ..network.wol import WakeOnLanSender
from .tooltip import InfoIcon


class DeviceDialog:
    """Dialog for adding or editing devices."""
    
    def __init__(self, parent, device: Optional[Device] = None, callback: Optional[Callable] = None):
        """
        Initialize device dialog.
        
        Args:
            parent: Parent window
            device: Device to edit (None for new device)
            callback: Callback function called with the device when saved
        """
        self.parent = parent
        self.device = device
        self.callback = callback
        self.dialog = None
        
        self.setup_dialog()
    
    def setup_dialog(self):
        """Set up the dialog window."""
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title("Add Device" if self.device is None else "Edit Device")
        self.dialog.geometry("450x350")
        self.dialog.resizable(False, False)
        self.dialog.grab_set()
        
        # Center the dialog
        self.dialog.transient(self.parent)
        
        # Main frame
        frame = ttk.Frame(self.dialog, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Entry variables
        self.name_var = tk.StringVar(value=self.device.name if self.device else "")
        self.mac_var = tk.StringVar(value=self.device.mac_address if self.device else "")
        self.ip_var = tk.StringVar(value=self.device.ip_address if self.device else "")
        self.port_var = tk.StringVar(value=str(self.device.port) if self.device else "9")
        
        self.setup_form_fields(frame)
        self.setup_help_section(frame)
        self.setup_buttons(frame)
        
        # Configure grid weights
        frame.columnconfigure(0, weight=1)
        
        # Focus on name entry and select all text if editing
        self.name_entry.focus()
        if self.device:
            self.name_entry.select_range(0, tk.END)
    
    def setup_form_fields(self, parent):
        """Set up the form input fields."""
        # Device Name
        name_frame = ttk.Frame(parent)
        name_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        name_frame.columnconfigure(1, weight=1)
        
        ttk.Label(name_frame, text="Device Name:").grid(row=0, column=0, sticky=tk.W)
        InfoIcon(name_frame, "Enter a friendly name for your device\n(e.g., 'My Computer', 'Home Server')").grid(row=0, column=2, padx=(5, 10))
        self.name_entry = ttk.Entry(name_frame, textvariable=self.name_var, width=30)
        self.name_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 0))
        
        # MAC Address
        mac_frame = ttk.Frame(parent)
        mac_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        mac_frame.columnconfigure(1, weight=1)
        
        ttk.Label(mac_frame, text="MAC Address:").grid(row=0, column=0, sticky=tk.W)
        InfoIcon(mac_frame, "The device's MAC address in format:\nAA:BB:CC:DD:EE:FF or AA-BB-CC-DD-EE-FF\n\nFind it with:\n• Windows: 'ipconfig /all'\n• Linux: 'ip addr' or 'ifconfig'").grid(row=0, column=2, padx=(5, 10))
        self.mac_entry = ttk.Entry(mac_frame, textvariable=self.mac_var, width=30)
        self.mac_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 0))
        
        # IP Address
        ip_frame = ttk.Frame(parent)
        ip_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        ip_frame.columnconfigure(1, weight=1)
        
        ttk.Label(ip_frame, text="IP Address (optional):").grid(row=0, column=0, sticky=tk.W)
        InfoIcon(ip_frame, "Optional: Specific IP address to send wake packet to\n\nLeave empty to use network broadcast\n(recommended for most cases)").grid(row=0, column=2, padx=(5, 10))
        self.ip_entry = ttk.Entry(ip_frame, textvariable=self.ip_var, width=30)
        self.ip_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 0))
        
        # Port
        port_frame = ttk.Frame(parent)
        port_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        port_frame.columnconfigure(1, weight=1)
        
        ttk.Label(port_frame, text="Port:").grid(row=0, column=0, sticky=tk.W)
        InfoIcon(port_frame, "UDP port for Wake-on-LAN packets:\n\n• Port 9: Standard WoL port (most common)\n• Port 7: Alternative WoL port\n• Port 0: Sometimes used for broadcasts\n\nYou can also enter a custom port number").grid(row=0, column=2, padx=(5, 10))
        
        # Port dropdown with common values
        self.port_combobox = ttk.Combobox(port_frame, textvariable=self.port_var, width=27, state="normal")
        self.port_combobox['values'] = ('9', '7', '0', '1234', '4000')
        self.port_combobox.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 0))
    
    def setup_help_section(self, parent):
        """Set up the help section."""
        help_frame = ttk.LabelFrame(parent, text="Quick Help", padding="10")
        help_frame.grid(row=4, column=0, columnspan=2, pady=15, sticky=(tk.W, tk.E))
        
        help_text = ("MAC Address formats: AA:BB:CC:DD:EE:FF or AA-BB-CC-DD-EE-FF\n"
                    "IP Address: Leave blank for network broadcast (recommended)\n"
                    "Port 9 is the standard - try Port 7 if it doesn't work")
        help_label = ttk.Label(help_frame, text=help_text, font=('Arial', 8), 
                              foreground='#666666', justify=tk.LEFT)
        help_label.pack(anchor=tk.W)
    
    def setup_buttons(self, parent):
        """Set up the dialog buttons."""
        button_frame = ttk.Frame(parent)
        button_frame.grid(row=5, column=0, columnspan=2, pady=20)
        
        save_btn = ttk.Button(button_frame, text="Save", command=self.save_device)
        save_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        cancel_btn = ttk.Button(button_frame, text="Cancel", command=self.dialog.destroy)
        cancel_btn.pack(side=tk.LEFT)
    
    def save_device(self):
        """Save the device after validation."""
        name = self.name_var.get().strip()
        mac = self.mac_var.get().strip()
        ip = self.ip_var.get().strip()
        port_str = self.port_var.get().strip()
        
        # Validation
        if not name:
            messagebox.showerror("Error", "Device name is required.")
            self.name_entry.focus()
            return
        
        if not mac:
            messagebox.showerror("Error", "MAC address is required.")
            self.mac_entry.focus()
            return
        
        # Validate MAC address format
        if not WakeOnLanSender.validate_mac_address(mac):
            messagebox.showerror("Error", "Invalid MAC address format.\n" +
                               "Use format: AA:BB:CC:DD:EE:FF or AA-BB-CC-DD-EE-FF")
            self.mac_entry.focus()
            return
        
        # Validate port
        try:
            port = int(port_str)
            if port < 0 or port > 65535:
                raise ValueError()
        except ValueError:
            messagebox.showerror("Error", "Port must be a number between 0 and 65535.")
            self.port_combobox.focus()
            return
        
        # Validate IP address if provided
        if ip:
            if not WakeOnLanSender.validate_ip_address(ip):
                if messagebox.askyesno("Invalid IP Address", 
                                     f"'{ip}' doesn't appear to be a valid IP address.\n" +
                                     "Do you want to continue anyway?"):
                    pass
                else:
                    self.ip_entry.focus()
                    return
        
        # Create device
        new_device = Device(name, mac, ip, port)
        
        # Call callback if provided
        if self.callback:
            self.callback(new_device)
        
        self.dialog.destroy()
    
    def show(self):
        """Show the dialog and wait for it to close."""
        self.dialog.wait_window()
