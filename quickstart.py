#!/usr/bin/env python3
"""
Mail2PDF NextGen - Interactive Setup Assistant
Ville de Fontaine 38600, France
"""

import os
import sys
import subprocess
from pathlib import Path

def print_header(text):
    """Print formatted header."""
    print("\n" + "=" * 80)
    print(text)
    print("=" * 80)

def check_python_version():
    """Check Python version."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("✗ Python 3.8+ required")
        return False
    print(f"✓ Python {version.major}.{version.minor}.{version.micro}")
    return True

def check_pip():
    """Check if pip is available."""
    try:
        subprocess.run(['pip', '--version'], capture_output=True, check=True)
        print("✓ pip is available")
        return True
    except Exception:
        print("✗ pip not found")
        return False

def install_dependencies():
    """Install required dependencies."""
    print("\nInstalling dependencies...")
    
    try:
        subprocess.run([
            sys.executable, '-m', 'pip', 'install', '-q', '-r', 'requirements.txt'
        ], check=True)
        print("✓ Dependencies installed")
        return True
    except Exception as e:
        print(f"✗ Failed to install dependencies: {e}")
        return False

def create_directories():
    """Create necessary directories."""
    print("\nCreating directories...")
    
    dirs = [
        'data/input',
        'data/output',
        'data/sessions'
    ]
    
    for dir_path in dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        print(f"✓ {dir_path}")
    
    return True

def test_imports():
    """Test if all required modules can be imported."""
    print("\nTesting imports...")
    
    modules = [
        'flask',
        'weasyprint',
        'chardet',
        'extract_msg',
        'PIL'
    ]
    
    all_ok = True
    
    for module in modules:
        try:
            __import__(module)
            print(f"✓ {module}")
        except ImportError:
            print(f"✗ {module} (optional)")
            all_ok = False
    
    return all_ok

def test_app():
    """Quick test of the application."""
    print("\nRunning quick validation test...")
    
    try:
        from main import EmailConverter
        
        converter = EmailConverter()
        
        # Test with example file
        test_file = Path('data/input/test_email.eml')
        
        if test_file.exists():
            result = converter.validate(str(test_file))
            
            if result['parseable']:
                print(f"✓ Test email parsed successfully")
                return True
            else:
                print(f"✗ Test email parsing failed")
                return False
        else:
            print("ℹ Test email not found (skip)")
            return True
    
    except Exception as e:
        print(f"✗ Test failed: {e}")
        return False

def show_next_steps():
    """Show next steps."""
    print_header("Setup Complete!")
    
    print("""
🎉 Mail2PDF NextGen is ready to use!

Next Steps:

1. CLI Usage:
   python main.py -i data/input/test_email.eml -o data/output

2. Web Interface:
   python app.py
   Then visit: http://localhost:5000

3. Docker:
   docker-compose up -d
   Then visit: http://localhost:5000

4. Examples:
   python examples.py

5. Validation Tests:
   python validate.py

6. Learn More:
   - README.md: Complete guide
   - documentation.html: API docs
   - examples.py: Code examples

📚 For help:
   - See DEPLOYMENT_GITHUB.md for GitHub setup
   - See DEPLOYMENT_DOCKER.md for Docker guide
   - See FULL_DOCUMENTATION.md for technical details

Happy converting! 📧→📄
""")

def main():
    """Run setup wizard."""
    print_header("Mail2PDF NextGen - Setup Wizard")
    
    print(f"\nVersion: 1.0.0")
    print(f"Author: Ville de Fontaine 38600")
    print(f"License: MIT")
    
    checks = [
        ("Python Version", check_python_version),
        ("pip Installation", check_pip),
        ("Create Directories", create_directories),
        ("Install Dependencies", install_dependencies),
        ("Test Imports", test_imports),
        ("Test Application", test_app),
    ]
    
    for check_name, check_func in checks:
        try:
            if check_func():
                print(f"✓ {check_name}")
            else:
                print(f"✗ {check_name}")
                if "Install" in check_name:
                    print("\nSetup failed. Please install dependencies manually:")
                    print(f"  {sys.executable} -m pip install -r requirements.txt")
                    sys.exit(1)
        except Exception as e:
            print(f"✗ {check_name}: {e}")
            sys.exit(1)
    
    show_next_steps()

if __name__ == '__main__':
    main()
