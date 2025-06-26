# Simple Wake-on-LAN Icon Assets

This directory contains icon assets for the Simple Wake-on-LAN application.

## Icon Files

- `icon.ico` - Windows icon format (32x32, 16x16 for best compatibility)
- `icon.png` - Cross-platform PNG format (recommended 32x32 or 64x64)
- `icon.xbm` - X11 bitmap format (for Linux compatibility)

## Creating Icons

You can create your own icon files and place them here. The application will automatically detect and use them in the following order:

1. `assets/icon.ico` (Windows)
2. `assets/icon.png` (Cross-platform)
3. `assets/icon.xbm` (Linux X11)
4. `icon.ico` (Root directory)
5. `icon.png` (Root directory)
6. `icon.xbm` (Root directory)

If no icon is found, the application will use a default title with an emoji (⚡).

## Icon Guidelines

- **Size**: 32x32 pixels is recommended for compatibility
- **Format**: ICO for Windows, PNG for cross-platform, XBM for Linux
- **Design**: Simple, recognizable symbol related to networking/power
- **Colors**: High contrast for visibility in system tray/taskbar

## Tools for Creating Icons

- **GIMP**: Free, cross-platform image editor
- **Paint.NET**: Windows-only, user-friendly
- **Inkscape**: Vector graphics, good for scalable icons
- **Online converters**: For converting between formats

Place your custom icon files in this directory and restart the application to see them.
