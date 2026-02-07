#!/usr/bin/env python
"""
Comprehensive validation script for Mail2PDF NextGen configuration feature.
"""
import json
import sys
from pathlib import Path

def validate_json_file(filepath):
    """Validate JSON syntax."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            json.load(f)
        print(f"✓ {filepath} is valid JSON")
        return True
    except json.JSONDecodeError as e:
        print(f"✗ {filepath} has JSON error: {e}")
        return False
    except Exception as e:
        print(f"✗ {filepath} error: {e}")
        return False

def validate_python_syntax(filepath):
    """Validate Python syntax."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            code = f.read()
        compile(code, filepath, 'exec')
        print(f"✓ {filepath} has valid Python syntax")
        return True
    except SyntaxError as e:
        print(f"✗ {filepath} has syntax error at line {e.lineno}: {e.msg}")
        return False
    except Exception as e:
        print(f"✗ {filepath} error: {e}")
        return False

def main():
    """Run all validation checks."""
    print("=" * 60)
    print("Mail2PDF NextGen - Configuration Feature Validation")
    print("=" * 60)
    
    all_passed = True
    
    # Validate JSON files
    print("\n[1/3] Validating JSON files...")
    json_files = [
        'data/config_dynamic.json',
        'data/languages.json'
    ]
    
    for json_file in json_files:
        if not validate_json_file(json_file):
            all_passed = False
    
    # Validate Python files
    print("\n[2/3] Validating Python syntax...")
    py_files = [
        'app.py',
        'tests/test_ui_config.py'
    ]
    
    for py_file in py_files:
        if Path(py_file).exists():
            if not validate_python_syntax(py_file):
                all_passed = False
        else:
            print(f"⚠ {py_file} not found")
    
# Check required directories
    print("\n[3/3] Checking directory structure...")
    required_dirs = [
        'data',
        'static/logos',
        'templates',
        'tests'
    ]
    
    for directory in required_dirs:
        path = Path(directory)
        if path.exists():
            print(f"✓ {directory}/ exists")
        else:
            print(f"✗ {directory}/ missing")
            all_passed = False
    
    # Final summary
    print("\n" + "=" * 60)
    if all_passed:
        print("✓ ALL VALIDATIONS PASSED")
        print("=" * 60)
        return 0
    else:
        print("✗ SOME VALIDATIONS FAILED")
        print("=" * 60)
        return 1

if __name__ == '__main__':
    sys.exit(main())
