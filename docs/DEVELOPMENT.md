# Development Guide

This guide explains how to work with the modular Simple Wake-on-LAN application.

## Project Structure

The application has been refactored from a single monolithic file into a modular package structure:

```
src/simple_wol/
├── __init__.py          # Package entry point
├── __main__.py          # Command line entry point  
├── app.py               # Main application class
├── device.py            # Device data model
├── config/              # Configuration management
│   ├── __init__.py
│   └── manager.py       # ConfigManager class
├── ui/                  # User interface components
│   ├── __init__.py
│   ├── main_window.py   # Main application window
│   ├── device_dialog.py # Add/edit device dialog
│   └── tooltip.py       # Tooltip widgets
└── network/             # Network operations
    ├── __init__.py
    └── wol.py           # Wake-on-LAN sender
```

## Development Tasks

Use the development task runner for common tasks:

```bash
# Install runtime dependencies
python dev.py install

# Install build dependencies (PyInstaller, etc.)
python dev.py install-build

# Run the application in development mode
python dev.py run

# Run tests
python dev.py test

# Build Windows executable
python dev.py build-windows

# Build Linux executable  
python dev.py build-linux

# Clean build artifacts
python dev.py clean

# Show help
python dev.py help
```

## Running the Application

### Development Mode

**Method 1: Use run scripts**
```bash
# Windows
run_modular.bat

# Linux/macOS
./run_modular.sh
```

**Method 2: Direct Python execution**
```bash
python run_modular.py
```

**Method 3: As a module**
```bash
python -m simple_wol
```

### Production Mode (Standalone Executable)

Build the executable first:
```bash
# Windows
build.bat

# Linux/macOS
./build.sh
```

Then run the executable from the `dist/` directory.

## Code Organization

### app.py
- `WakeOnLanApp`: Main application class
- Coordinates between UI and business logic
- Handles device persistence

### device.py
- `Device`: Data model for network devices
- Serialization/deserialization methods

### config/manager.py
- `ConfigManager`: Handles device persistence
- Import/export functionality
- JSON file operations

### ui/main_window.py
- `MainWindow`: Main application window
- Device list management
- Button handlers and context menus

### ui/device_dialog.py
- `DeviceDialog`: Add/edit device dialog
- Form validation
- Device creation/editing

### ui/tooltip.py
- `ToolTip`: Delayed tooltip widget
- `InfoIcon`: Info icon with tooltip

### network/wol.py
- `WakeOnLanSender`: Wake-on-LAN operations
- Network validation utilities

## Adding New Features

### Adding a New UI Component

1. Create a new file in `src/simple_wol/ui/`
2. Import and use in `ui/__init__.py`
3. Use in `main_window.py` or create new dialogs

### Adding Network Functionality

1. Add to `src/simple_wol/network/wol.py`
2. Or create a new module in the `network/` package
3. Import in `network/__init__.py`

### Adding Configuration Options

1. Extend the `Device` class with new fields
2. Update `ConfigManager` serialization if needed
3. Add UI controls in `DeviceDialog`

## Building and Distribution

### PyInstaller Configuration

The build process uses PyInstaller with custom spec files:
- `build/simple_wol.spec` - Windows build configuration
- `build/simple_wol_linux.spec` - Linux build configuration (auto-generated)

### Build Scripts

- `build/build_windows.py` - Windows build script
- `build/build_linux.py` - Linux build script
- `build.bat` / `build.sh` - Simple build wrappers

### Dependencies

Runtime dependencies are listed in `requirements.txt`:
- `wakeonlan` - Wake-on-LAN packet sending

Build dependencies are in `requirements-build.txt`:
- `pyinstaller` - Executable packaging
- `pillow` - Enhanced icon support

## Testing

Basic test structure is in place in the `tests/` directory:
- `test_basic.py` - Basic import tests
- `run_tests.py` - Test runner script

Run tests with:
```bash
python dev.py test
```

## Migration from Monolithic Version

The original `simple_wol.py` file has been split into the modular structure while maintaining all functionality:

- **ToolTip, InfoIcon** → `ui/tooltip.py`
- **Device** → `device.py`
- **ConfigManager** → `config/manager.py`
- **WakeOnLanApp** → `app.py` + `ui/main_window.py`
- **Device dialog** → `ui/device_dialog.py`
- **Wake-on-LAN logic** → `network/wol.py`

All features from the original version are preserved:
- Device management
- Import/export
- Context menus
- Tooltips
- Column sorting
- Icon support
- Update checking (placeholder)

The modular structure makes the code more maintainable and easier to extend for future development.
