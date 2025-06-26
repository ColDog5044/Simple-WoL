#!/usr/bin/env python3
"""
Development task runner for Simple Wake-on-LAN application.
"""

import sys
import os
import subprocess
import argparse
import glob
from pathlib import Path

def run_command(cmd, description):
    """Run a command and print status."""
    print(f"➤ {description}")
    result = subprocess.run(cmd, shell=True)
    if result.returncode == 0:
        print("✓ Success\n")
    else:
        print(f"✗ Failed with exit code {result.returncode}\n")
    return result.returncode

def install_deps():
    """Install runtime dependencies."""
    return run_command(
        "python -m pip install -r requirements.txt",
        "Installing runtime dependencies"
    )

def install_build_deps():
    """Install build dependencies."""
    return run_command(
        "python -m pip install -r requirements-build.txt",
        "Installing build dependencies"
    )

def run_app():
    """Run the application in development mode."""
    return run_command(
        "python run_modular.py",
        "Running application in development mode"
    )

def run_tests():
    """Run the test suite."""
    return run_command(
        "python run_tests.py",
        "Running test suite"
    )

def build_windows():
    """Build Windows executable."""
    return run_command(
        "python build/build_windows.py",
        "Building Windows executable"
    )

def build_linux():
    """Build Linux executable."""
    return run_command(
        "python build/build_linux.py",
        "Building Linux executable"
    )

def clean():
    """Clean build artifacts and cache files."""
    import shutil
    import glob
    
    # Directories to clean
    dirs_to_clean = [
        'dist', 
        'build/__pycache__',
        'src/simple_wol/__pycache__',
        'src/simple_wol/ui/__pycache__',
        'src/simple_wol/network/__pycache__',
        'src/simple_wol/config/__pycache__',
        'tests/__pycache__',
    ]
    
    # Files to clean
    files_to_clean = [
        'build/simple_wol_linux.spec',
    ]
    
    # Pattern-based cleanup
    patterns_to_clean = [
        '**/*.pyc',
        '**/*.pyo',
        '**/__pycache__',
    ]
    
    print("🧹 Cleaning build artifacts and cache files...")
    
    # Clean directories
    for dir_path in dirs_to_clean:
        if os.path.exists(dir_path):
            print(f"➤ Removing directory: {dir_path}")
            shutil.rmtree(dir_path)
            print("✓ Removed")
    
    # Clean individual files
    for file_path in files_to_clean:
        if os.path.exists(file_path):
            print(f"➤ Removing file: {file_path}")
            os.remove(file_path)
            print("✓ Removed")
    
    # Clean by patterns
    for pattern in patterns_to_clean:
        for path in glob.glob(pattern, recursive=True):
            if os.path.isfile(path):
                print(f"➤ Removing: {path}")
                os.remove(path)
                print("✓ Removed")
            elif os.path.isdir(path):
                print(f"➤ Removing directory: {path}")
                shutil.rmtree(path)
                print("✓ Removed")
    
    print("\n✨ Cleanup complete!")

def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Development task runner")
    parser.add_argument('task', choices=[
        'install', 'install-build', 'run', 'test', 'build-windows', 
        'build-linux', 'clean', 'help'
    ], help='Task to run')
    
    args = parser.parse_args()
    
    if args.task == 'help':
        print("Available tasks:")
        print("  install       - Install runtime dependencies")
        print("  install-build - Install build dependencies")
        print("  run          - Run application in development mode")
        print("  test         - Run test suite")
        print("  build-windows - Build Windows executable")
        print("  build-linux  - Build Linux executable")
        print("  clean        - Clean build artifacts")
        return 0
    
    task_map = {
        'install': install_deps,
        'install-build': install_build_deps,
        'run': run_app,
        'test': run_tests,
        'build-windows': build_windows,
        'build-linux': build_linux,
        'clean': clean,
    }
    
    return task_map[args.task]()

if __name__ == '__main__':
    sys.exit(main())
