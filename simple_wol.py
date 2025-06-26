import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
import re
import socket
from wakeonlan import send_magic_packet
from typing import Dict, List, Optional

# Application version
__version__ = "0.1.0"


class ToolTip:
    """Elegant tooltip class with delayed appearance."""
    
    def __init__(self, widget, text, delay=800):
        self.widget = widget
        self.text = text
        self.delay = delay
        self.tooltip_window = None
        self.show_timer = None
        self.widget.bind("<Enter>", self.on_enter)
        self.widget.bind("<Leave>", self.on_leave)
        self.widget.bind("<Motion>", self.on_motion)
    
    def on_enter(self, event=None):
        if self.show_timer:
            self.widget.after_cancel(self.show_timer)
        self.show_timer = self.widget.after(self.delay, self.show_tooltip)
    
    def on_leave(self, event=None):
        if self.show_timer:
            self.widget.after_cancel(self.show_timer)
            self.show_timer = None
        self.hide_tooltip()
    
    def on_motion(self, event=None):
        if self.tooltip_window:
            self.hide_tooltip()
    
    def show_tooltip(self, event=None):
        if self.tooltip_window or not self.text:
            return
        
        x = self.widget.winfo_rootx() + self.widget.winfo_width() + 5
        y = self.widget.winfo_rooty() + self.widget.winfo_height() // 2
        
        self.tooltip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        
        # Add a subtle shadow effect
        shadow = tk.Frame(tw, background='#888888')
        shadow.pack(padx=(2, 0), pady=(2, 0))
        
        content = tk.Frame(shadow, background="#fffef0", relief=tk.SOLID, borderwidth=1)
        content.pack()
        
        label = tk.Label(content, text=self.text, justify=tk.LEFT,
                        background="#fffef0", foreground="#333333",
                        font=("Segoe UI", 9), wraplength=300, padx=8, pady=6)
        label.pack()
        
        # Fade in effect (simplified)
        tw.attributes('-alpha', 0.9)
    
    def hide_tooltip(self, event=None):
        tw = self.tooltip_window
        self.tooltip_window = None
        if tw:
            tw.destroy()


class InfoIcon:
    """Small info icon that shows tooltip on hover."""
    
    def __init__(self, parent, tooltip_text, delay=500):
        self.icon = tk.Label(parent, text="ⓘ", font=("Segoe UI", 10), 
                           foreground="#666666", cursor="question_arrow",
                           padx=2, pady=0)
        self.tooltip = ToolTip(self.icon, tooltip_text, delay)
    
    def grid(self, **kwargs):
        self.icon.grid(**kwargs)
    
    def pack(self, **kwargs):
        self.icon.pack(**kwargs)


