# Changelog

All notable changes to the Simple Wake-on-LAN project will be documented in this file.

## [0.1.0] - 2025-06-26

### Major Refactoring - Modular Architecture

#### Added
- **Modular Package Structure**: Split monolithic `simple_wol.py` into organized packages
  - `src/simple_wol/` - Main application package
  - `src/simple_wol/ui/` - User interface components
  - `src/simple_wol/network/` - Network operations
  - `src/simple_wol/config/` - Configuration management
- **New Build System**: PyInstaller-based executable building
  - `build/build_windows.py` - Windows build script
  - `build/build_linux.py` - Linux build script
  - `build.bat` / `build.sh` - Simple build wrappers
  - `build/simple_wol.spec` - PyInstaller configuration
- **Development Tools**:
  - `dev.py` - Development task runner
  - `run_tests.py` - Test runner
  - `run_modular.py` - Modular version runner
  - `run_modular.bat` / `run_modular.sh` - Run scripts
- **Modern Python Packaging**:
  - `pyproject.toml` - Modern Python project configuration
  - Updated `setup.py` for modular structure
  - `requirements-build.txt` - Build dependencies
- **Documentation**:
  - `docs/DEVELOPMENT.md` - Development guide
  - `assets/README.md` - Icon usage guide
  - Updated main `README.md` with new structure
- **Testing Infrastructure**:
  - `tests/` directory structure
  - `tests/test_basic.py` - Basic import tests

#### Changed
- **Code Organization**: Refactored monolithic file into modular components:
  - `WakeOnLanApp` → `app.py` + `ui/main_window.py`
  - `Device` → `device.py`
  - `ConfigManager` → `config/manager.py`
  - `ToolTip`, `InfoIcon` → `ui/tooltip.py`
  - Device dialog → `ui/device_dialog.py`
  - Wake-on-LAN operations → `network/wol.py`
- **Entry Points**: Multiple ways to run the application
  - `python -m simple_wol`
  - `python run_modular.py`
  - Platform-specific run scripts
- **Build Process**: From simple scripts to full PyInstaller workflow
- **Package Structure**: From flat to hierarchical module organization

#### Technical Improvements
- **Maintainability**: Separated concerns into focused modules
- **Scalability**: Easier to add new features and components
- **Testing**: Infrastructure for unit and integration tests
- **Distribution**: Professional build system for standalone executables
- **Documentation**: Comprehensive development and usage guides

#### Preserved Features
All features from the original monolithic version are preserved:
- ✅ Cross-platform GUI (Windows/Linux)
- ✅ Device management (add, edit, remove)
- ✅ Wake-on-LAN packet sending
- ✅ Import/export device configurations
- ✅ Right-click context menus
- ✅ Column sorting
- ✅ Tooltips and help information
- ✅ Custom icon support
- ✅ Update checking placeholder
- ✅ Clipboard operations (copy MAC/IP)
- ✅ Input validation
- ✅ Error handling

#### Migration Path
- Original `simple_wol.py` remains functional
- New modular version available via `run_modular.py`
- Both versions can coexist during transition
- Configuration files (`devices.json`) compatible between versions

#### Future Development Ready
- Modular architecture enables easy feature additions
- Professional build system for distribution
- Test infrastructure for quality assurance
- Documentation for new contributors
- Package structure follows Python best practices

### Notes
This is a major architectural change that transforms a single-file application into a professional, scalable Python package while maintaining all existing functionality and user experience.

## [0.1.1] - 2025-06-26

### Removed - Project Cleanup
- **Obsolete Files Removed**:
  - `simple_wol.py` - Original monolithic file (replaced by modular structure)
  - `install.bat` / `install.sh` - Old installation scripts (replaced by `dev.py`)
  - `test_dependencies.py` - Old dependency test (replaced by proper test suite)
  - `ICON_README.md` - Old icon documentation (replaced by `assets/README.md`)
- **Cache Cleanup**:
  - Removed all `__pycache__` directories
  - Cleaned up build artifacts
- **Improved Clean Function**:
  - Enhanced `dev.py clean` command
  - Comprehensive cleanup of cache files and build artifacts
  - Pattern-based cleanup for thorough maintenance

### Changed
- **Development Workflow**: Updated clean command to handle new structure
- **File Organization**: Removed redundant and obsolete files
- **Documentation**: Streamlined to focus on modular architecture
