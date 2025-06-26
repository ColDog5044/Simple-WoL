"""
Main window UI for the Wake-on-LAN application.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from typing import List, Optional, Callable
import os

from ..device import Device
from ..network.wol import WakeOnLanSender
from .tooltip import ToolTip
from .device_dialog import DeviceDialog


class MainWindow:
    """Main window for the Wake-on-LAN application."""
    
    def __init__(self, root: tk.Tk):
        """
        Initialize the main window.
        
        Args:
            root: The root Tkinter window
        """
        self.root = root
        self.devices: List[Device] = []
        self.device_changed_callback: Optional[Callable] = None
        
        # Sort state tracking
        self.sort_reverse = {'Device Name': False, 'MAC Address': False, 'IP Address': False, 'Port': False}
        self.last_sorted_column = None
        
        self.setup_window()
        self.setup_ui()
        self.setup_icon()
    
    def setup_window(self):
        """Set up the main window properties."""
        self.root.title("Simple Wake-on-LAN")
        self.root.geometry("800x600")
        self.root.minsize(600, 400)
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
    
    def setup_icon(self):
        """Set up the application icon."""
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
                    except Exception:
                        # Continue trying other formats
                        continue
            
            if not icon_found:
                # Create a simple default icon
                self.create_default_icon()
                
        except Exception:
            # Silently continue if icon setting fails
            pass
    
    def create_default_icon(self):
        """Create a simple default icon when no custom icon is found."""
        try:
            # Use emoji in title as visual indicator
            self.root.title("⚡ Simple Wake-on-LAN")
        except Exception:
            # If all else fails, just use plain title
            self.root.title("Simple Wake-on-LAN")
    
    def setup_ui(self):
        """Set up the user interface."""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Wake-on-LAN Manager", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Device list frame
        self.setup_device_list(main_frame)
        
        # Button frame
        self.setup_buttons(main_frame)
        
        # Context menu
        self.setup_context_menu()
    
    def setup_device_list(self, parent):
        """Set up the device list treeview."""
        list_frame = ttk.LabelFrame(parent, text="Devices", padding="10")
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
        
        # Scrollbar for treeview
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.device_tree.yview)
        self.device_tree.configure(yscrollcommand=scrollbar.set)
        
        self.device_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Add tooltip
        ToolTip(self.device_tree, "Double-click a device to wake it up", delay=1000)
        
        # Bind events
        self.device_tree.bind('<Double-1>', self.on_double_click)
        self.device_tree.bind('<Button-3>', self.on_right_click)
    
    def setup_buttons(self, parent):
        """Set up the action buttons."""
        button_frame = ttk.Frame(parent)
        button_frame.grid(row=2, column=0, columnspan=3, pady=10)
        
        # Device management buttons
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
        
        # Import/Export buttons
        export_btn = ttk.Button(button_frame, text="Export Devices", command=self.export_devices)
        export_btn.pack(side=tk.LEFT, padx=5)
        ToolTip(export_btn, "Save your device list to a file for backup", delay=700)
        
        import_btn = ttk.Button(button_frame, text="Import Devices", command=self.import_devices)
        import_btn.pack(side=tk.LEFT, padx=5)
        ToolTip(import_btn, "Load devices from a previously saved file", delay=700)
        
        # Second separator for utility functions
        ttk.Separator(button_frame, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=10)
        
        # Utility buttons
        update_btn = ttk.Button(button_frame, text="Check for Updates", command=self.check_for_updates)
        update_btn.pack(side=tk.LEFT, padx=5)
        ToolTip(update_btn, "Check for application updates online", delay=700)
    
    def setup_context_menu(self):
        """Set up the right-click context menu."""
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="Wake Device", command=self.wake_device)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Edit Device", command=self.edit_device)
        self.context_menu.add_command(label="Remove Device", command=self.remove_device)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Copy MAC Address", command=self.copy_mac_address)
        self.context_menu.add_command(label="Copy IP Address", command=self.copy_ip_address)
    
    def set_devices(self, devices: List[Device]):
        """Set the list of devices to display."""
        self.devices = devices
        self.refresh_device_list()
    
    def set_device_changed_callback(self, callback: Callable):
        """Set the callback for when devices are changed."""
        self.device_changed_callback = callback
    
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
        
        # Notify about changes
        if self.device_changed_callback:
            self.device_changed_callback()
    
    def on_double_click(self, event):
        """Handle double-click events - only wake if clicking on an actual item."""
        item = self.device_tree.identify_row(event.y)
        if item:
            self.wake_device()
    
    def on_right_click(self, event):
        """Handle right-click events - show context menu if clicking on an actual item."""
        item = self.device_tree.identify_row(event.y)
        if item:
            # Select the item that was right-clicked
            self.device_tree.selection_set(item)
            self.device_tree.focus(item)
            
            # Show context menu
            try:
                self.context_menu.tk_popup(event.x_root, event.y_root)
            finally:
                self.context_menu.grab_release()
    
    def get_selected_device(self) -> Optional[Device]:
        """Get the currently selected device."""
        selection = self.device_tree.selection()
        if not selection:
            return None
        
        item = selection[0]
        index = self.device_tree.index(item)
        return self.devices[index] if index < len(self.devices) else None
    
    def get_selected_index(self) -> Optional[int]:
        """Get the index of the currently selected device."""
        selection = self.device_tree.selection()
        if not selection:
            return None
        
        item = selection[0]
        return self.device_tree.index(item)
    
    def add_device(self):
        """Open dialog to add a new device."""
        def on_device_added(device: Device):
            self.devices.append(device)
            self.refresh_device_list()
            if self.device_changed_callback:
                self.device_changed_callback()
        
        dialog = DeviceDialog(self.root, callback=on_device_added)
        dialog.show()
    
    def edit_device(self):
        """Open dialog to edit selected device."""
        device = self.get_selected_device()
        index = self.get_selected_index()
        
        if not device:
            messagebox.showwarning("No Selection", "Please select a device to edit.")
            return
        
        def on_device_edited(edited_device: Device):
            self.devices[index] = edited_device
            self.refresh_device_list()
            if self.device_changed_callback:
                self.device_changed_callback()
        
        dialog = DeviceDialog(self.root, device=device, callback=on_device_edited)
        dialog.show()
    
    def remove_device(self):
        """Remove selected device."""
        device = self.get_selected_device()
        index = self.get_selected_index()
        
        if not device:
            messagebox.showwarning("No Selection", "Please select a device to remove.")
            return
        
        if messagebox.askyesno("Confirm", f"Are you sure you want to remove '{device.name}'?"):
            del self.devices[index]
            self.refresh_device_list()
            if self.device_changed_callback:
                self.device_changed_callback()
    
    def wake_device(self):
        """Send Wake-on-LAN packet to selected device."""
        device = self.get_selected_device()
        
        if not device:
            messagebox.showwarning("No Selection", "Please select a device to wake.")
            return
        
        try:
            WakeOnLanSender.wake_device(device)
            messagebox.showinfo("Success", f"Wake-on-LAN packet sent to {device.name}")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def copy_mac_address(self):
        """Copy the MAC address of the selected device to clipboard."""
        device = self.get_selected_device()
        
        if not device:
            return
        
        # Copy to clipboard
        self.root.clipboard_clear()
        self.root.clipboard_append(device.mac_address)
        
        # Show feedback
        messagebox.showinfo("Copied", f"MAC address copied to clipboard:\n{device.mac_address}")
    
    def copy_ip_address(self):
        """Copy the IP address of the selected device to clipboard."""
        device = self.get_selected_device()
        
        if not device:
            return
        
        if device.ip_address:
            # Copy to clipboard
            self.root.clipboard_clear()
            self.root.clipboard_append(device.ip_address)
            
            # Show feedback
            messagebox.showinfo("Copied", f"IP address copied to clipboard:\n{device.ip_address}")
        else:
            messagebox.showinfo("No IP Address", f"{device.name} uses broadcast mode (no specific IP address).")
    
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
        
        if file_path and self.device_changed_callback:
            # Let the main app handle the actual export
            self.device_changed_callback(export_path=file_path)
    
    def import_devices(self):
        """Import devices from a file."""
        file_path = filedialog.askopenfilename(
            title="Import Devices",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if file_path and self.device_changed_callback:
            # Let the main app handle the actual import
            self.device_changed_callback(import_path=file_path)
    
    def check_for_updates(self):
        """Check for application updates (placeholder functionality)."""
        from .. import __version__
        
        # TODO: Implement update checking functionality
        # This could check GitHub releases, a version server, etc.
        
        # Placeholder implementation
        messagebox.showinfo(
            "Check for Updates", 
            f"Current Version: {__version__}\n\n"
            "Update checking functionality will be implemented in a future version.\n\n"
            "Features to add:\n"
            "• Check GitHub releases for new versions\n"
            "• Download and install updates\n"
            "• Show changelog and release notes\n"
            "• Auto-update options"
        )
