# Simple Wake-on-LAN (WoL) Manager

A lightweight, cross-platform Wake-on-LAN application with a simple GUI that allows you to manage and wake network devices remotely.

## Features

- 🖥️ **Cross-Platform**: Works on Windows and Linux
- 🎯 **Simple GUI**: Easy-to-use interface built with tkinter
- 💾 **Device Storage**: Save your devices in a JSON configuration file
- 📤 **Export/Import**: Share device configurations between different computers
- 🔧 **Customizable**: Configure IP addresses and ports for each device
- ⚡ **Quick Wake**: Double-click a device to wake it instantly
- 🖱️ **Right-Click Menu**: Context menu with common actions
- 📋 **Copy to Clipboard**: Easy copying of MAC and IP addresses
- 🔄 **Auto-Updates**: Check for application updates (coming soon)
- 🎨 **Custom Icons**: Support for custom taskbar and window icons

## Screenshots

The application provides a clean, intuitive interface for managing your Wake-on-LAN enabled devices:
- Device list with name, MAC address, IP address, and port
- Add, edit, and remove devices
- Wake devices with a single click
- Export and import device configurations

## Installation

### Windows

1. Make sure you have Python 3.7 or higher installed
2. Run the installation script:
   ```cmd
   install.bat
   ```
3. Start the application:
   ```cmd
   run.bat
   ```

### Linux

1. Make sure you have Python 3.7+ and tkinter installed:
   ```bash
   # Ubuntu/Debian
   sudo apt install python3 python3-pip python3-tk
   
   # Fedora/RHEL
   sudo dnf install python3 python3-pip python3-tkinter
   
   # Arch Linux
   sudo pacman -S python python-pip tk
   ```

2. Run the installation script:
   ```bash
   chmod +x install.sh
   ./install.sh
   ```

3. Start the application:
   ```bash
   ./run.sh
   ```

### Manual Installation

If you prefer to install manually:

```bash
pip install -r requirements.txt
python simple_wol.py
```

## Usage

### Adding a Device

1. Click "Add Device"
2. Fill in the device information:
   - **Device Name**: A friendly name for your device
   - **MAC Address**: The device's MAC address (format: XX:XX:XX:XX:XX:XX or XX-XX-XX-XX-XX-XX)
   - **IP Address**: (Optional) Specific IP address to send the packet to
   - **Port**: UDP port to use (default: 9)
3. Click "Save"

### Waking a Device

- **Method 1**: Select a device and click "Wake Device"
- **Method 2**: Double-click on a device in the list

### Managing Devices

- **Edit**: Select a device and click "Edit Device"
- **Remove**: Select a device and click "Remove Device"
- **Export**: Click "Export Devices" to save your device list to a file
- **Import**: Click "Import Devices" to load devices from a file

## Configuration

Devices are automatically saved to `devices.json` in the application directory. This file contains:

```json
[
  {
    "name": "My Computer",
    "mac_address": "AA:BB:CC:DD:EE:FF",
    "ip_address": "192.168.1.100",
    "port": 9
  }
]
```

### Custom Icons

You can customize the application icon by placing icon files in the application directory:

- **Windows**: `icon.ico` (recommended)
- **Cross-platform**: `icon.png` (32x32 pixels)
- **Linux/X11**: `icon.xbm` or `icon.png`

The application will automatically detect and use custom icons. See `ICON_README.md` for detailed instructions.

## Requirements

- Python 3.7 or higher
- tkinter (usually included with Python)
- wakeonlan library (automatically installed)

## Wake-on-LAN Setup

For Wake-on-LAN to work, the target device must be configured properly:

### Windows
1. Open Device Manager
2. Find your network adapter under "Network adapters"
3. Right-click and select "Properties"
4. Go to "Power Management" tab
5. Check "Allow this device to wake the computer"
6. Go to "Advanced" tab
7. Enable "Wake on Magic Packet"

### Linux
```bash
# Check if WoL is supported
sudo ethtool eth0

# Enable WoL
sudo ethtool -s eth0 wol g

# Make it persistent (add to /etc/rc.local or systemd service)
```

### BIOS/UEFI
Enable "Wake on LAN" or "Power on by PCI-E/PCIe" in BIOS settings.

## Troubleshooting

### Common Issues

1. **Device doesn't wake up**:
   - Ensure Wake-on-LAN is enabled in device settings
   - Check if the device is connected via Ethernet (WiFi WoL is often unreliable)
   - Verify the MAC address is correct
   - Try using broadcast instead of specific IP address

2. **Permission errors on Linux**:
   - The application doesn't require root privileges
   - Ensure you have network access permissions

3. **GUI doesn't appear**:
   - Make sure tkinter is installed: `python -c "import tkinter"`
   - On Linux, install the tkinter package for your distribution

### Network Configuration

- **Broadcast**: Leave IP address empty to use network broadcast
- **Directed**: Enter specific IP address for directed packets
- **Port**: Standard WoL port is 9, but some devices use 7

## Development

The application is built with:
- **GUI**: tkinter (cross-platform, included with Python)
- **WoL**: wakeonlan library for sending magic packets
- **Configuration**: JSON for device storage

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
