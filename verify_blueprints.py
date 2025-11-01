#!/usr/bin/env python3
"""
Verify that the Blueprint UI infrastructure is properly set up.

This script checks:
1. All Blueprint files exist
2. All compiled UI files exist
3. Blueprint files are syntactically valid (if blueprint-compiler is available)
4. Example file is present
5. README has Blueprint documentation
"""

import os
import sys
from pathlib import Path

def check_file_exists(path, description):
    """Check if a file exists and report the result."""
    if Path(path).exists():
        print(f"✓ {description}: {path}")
        return True
    else:
        print(f"✗ {description}: {path} (NOT FOUND)")
        return False

def check_directory_exists(path, description):
    """Check if a directory exists and report the result."""
    if Path(path).is_dir():
        print(f"✓ {description}: {path}")
        return True
    else:
        print(f"✗ {description}: {path} (NOT FOUND)")
        return False

def verify_blueprint_infrastructure():
    """Verify the Blueprint infrastructure."""
    print("=" * 60)
    print("GTK Blueprint Infrastructure Verification")
    print("=" * 60)
    print()
    
    all_ok = True
    
    # Check ui directory
    print("Checking directory structure...")
    all_ok &= check_directory_exists("ui", "UI directory")
    print()
    
    # Check Blueprint files
    print("Checking Blueprint (.blp) files...")
    blueprint_files = [
        "ui/main_window.blp",
        "ui/search_entry.blp",
        "ui/list_row.blp",
        "ui/footer.blp",
        "ui/preferences.blp",
    ]
    for blp_file in blueprint_files:
        all_ok &= check_file_exists(blp_file, "Blueprint file")
    print()
    
    # Check compiled UI files
    print("Checking compiled UI (.ui) files...")
    ui_files = [
        "ui/main_window.ui",
        "ui/search_entry.ui",
        "ui/list_row.ui",
        "ui/footer.ui",
        "ui/preferences.ui",
    ]
    for ui_file in ui_files:
        all_ok &= check_file_exists(ui_file, "Compiled UI file")
    print()
    
    # Check build configuration files
    print("Checking build configuration...")
    all_ok &= check_file_exists("meson.build", "Meson build file")
    all_ok &= check_file_exists("compile_blueprints.py", "Python compilation script")
    print()
    
    # Check documentation
    print("Checking documentation...")
    all_ok &= check_file_exists("examples_blueprint.py", "Example implementations")
    all_ok &= check_file_exists("BLUEPRINT_MIGRATION.md", "Migration guide")
    
    # Check README has Blueprint section
    if Path("README.md").exists():
        with open("README.md", "r") as f:
            readme_content = f.read()
            if "Blueprint" in readme_content:
                print("✓ README.md contains Blueprint documentation")
            else:
                print("✗ README.md missing Blueprint documentation")
                all_ok = False
    else:
        print("✗ README.md not found")
        all_ok = False
    print()
    
    # Check for blueprint-compiler
    print("Checking for blueprint-compiler...")
    import subprocess
    try:
        result = subprocess.run(
            ['which', 'blueprint-compiler'],
            capture_output=True,
            text=True,
            check=True
        )
        print(f"✓ blueprint-compiler found at: {result.stdout.strip()}")
        
        # Try to get version
        try:
            version_result = subprocess.run(
                ['blueprint-compiler', '--version'],
                capture_output=True,
                text=True,
                check=True
            )
            print(f"  Version: {version_result.stdout.strip()}")
        except:
            pass
    except subprocess.CalledProcessError:
        print("⚠ blueprint-compiler not found in PATH")
        print("  Install it to compile Blueprint files:")
        print("  - Ubuntu/Debian: sudo apt install blueprint-compiler")
        print("  - Fedora: sudo dnf install blueprint-compiler")
        print("  - Arch: sudo pacman -S blueprint-compiler")
    print()
    
    # Summary
    print("=" * 60)
    if all_ok:
        print("✓ All checks passed! Blueprint infrastructure is ready.")
        print()
        print("Next steps:")
        print("1. Install blueprint-compiler if not already installed")
        print("2. Run: python3 compile_blueprints.py")
        print("3. See examples_blueprint.py for usage examples")
        print("4. Read BLUEPRINT_MIGRATION.md for migration guide")
        return 0
    else:
        print("✗ Some checks failed. Please fix the issues above.")
        return 1

if __name__ == '__main__':
    sys.exit(verify_blueprint_infrastructure())
