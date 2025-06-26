#!/usr/bin/env python3
"""
Test script for Simple Wake-on-LAN application
"""

import sys
import importlib.util

def test_python_version():
    """Test if Python version is compatible."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        return False, f"Python {version.major}.{version.minor} found, but 3.7+ required"
    return True, f"Python {version.major}.{version.minor}.{version.micro} - OK"

def test_module(module_name):
    """Test if a module can be imported."""
    try:
        spec = importlib.util.find_spec(module_name)
        if spec is None:
            return False, f"{module_name} not found"
        return True, f"{module_name} - OK"
    except Exception as e:
        return False, f"{module_name} - Error: {str(e)}"

def main():
    """Run all tests."""
    print("Simple Wake-on-LAN - System Test")
    print("=" * 40)
    
    tests = [
        ("Python Version", test_python_version),
        ("tkinter", lambda: test_module("tkinter")),
        ("json", lambda: test_module("json")),
        ("socket", lambda: test_module("socket")),
        ("re", lambda: test_module("re")),
        ("os", lambda: test_module("os")),
    ]
    
    all_passed = True
    
    for test_name, test_func in tests:
        try:
            passed, message = test_func()
            status = "✓ PASS" if passed else "✗ FAIL"
            print(f"{test_name:15} {status:8} {message}")
            if not passed:
                all_passed = False
        except Exception as e:
            print(f"{test_name:15} ✗ FAIL    Error: {str(e)}")
            all_passed = False
    
    print("\n" + "=" * 40)
    
    # Test wakeonlan separately as it might not be installed yet
    wakeonlan_passed, wakeonlan_msg = test_module("wakeonlan")
    print(f"{'wakeonlan':15} {'✓ PASS' if wakeonlan_passed else '✗ FAIL':8} {wakeonlan_msg}")
    
    if not wakeonlan_passed:
        print("\nTo install wakeonlan, run:")
        print("  pip install wakeonlan")
        print("  or")
        print("  pip install -r requirements.txt")
    
    if all_passed:
        print("\n✓ All core dependencies are available!")
        if wakeonlan_passed:
            print("✓ Ready to run Simple Wake-on-LAN!")
        else:
            print("! Install wakeonlan to complete setup")
    else:
        print("\n✗ Some dependencies are missing. Please check the installation.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