class Device:
    """Represents a network device that can be woken up."""
    
    def __init__(self, name: str, mac_address: str, ip_address: str = "", port: int = 9):
        self.name = name
        self.mac_address = mac_address.upper()
        self.ip_address = ip_address
        self.port = port
    
    def to_dict(self) -> Dict:
        return {
            'name': self.name,
            'mac_address': self.mac_address,
            'ip_address': self.ip_address,
            'port': self.port
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Device':
        return cls(
            name=data['name'],
            mac_address=data['mac_address'],
            ip_address=data.get('ip_address', ''),
            port=data.get('port', 9)
        )


class ConfigManager:
    """Manages saving and loading device configurations."""
    
    def __init__(self, config_file: str = 'devices.json'):
        self.config_file = config_file
    
    def save_devices(self, devices: List[Device]) -> None:
        """Save devices to config file."""
        try:
            data = [device.to_dict() for device in devices]
            with open(self.config_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            raise Exception(f"Failed to save devices: {str(e)}")
    
    def load_devices(self) -> List[Device]:
        """Load devices from config file."""
        if not os.path.exists(self.config_file):
            return []
        
        try:
            with open(self.config_file, 'r') as f:
                data = json.load(f)
            return [Device.from_dict(item) for item in data]
        except Exception as e:
            raise Exception(f"Failed to load devices: {str(e)}")
    
    def export_devices(self, devices: List[Device], export_path: str) -> None:
        """Export devices to a specified file."""
        try:
            data = [device.to_dict() for device in devices]
            with open(export_path, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            raise Exception(f"Failed to export devices: {str(e)}")
    
    def import_devices(self, import_path: str) -> List[Device]:
        """Import devices from a specified file."""
        try:
            with open(import_path, 'r') as f:
                data = json.load(f)
            return [Device.from_dict(item) for item in data]
        except Exception as e:
            raise Exception(f"Failed to import devices: {str(e)}")


class WakeOnLanApp:
    """Main Wake-on-LAN application with GUI."""
    
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Simple Wake-on-LAN")
        self.root.geometry("800x600")
        self.root.minsize(600, 400)
        
        # Set application icon (placeholder)
        self.set_application_icon()
        
        self.config_manager = ConfigManager()
        self.devices: List[Device] = []
        
        self.setup_ui()
        self.load_devices()
    
    def set_application_icon(self):
        """Set the application icon for window and taskbar (placeholder functionality)."""
        # TODO: Implement custom icon functionality
        # This should work cross-platform (Windows, Linux, macOS)
        
        try:
            # Check if custom icon file exists
            icon_paths = [
                'icon.ico',      # Windows format
                'icon.png',      # Cross-platform format  
                'icon.xbm',      # X11 bitmap format (Linux)
                'assets/icon.ico',
                'assets/icon.png',
                'resources/icon.ico',
                'resources/icon.png'
            ]
            
            icon_found = False
            for icon_path in icon_paths:
                if os.path.exists(icon_path):
                    try:
                        # Try to set the icon
                        if icon_path.endswith('.ico'):
                            # Windows ICO format
                            self.root.iconbitmap(icon_path)
                        elif icon_path.endswith('.png'):
                            # PNG format - convert to PhotoImage
                            try:
                                from PIL import Image, ImageTk
                                img = Image.open(icon_path)
                                # Resize to standard icon size if needed
                                img = img.resize((32, 32), Image.Resampling.LANCZOS)
                                photo = ImageTk.PhotoImage(img)
                                self.root.iconphoto(True, photo)
                            except ImportError:
                                # PIL not available, try basic tkinter PhotoImage
                                photo = tk.PhotoImage(file=icon_path)
                                self.root.iconphoto(True, photo)
                        elif icon_path.endswith('.xbm'):
                            # X11 bitmap format
                            self.root.iconbitmap(f'@{icon_path}')
                        
                        icon_found = True
                        break
                    except Exception as e:
                        # Continue trying other formats
                        continue
            
            if not icon_found:
                # Create a simple default icon using tkinter (cross-platform)
                self.create_default_icon()
                
        except Exception as e:
            # Silently continue if icon setting fails
            pass
    
    def create_default_icon(self):
        """Create a simple default icon when no custom icon is found."""
        try:
            # Create a simple 32x32 icon using tkinter
            # This creates a basic geometric pattern as placeholder
            icon_size = 32
            
            # Create a small window to generate the icon
            icon_window = tk.Toplevel()
            icon_window.withdraw()  # Hide the window
            
            canvas = tk.Canvas(icon_window, width=icon_size, height=icon_size, bg='white')
            canvas.pack()
            
            # Draw a simple "W" shape for Wake-on-LAN
            canvas.create_polygon(
                [4, 28, 8, 4, 12, 20, 16, 4, 20, 20, 24, 4, 28, 28],
                fill='#2E7D32', outline='#1B5E20', width=1
            )
            
            # Convert canvas to PhotoImage (this is a simplified approach)
            # In a real implementation, you'd want to use PIL for better results
            canvas.update()
            
            # Use a basic approach - just set window title with emoji as visual indicator
            self.root.title("⚡ Simple Wake-on-LAN")
            
            icon_window.destroy()
            
        except Exception:
            # If all else fails, just use the title with emoji
            self.root.title("⚡ Simple Wake-on-LAN")
    
    def setup_ui(self):
        """Set up the user interface."""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Wake-on-LAN Manager", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Device list frame
        list_frame = ttk.LabelFrame(main_frame, text="Devices", padding="10")
        list_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
        # Treeview for device list
        columns = ('Device Name', 'MAC Address', 'IP Address', 'Port')
        self.device_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=10)
        
        # Configure column headings and widths with sorting
        self.device_tree.heading('Device Name', text='Device Name ↕', command=lambda: self.sort_column('Device Name'))
        self.device_tree.heading('MAC Address', text='MAC Address ↕', command=lambda: self.sort_column('MAC Address'))
        self.device_tree.heading('IP Address', text='IP Address ↕', command=lambda: self.sort_column('IP Address'))
        self.device_tree.heading('Port', text='Port ↕', command=lambda: self.sort_column('Port'))
        
        self.device_tree.column('Device Name', width=200)
        self.device_tree.column('MAC Address', width=150)
        self.device_tree.column('IP Address', width=150)
        self.device_tree.column('Port', width=80)
        
        # Keep track of sort state
        self.sort_reverse = {'Device Name': False, 'MAC Address': False, 'IP Address': False, 'Port': False}
        self.last_sorted_column = None
        
        # Scrollbar for treeview
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.device_tree.yview)
        self.device_tree.configure(yscrollcommand=scrollbar.set)
        
        self.device_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Add subtle tooltip to the device tree
        ToolTip(self.device_tree, "Double-click a device to wake it up", delay=1000)
        
        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=3, pady=10)
        
        # Buttons (only add tooltips to less obvious ones)
        add_btn = ttk.Button(button_frame, text="Add Device", command=self.add_device)
        add_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        edit_btn = ttk.Button(button_frame, text="Edit Device", command=self.edit_device)
        edit_btn.pack(side=tk.LEFT, padx=5)
        
        remove_btn = ttk.Button(button_frame, text="Remove Device", command=self.remove_device)
        remove_btn.pack(side=tk.LEFT, padx=5)
        
        wake_btn = ttk.Button(button_frame, text="Wake Device", command=self.wake_device)
        wake_btn.pack(side=tk.LEFT, padx=5)
        ToolTip(wake_btn, "Send Wake-on-LAN packet to selected device", delay=700)
        
        # Separator
        ttk.Separator(button_frame, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=10)
        
        export_btn = ttk.Button(button_frame, text="Export Devices", command=self.export_devices)
        export_btn.pack(side=tk.LEFT, padx=5)
        ToolTip(export_btn, "Save your device list to a file for backup", delay=700)
        
        import_btn = ttk.Button(button_frame, text="Import Devices", command=self.import_devices)
        import_btn.pack(side=tk.LEFT, padx=5)
        ToolTip(import_btn, "Load devices from a previously saved file", delay=700)
        
        # Second separator for utility functions
        ttk.Separator(button_frame, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=10)
        
        update_btn = ttk.Button(button_frame, text="Check for Updates", command=self.check_for_updates)
        update_btn.pack(side=tk.LEFT, padx=5)
        ToolTip(update_btn, "Check for application updates online", delay=700)
        
        # Bind double-click to wake device (only on actual items)
        self.device_tree.bind('<Double-1>', self.on_double_click)
        
        # Bind right-click for context menu
        self.device_tree.bind('<Button-3>', self.on_right_click)
        
        # Create context menu
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="Wake Device", command=self.wake_device)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Edit Device", command=self.edit_device)
        self.context_menu.add_command(label="Remove Device", command=self.remove_device)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Copy MAC Address", command=self.copy_mac_address)
        self.context_menu.add_command(label="Copy IP Address", command=self.copy_ip_address)
    
    def load_devices(self):
        """Load devices from config file and populate the tree."""
        try:
            self.devices = self.config_manager.load_devices()
            self.refresh_device_list()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load devices: {str(e)}")
    
    def save_devices(self):
        """Save current devices to config file."""
        try:
            self.config_manager.save_devices(self.devices)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save devices: {str(e)}")
    
    def refresh_device_list(self):
        """Refresh the device list in the tree view."""
        # Clear existing items
        for item in self.device_tree.get_children():
            self.device_tree.delete(item)
        
        # Add devices to tree
        for device in self.devices:
            self.device_tree.insert('', tk.END, values=(
                device.name,
                device.mac_address,
                device.ip_address or 'Broadcast',
                device.port
            ))
    
    def sort_column(self, col):
        """Sort the tree view by the specified column."""
        if not self.devices:
            return
        
        # Update sort indicators in headers
        for column in ['Device Name', 'MAC Address', 'IP Address', 'Port']:
            if column == col:
                if self.last_sorted_column == col:
                    self.sort_reverse[col] = not self.sort_reverse[col]
                else:
                    self.sort_reverse[col] = False
                arrow = ' ↓' if self.sort_reverse[col] else ' ↑'
                header_text = column + arrow
            else:
                header_text = column + ' ↕'
            self.device_tree.heading(column, text=header_text)
        
        self.last_sorted_column = col
        
        # Sort the devices list
        if col == 'Device Name':
            self.devices.sort(key=lambda x: x.name.lower(), reverse=self.sort_reverse[col])
        elif col == 'MAC Address':
            self.devices.sort(key=lambda x: x.mac_address, reverse=self.sort_reverse[col])
        elif col == 'IP Address':
            self.devices.sort(key=lambda x: x.ip_address or '', reverse=self.sort_reverse[col])
        elif col == 'Port':
            self.devices.sort(key=lambda x: x.port, reverse=self.sort_reverse[col])
        
        # Refresh the display
        self.refresh_device_list()
    
    def on_double_click(self, event):
        """Handle double-click events - only wake if clicking on an actual item."""
        # Get the item that was clicked
        item = self.device_tree.identify_row(event.y)
        if item:  # Only proceed if we clicked on an actual row
            self.wake_device()
    
    def on_right_click(self, event):
        """Handle right-click events - show context menu if clicking on an actual item."""
        # Get the item that was clicked
        item = self.device_tree.identify_row(event.y)
        if item:  # Only show menu if we clicked on an actual row
            # Select the item that was right-clicked
            self.device_tree.selection_set(item)
            self.device_tree.focus(item)
            
            # Show context menu
            try:
                self.context_menu.tk_popup(event.x_root, event.y_root)
            finally:
                self.context_menu.grab_release()
    
    def copy_mac_address(self):
        """Copy the MAC address of the selected device to clipboard."""
        selection = self.device_tree.selection()
        if not selection:
            return
        
        item = selection[0]
        index = self.device_tree.index(item)
        device = self.devices[index]
        
        # Copy to clipboard
        self.root.clipboard_clear()
        self.root.clipboard_append(device.mac_address)
        
        # Show feedback
        messagebox.showinfo("Copied", f"MAC address copied to clipboard:\n{device.mac_address}")
    
    def copy_ip_address(self):
        """Copy the IP address of the selected device to clipboard."""
        selection = self.device_tree.selection()
        if not selection:
            return
        
        item = selection[0]
        index = self.device_tree.index(item)
        device = self.devices[index]
        
        if device.ip_address:
            # Copy to clipboard
            self.root.clipboard_clear()
            self.root.clipboard_append(device.ip_address)
            
            # Show feedback
            messagebox.showinfo("Copied", f"IP address copied to clipboard:\n{device.ip_address}")
        else:
            messagebox.showinfo("No IP Address", f"{device.name} uses broadcast mode (no specific IP address).")
    
    def add_device(self):
        """Open dialog to add a new device."""
        self.device_dialog()
    
    def edit_device(self):
        """Open dialog to edit selected device."""
        selection = self.device_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a device to edit.")
            return
        
        item = selection[0]
        index = self.device_tree.index(item)
        device = self.devices[index]
        
        self.device_dialog(device, index)
    
    def remove_device(self):
        """Remove selected device."""
        selection = self.device_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a device to remove.")
            return
        
        if messagebox.askyesno("Confirm", "Are you sure you want to remove this device?"):
            item = selection[0]
            index = self.device_tree.index(item)
            del self.devices[index]
            self.refresh_device_list()
            self.save_devices()
    
    def wake_device(self):
        """Send Wake-on-LAN packet to selected device."""
        selection = self.device_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a device to wake.")
            return
        
        item = selection[0]
        index = self.device_tree.index(item)
        device = self.devices[index]
        
        try:
            if device.ip_address:
                send_magic_packet(device.mac_address, ip_address=device.ip_address, port=device.port)
            else:
                send_magic_packet(device.mac_address, port=device.port)
            
            messagebox.showinfo("Success", f"Wake-on-LAN packet sent to {device.name}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to send Wake-on-LAN packet: {str(e)}")
    
    def device_dialog(self, device: Optional[Device] = None, index: Optional[int] = None):
        """Open dialog for adding/editing device."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Device" if device is None else "Edit Device")
        dialog.geometry("450x350")
        dialog.resizable(False, False)
        dialog.grab_set()
        
        # Center the dialog
        dialog.transient(self.root)
        
        # Main frame
        frame = ttk.Frame(dialog, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Entry variables
        name_var = tk.StringVar(value=device.name if device else "")
        mac_var = tk.StringVar(value=device.mac_address if device else "")
        ip_var = tk.StringVar(value=device.ip_address if device else "")
        port_var = tk.StringVar(value=str(device.port) if device else "9")
        
        # Form fields with info icons
        # Device Name
        name_frame = ttk.Frame(frame)
        name_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        name_frame.columnconfigure(1, weight=1)
        
        ttk.Label(name_frame, text="Device Name:").grid(row=0, column=0, sticky=tk.W)
        InfoIcon(name_frame, "Enter a friendly name for your device\n(e.g., 'My Computer', 'Home Server')").grid(row=0, column=2, padx=(5, 10))
        name_entry = ttk.Entry(name_frame, textvariable=name_var, width=30)
        name_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 0))
        
        # MAC Address
        mac_frame = ttk.Frame(frame)
        mac_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        mac_frame.columnconfigure(1, weight=1)
        
        ttk.Label(mac_frame, text="MAC Address:").grid(row=0, column=0, sticky=tk.W)
        InfoIcon(mac_frame, "The device's MAC address in format:\nAA:BB:CC:DD:EE:FF or AA-BB-CC-DD-EE-FF\n\nFind it with:\n• Windows: 'ipconfig /all'\n• Linux: 'ip addr' or 'ifconfig'").grid(row=0, column=2, padx=(5, 10))
        mac_entry = ttk.Entry(mac_frame, textvariable=mac_var, width=30)
        mac_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 0))
        
        # IP Address
        ip_frame = ttk.Frame(frame)
        ip_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        ip_frame.columnconfigure(1, weight=1)
        
        ttk.Label(ip_frame, text="IP Address (optional):").grid(row=0, column=0, sticky=tk.W)
        InfoIcon(ip_frame, "Optional: Specific IP address to send wake packet to\n\nLeave empty to use network broadcast\n(recommended for most cases)").grid(row=0, column=2, padx=(5, 10))
        ip_entry = ttk.Entry(ip_frame, textvariable=ip_var, width=30)
        ip_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 0))
        
        # Port
        port_frame = ttk.Frame(frame)
        port_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        port_frame.columnconfigure(1, weight=1)
        
        ttk.Label(port_frame, text="Port:").grid(row=0, column=0, sticky=tk.W)
        InfoIcon(port_frame, "UDP port for Wake-on-LAN packets:\n\n• Port 9: Standard WoL port (most common)\n• Port 7: Alternative WoL port\n• Port 0: Sometimes used for broadcasts\n\nYou can also enter a custom port number").grid(row=0, column=2, padx=(5, 10))
        
        # Port dropdown with common values
        port_combobox = ttk.Combobox(port_frame, textvariable=port_var, width=27, state="normal")
        port_combobox['values'] = ('9', '7', '0', '1234', '4000')
        port_combobox.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 0))
        
        # Help text frame
        help_frame = ttk.LabelFrame(frame, text="Quick Help", padding="10")
        help_frame.grid(row=4, column=0, columnspan=2, pady=15, sticky=(tk.W, tk.E))
        
        help_text = ("MAC Address formats: AA:BB:CC:DD:EE:FF or AA-BB-CC-DD-EE-FF\n"
                    "IP Address: Leave blank for network broadcast (recommended)\n"
                    "Port 9 is the standard - try Port 7 if it doesn't work")
        help_label = ttk.Label(help_frame, text=help_text, font=('Arial', 8), 
                              foreground='#666666', justify=tk.LEFT)
        help_label.pack(anchor=tk.W)
        
        # Button frame
        button_frame = ttk.Frame(frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=20)
        
        def save_device():
            name = name_var.get().strip()
            mac = mac_var.get().strip()
            ip = ip_var.get().strip()
            port_str = port_var.get().strip()
            
            # Validation
            if not name:
                messagebox.showerror("Error", "Device name is required.")
                name_entry.focus()
                return
            
            if not mac:
                messagebox.showerror("Error", "MAC address is required.")
                mac_entry.focus()
                return
            
            # Validate MAC address format
            mac_pattern = r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$'
            if not re.match(mac_pattern, mac):
                messagebox.showerror("Error", "Invalid MAC address format.\n" +
                                   "Use format: AA:BB:CC:DD:EE:FF or AA-BB-CC-DD-EE-FF")
                mac_entry.focus()
                return
            
            # Validate port
            try:
                port = int(port_str)
                if port < 0 or port > 65535:
                    raise ValueError()
            except ValueError:
                messagebox.showerror("Error", "Port must be a number between 0 and 65535.")
                port_combobox.focus()
                return
            
            # Validate IP address if provided
            if ip:
                try:
                    socket.inet_aton(ip)
                except socket.error:
                    if messagebox.askyesno("Invalid IP Address", 
                                         f"'{ip}' doesn't appear to be a valid IP address.\n" +
                                         "Do you want to continue anyway?"):
                        pass
                    else:
                        ip_entry.focus()
                        return
            
            # Create or update device
            new_device = Device(name, mac, ip, port)
            
            if device is None:  # Adding new device
                self.devices.append(new_device)
            else:  # Editing existing device
                self.devices[index] = new_device
            
            self.refresh_device_list()
            self.save_devices()
            dialog.destroy()
        
        # Buttons (no tooltips needed - they're self-explanatory)
        save_btn = ttk.Button(button_frame, text="Save", command=save_device)
        save_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        cancel_btn = ttk.Button(button_frame, text="Cancel", command=dialog.destroy)
        cancel_btn.pack(side=tk.LEFT)
        
        # Configure grid weights
        frame.columnconfigure(0, weight=1)
        
        # Focus on name entry and select all text if editing
        name_entry.focus()
        if device:
            name_entry.select_range(0, tk.END)
    
    def export_devices(self):
        """Export devices to a file."""
        if not self.devices:
            messagebox.showwarning("No Devices", "No devices to export.")
            return
        
        file_path = filedialog.asksaveasfilename(
            title="Export Devices",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                self.config_manager.export_devices(self.devices, file_path)
                messagebox.showinfo("Success", f"Devices exported to {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export devices: {str(e)}")
    
    def import_devices(self):
        """Import devices from a file."""
        file_path = filedialog.askopenfilename(
            title="Import Devices",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                imported_devices = self.config_manager.import_devices(file_path)
                
                if messagebox.askyesno("Import Devices", 
                                     f"Import {len(imported_devices)} device(s)? "
                                     "This will replace your current device list."):
                    self.devices = imported_devices
                    self.refresh_device_list()
                    self.save_devices()
                    messagebox.showinfo("Success", f"Imported {len(imported_devices)} device(s)")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to import devices: {str(e)}")
    
    def check_for_updates(self):
        """Check for application updates (placeholder functionality)."""
        # TODO: Implement update checking functionality
        # This could check GitHub releases, a version server, etc.
        
        # Placeholder implementation
        result = messagebox.showinfo(
            "Check for Updates", 
            f"Current Version: {__version__}\n\n"
            "Update checking functionality will be implemented in a future version.\n\n"
            "Features to add:\n"
            "• Check GitHub releases for new versions\n"
            "• Download and install updates\n"
            "• Show changelog and release notes\n"
            "• Auto-update options"
        )
        
        # Future implementation ideas:
        # 1. Check GitHub API for latest release
        # 2. Compare version numbers
        # 3. Show update dialog with changelog
        # 4. Option to download/install update
        # 5. Auto-update settings in preferences


def main():
    """Main function to run the application."""
    root = tk.Tk()
    app = WakeOnLanApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
