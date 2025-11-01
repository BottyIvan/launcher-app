#!/usr/bin/env python3
"""
Validation script for Wizard Blueprint UI integration.

This script validates that all the necessary files and structure
are in place for the Blueprint UI implementation.
"""

import os
import sys
from pathlib import Path

# Version requirements
MIN_GTK_VERSION = "4.0"
MIN_ADW_VERSION = "1"
MIN_BLUEPRINT_COMPILER_VERSION = "0.4.0"


def check_file_exists(filepath, description):
    """Check if a file exists and report."""
    exists = os.path.exists(filepath)
    status = "✓" if exists else "✗"
    print(f"{status} {description}: {filepath}")
    return exists


def check_directory_exists(dirpath, description):
    """Check if a directory exists and report."""
    exists = os.path.isdir(dirpath)
    status = "✓" if exists else "✗"
    print(f"{status} {description}: {dirpath}")
    return exists


def validate_blueprint_structure():
    """Validate the Blueprint UI structure."""
    print("=" * 70)
    print("Validating GNOME Blueprint UI Structure for Wizard Module")
    print("=" * 70)
    
    # Get the script's location and navigate to the Wizard directory
    script_path = Path(__file__).resolve()
    wizard_path = script_path.parent
    
    all_checks = []
    
    # Check directories
    print("\n📁 Directory Structure:")
    all_checks.append(check_directory_exists(
        wizard_path / "resources",
        "Resources directory"
    ))
    all_checks.append(check_directory_exists(
        wizard_path / "resources" / "blueprints",
        "Blueprints directory"
    ))
    all_checks.append(check_directory_exists(
        wizard_path / "resources" / "ui",
        "UI output directory"
    ))
    
    # Check Blueprint files
    print("\n📄 Blueprint Files:")
    blueprint_files = [
        ("wizard-window.blp", "Main window Blueprint"),
        ("welcome-page.blp", "Welcome page Blueprint"),
        ("summary-page.blp", "Summary page Blueprint"),
        ("wizard-page.blp", "Generic page Blueprint"),
    ]
    
    for filename, description in blueprint_files:
        all_checks.append(check_file_exists(
            wizard_path / "resources" / "blueprints" / filename,
            description
        ))
    
    # Check configuration files
    print("\n⚙️  Configuration Files:")
    all_checks.append(check_file_exists(
        wizard_path / "resources" / "wizard.gresource.xml",
        "GResource XML definition"
    ))
    all_checks.append(check_file_exists(
        wizard_path / "meson.build",
        "Meson build file"
    ))
    
    # Check Python modules
    print("\n🐍 Python Modules:")
    python_files = [
        ("blueprint_ui.py", "Blueprint UI loader module"),
        ("app_blueprint_example.py", "Example Blueprint integration"),
        ("app.py", "Original wizard app"),
        ("__main__.py", "Main entry point"),
    ]
    
    for filename, description in python_files:
        all_checks.append(check_file_exists(
            wizard_path / filename,
            description
        ))
    
    # Check documentation
    print("\n📚 Documentation:")
    all_checks.append(check_file_exists(
        wizard_path / "resources" / "README.md",
        "Blueprint documentation"
    ))
    
    # Summary
    print("\n" + "=" * 70)
    passed = sum(all_checks)
    total = len(all_checks)
    print(f"Validation Result: {passed}/{total} checks passed")
    
    if passed == total:
        print("✅ All validation checks passed!")
        print("\nNext steps:")
        print("1. Build the project with Meson")
        print("2. Ensure blueprint-compiler is installed")
        print("3. Run the wizard to test the UI")
        return 0
    else:
        print("❌ Some validation checks failed!")
        print("\nPlease ensure all required files are in place.")
        return 1


def validate_blueprint_syntax():
    """Basic validation of Blueprint file syntax."""
    print("\n" + "=" * 70)
    print("Validating Blueprint File Syntax")
    print("=" * 70)
    
    script_path = Path(__file__).resolve()
    wizard_path = script_path.parent
    blueprints_path = wizard_path / "resources" / "blueprints"
    
    if not blueprints_path.exists():
        print("❌ Blueprints directory not found")
        return 1
    
    all_valid = True
    for blp_file in blueprints_path.glob("*.blp"):
        print(f"\n📄 Checking {blp_file.name}...")
        try:
            with open(blp_file, 'r') as f:
                content = f.read()
                
            # Basic syntax checks
            checks = [
                (f"using Gtk {MIN_GTK_VERSION};" in content, f"Uses GTK {MIN_GTK_VERSION}"),
                (f"using Adw {MIN_ADW_VERSION};" in content, f"Uses Adwaita {MIN_ADW_VERSION}"),
                ("template " in content, "Has template definition"),
                (content.count("{") == content.count("}"), "Balanced braces"),
            ]
            
            for check, description in checks:
                status = "✓" if check else "✗"
                print(f"  {status} {description}")
                if not check:
                    all_valid = False
                    
        except Exception as e:
            print(f"  ✗ Error reading file: {e}")
            all_valid = False
    
    if all_valid:
        print("\n✅ All Blueprint files have valid basic syntax")
        return 0
    else:
        print("\n❌ Some Blueprint files have syntax issues")
        return 1


def validate_meson_build():
    """Validate meson.build configuration."""
    print("\n" + "=" * 70)
    print("Validating Meson Build Configuration")
    print("=" * 70)
    
    script_path = Path(__file__).resolve()
    wizard_path = script_path.parent
    meson_file = wizard_path / "meson.build"
    
    if not meson_file.exists():
        print("❌ meson.build not found")
        return 1
    
    try:
        with open(meson_file, 'r') as f:
            content = f.read()
        
        # Check for required elements
        checks = [
            ("blueprint_compiler" in content, "Blueprint compiler detection"),
            ("find_program('blueprint-compiler'" in content, "Blueprint compiler program search"),
            ("custom_target" in content, "Custom target for compilation"),
            ("batch-compile" in content, "Batch compilation command"),
            ("gnome.compile_resources" in content, "GResource compilation"),
            ("wizard.gresource.xml" in content, "GResource XML reference"),
            ("blueprint_ui.py" in content, "Blueprint UI module in sources"),
        ]
        
        print("\n⚙️  Meson configuration checks:")
        all_valid = True
        for check, description in checks:
            status = "✓" if check else "✗"
            print(f"  {status} {description}")
            if not check:
                all_valid = False
        
        if all_valid:
            print("\n✅ Meson build configuration is valid")
            return 0
        else:
            print("\n❌ Meson build configuration has issues")
            return 1
            
    except Exception as e:
        print(f"❌ Error reading meson.build: {e}")
        return 1


if __name__ == "__main__":
    results = []
    
    # Run all validations
    results.append(validate_blueprint_structure())
    results.append(validate_blueprint_syntax())
    results.append(validate_meson_build())
    
    # Final summary
    print("\n" + "=" * 70)
    print("FINAL VALIDATION SUMMARY")
    print("=" * 70)
    
    if all(r == 0 for r in results):
        print("✅ All validations passed successfully!")
        print("\nThe GNOME Blueprint UI integration is complete and ready to build.")
        sys.exit(0)
    else:
        print("❌ Some validations failed. Please review the output above.")
        sys.exit(1)
