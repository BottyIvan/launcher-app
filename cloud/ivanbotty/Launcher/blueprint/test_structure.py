#!/usr/bin/env python3
"""
Blueprint Design Pattern Structure Test

This script validates the blueprint design pattern structure
without requiring GTK to be available.
"""

import sys
import os
import ast

# Add project root to path - find it by looking for pyproject.toml
def find_project_root():
    current = os.path.abspath(os.path.dirname(__file__))
    while current != '/':
        if os.path.exists(os.path.join(current, 'pyproject.toml')):
            return current
        current = os.path.dirname(current)
    # Fallback to relative path if not found
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))

sys.path.insert(0, find_project_root())

def test_file_structure():
    """Test that all blueprint files exist."""
    print("Testing blueprint file structure...")
    files = [
        'cloud/ivanbotty/Launcher/blueprint/__init__.py',
        'cloud/ivanbotty/Launcher/blueprint/style_blueprint.py',
        'cloud/ivanbotty/Launcher/blueprint/component_registry.py',
        'cloud/ivanbotty/Launcher/blueprint/ui_blueprint.py',
        'cloud/ivanbotty/Launcher/blueprint/README.md',
    ]
    
    all_exist = True
    for file in files:
        if os.path.exists(file):
            print(f"✓ {file}")
        else:
            print(f"✗ {file} not found")
            all_exist = False
    
    return all_exist

def test_syntax():
    """Test that all Python files have valid syntax."""
    print("\nTesting Python syntax...")
    files = [
        'cloud/ivanbotty/Launcher/blueprint/__init__.py',
        'cloud/ivanbotty/Launcher/blueprint/style_blueprint.py',
        'cloud/ivanbotty/Launcher/blueprint/component_registry.py',
        'cloud/ivanbotty/Launcher/blueprint/ui_blueprint.py',
        'cloud/ivanbotty/Launcher/app.py',
        'cloud/ivanbotty/Launcher/widget/row.py',
        'cloud/ivanbotty/Launcher/widget/search_entry.py',
    ]
    
    all_valid = True
    for file in files:
        try:
            with open(file, 'r') as f:
                ast.parse(f.read())
            print(f"✓ {file}")
        except SyntaxError as e:
            print(f"✗ {file}: {e}")
            all_valid = False
    
    return all_valid

def test_class_structure():
    """Test that classes are properly defined."""
    print("\nTesting class definitions...")
    
    test_cases = [
        ('cloud/ivanbotty/Launcher/blueprint/style_blueprint.py', 'StyleBlueprint'),
        ('cloud/ivanbotty/Launcher/blueprint/component_registry.py', 'ComponentRegistry'),
        ('cloud/ivanbotty/Launcher/blueprint/ui_blueprint.py', 'UIBlueprint'),
    ]
    
    all_valid = True
    for file, class_name in test_cases:
        try:
            with open(file, 'r') as f:
                tree = ast.parse(f.read())
            
            # Find class definition
            classes = [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
            if class_name in classes:
                print(f"✓ {class_name} class defined in {file}")
            else:
                print(f"✗ {class_name} class not found in {file}")
                all_valid = False
        except Exception as e:
            print(f"✗ Error checking {file}: {e}")
            all_valid = False
    
    return all_valid

def test_method_definitions():
    """Test that key methods are defined."""
    print("\nTesting method definitions...")
    
    test_cases = [
        ('cloud/ivanbotty/Launcher/blueprint/style_blueprint.py', 'StyleBlueprint', 
         ['get_layout', 'apply_margins', 'apply_spacing', 'get_icon_size']),
        ('cloud/ivanbotty/Launcher/blueprint/component_registry.py', 'ComponentRegistry',
         ['create_button', 'create_label', 'create_box', 'create_icon', 'create_entry']),
        ('cloud/ivanbotty/Launcher/blueprint/ui_blueprint.py', 'UIBlueprint',
         ['create_window', 'create_search_bar', 'create_main_list_view', 'create_main_layout']),
    ]
    
    all_valid = True
    for file, class_name, methods in test_cases:
        try:
            with open(file, 'r') as f:
                tree = ast.parse(f.read())
            
            # Find class and its methods
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef) and node.name == class_name:
                    class_methods = [m.name for m in node.body if isinstance(m, ast.FunctionDef)]
                    for method in methods:
                        if method in class_methods:
                            print(f"✓ {class_name}.{method}()")
                        else:
                            print(f"✗ {class_name}.{method}() not found")
                            all_valid = False
                    break
        except Exception as e:
            print(f"✗ Error checking {file}: {e}")
            all_valid = False
    
    return all_valid

def test_integration():
    """Test that app.py uses the blueprint."""
    print("\nTesting integration...")
    
    try:
        with open('cloud/ivanbotty/Launcher/app.py', 'r') as f:
            content = f.read()
        
        checks = [
            ('UIBlueprint import', 'from cloud.ivanbotty.Launcher.blueprint import UIBlueprint'),
            ('Blueprint initialization', 'self.ui_blueprint = UIBlueprint()'),
            ('Blueprint usage', 'self.ui_blueprint.create_'),
        ]
        
        all_valid = True
        for name, pattern in checks:
            if pattern in content:
                print(f"✓ {name}")
            else:
                print(f"✗ {name} not found")
                all_valid = False
        
        return all_valid
    except Exception as e:
        print(f"✗ Error checking integration: {e}")
        return False

def test_documentation():
    """Test that documentation exists and is comprehensive."""
    print("\nTesting documentation...")
    
    try:
        with open('cloud/ivanbotty/Launcher/blueprint/README.md', 'r') as f:
            content = f.read()
        
        sections = [
            'Overview',
            'Architecture',
            'StyleBlueprint',
            'ComponentRegistry',
            'UIBlueprint',
            'Benefits',
            'Usage',
        ]
        
        all_found = True
        for section in sections:
            if section in content:
                print(f"✓ Section: {section}")
            else:
                print(f"✗ Section not found: {section}")
                all_found = False
        
        # Check length
        word_count = len(content.split())
        print(f"✓ Documentation length: {word_count} words")
        
        return all_found
    except Exception as e:
        print(f"✗ Error checking documentation: {e}")
        return False

def main():
    """Run all tests."""
    print("=" * 60)
    print("Blueprint Design Pattern Structure Test")
    print("=" * 60)
    
    tests = [
        test_file_structure,
        test_syntax,
        test_class_structure,
        test_method_definitions,
        test_integration,
        test_documentation,
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    print("\n" + "=" * 60)
    passed = sum(results)
    total = len(results)
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("✓ All structure tests passed!")
        print("\nNote: Runtime tests require GTK4 and cannot be run in this environment.")
        print("The application should be tested manually in a GTK4-enabled environment.")
        return 0
    else:
        print("✗ Some tests failed")
        return 1

if __name__ == '__main__':
    sys.exit(main())
