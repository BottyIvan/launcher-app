#!/usr/bin/env python3
"""
Compile Blueprint (.blp) files to GTK UI (.ui) files.

This script provides an alternative to meson for compiling Blueprint files.
It can be used to compile the UI files before running the application directly
with python3.
"""

import os
import sys
import subprocess
from pathlib import Path

def find_blueprint_compiler():
    """Find the blueprint-compiler executable."""
    try:
        result = subprocess.run(
            ['which', 'blueprint-compiler'],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        print("Error: blueprint-compiler not found in PATH")
        print("Please install blueprint-compiler:")
        print("  - On Ubuntu/Debian: sudo apt install blueprint-compiler")
        print("  - On Fedora: sudo dnf install blueprint-compiler")
        print("  - On Arch: sudo pacman -S blueprint-compiler")
        print("  - Or via Flatpak: flatpak install flathub com.github.jwestman.blueprint-compiler")
        return None

def compile_blueprint_file(blueprintc, blp_file, ui_file):
    """Compile a single Blueprint file to UI file."""
    try:
        print(f"Compiling {blp_file} -> {ui_file}")
        result = subprocess.run(
            [blueprintc, 'compile', '--output', ui_file, blp_file],
            capture_output=True,
            text=True,
            check=True
        )
        if result.returncode == 0:
            print(f"  ✓ Successfully compiled {blp_file}")
            return True
        else:
            print(f"  ✗ Failed to compile {blp_file}")
            print(f"    stdout: {result.stdout}")
            print(f"    stderr: {result.stderr}")
            return False
    except subprocess.CalledProcessError as e:
        print(f"  ✗ Failed to compile {blp_file}")
        print(f"    Error: {e}")
        print(f"    stdout: {e.stdout}")
        print(f"    stderr: {e.stderr}")
        return False

def compile_all_blueprints():
    """Compile all Blueprint files in the ui/ directory."""
    # Get the project root directory
    script_dir = Path(__file__).parent
    ui_dir = script_dir / 'ui'
    
    if not ui_dir.exists():
        print(f"Error: UI directory not found at {ui_dir}")
        return 1
    
    # Find blueprint-compiler
    blueprintc = find_blueprint_compiler()
    if not blueprintc:
        return 1
    
    # Find all .blp files
    blp_files = list(ui_dir.glob('*.blp'))
    if not blp_files:
        print(f"No Blueprint files found in {ui_dir}")
        return 1
    
    print(f"Found {len(blp_files)} Blueprint file(s)")
    print()
    
    # Compile each file
    success_count = 0
    failed_count = 0
    
    for blp_file in blp_files:
        ui_file = blp_file.with_suffix('.ui')
        if compile_blueprint_file(blueprintc, str(blp_file), str(ui_file)):
            success_count += 1
        else:
            failed_count += 1
    
    print()
    print(f"Compilation complete: {success_count} succeeded, {failed_count} failed")
    
    return 0 if failed_count == 0 else 1

if __name__ == '__main__':
    sys.exit(compile_all_blueprints())
