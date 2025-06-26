# Icon Assets for Simple Wake-on-LAN

This directory should contain icon files for the application.

## Supported Icon Formats:

### Windows
- `icon.ico` - Windows ICO format (recommended for Windows)
- Size: 16x16, 32x32, 48x48, 256x256 (multi-size ICO)

### Cross-Platform  
- `icon.png` - PNG format (works on all platforms)
- Size: 32x32 pixels recommended for taskbar
- Size: 16x16, 32x32, 48x48, 64x64 for multi-resolution support

### Linux/X11
- `icon.xbm` - X11 bitmap format
- `icon.png` - PNG format (preferred)

## File Locations:

The application will search for icons in this order:
1. `icon.ico` (current directory)
2. `icon.png` (current directory) 
3. `icon.xbm` (current directory)
4. `assets/icon.ico`
5. `assets/icon.png`
6. `resources/icon.ico`
7. `resources/icon.png`

## Creating Icons:

### Online Tools:
- [favicon.io](https://favicon.io/) - Generate ICO and PNG from text/image
- [converticon.com](https://converticon.com/) - Convert between formats
- [iconarchive.com](https://iconarchive.com/) - Free icon downloads

### Design Guidelines:
- Use simple, recognizable symbols
- High contrast for visibility in taskbar
- Test at 16x16 size for clarity
- Consider dark/light theme compatibility

### Wake-on-LAN Icon Ideas:
- Lightning bolt (⚡) 
- Power button symbol
- Network/wifi icon with power symbol
- Computer with wireless waves
- Moon/sleep symbol with wake indicator

## Installation:
Simply place your icon file in one of the supported locations and restart the application.
