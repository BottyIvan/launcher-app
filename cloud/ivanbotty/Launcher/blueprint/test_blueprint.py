#!/usr/bin/env python3
"""
Blueprint Design Pattern Test Script

This script tests the blueprint design pattern implementation
to ensure all components can be instantiated correctly.
"""

import sys
import os

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

def test_imports():
    """Test that all blueprint modules can be imported."""
    print("Testing blueprint imports...")
    try:
        from cloud.ivanbotty.Launcher.blueprint import UIBlueprint, ComponentRegistry, StyleBlueprint
        print("✓ Blueprint modules imported successfully")
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False

def test_style_blueprint():
    """Test StyleBlueprint functionality."""
    print("\nTesting StyleBlueprint...")
    try:
        from cloud.ivanbotty.Launcher.blueprint.style_blueprint import StyleBlueprint
        
        # Test initialization
        style = StyleBlueprint()
        assert style.current_style in [StyleBlueprint.COMPACT, StyleBlueprint.DEFAULT]
        print(f"✓ Current style: {style.current_style}")
        
        # Test layout retrieval
        layout = style.get_layout()
        assert 'window_width' in layout
        assert 'margin_start' in layout
        print(f"✓ Layout configuration loaded: {len(layout)} properties")
        
        # Test spacing values
        assert 'md' in style.SPACING
        print(f"✓ Spacing values available: {list(style.SPACING.keys())}")
        
        # Test icon sizes
        icon_size = style.get_icon_size('md')
        assert isinstance(icon_size, int)
        print(f"✓ Icon size (md): {icon_size}px")
        
        return True
    except Exception as e:
        print(f"✗ StyleBlueprint test failed: {e}")
        return False

def test_component_structure():
    """Test component registry structure."""
    print("\nTesting ComponentRegistry structure...")
    try:
        from cloud.ivanbotty.Launcher.blueprint.component_registry import ComponentRegistry
        from cloud.ivanbotty.Launcher.blueprint.style_blueprint import StyleBlueprint
        
        # Test initialization
        style = StyleBlueprint()
        registry = ComponentRegistry(style)
        print("✓ ComponentRegistry initialized")
        
        # Check that key methods exist
        methods = [
            'create_button',
            'create_icon_button',
            'create_label',
            'create_box',
            'create_icon',
            'create_scrolled_window',
            'create_entry',
            'create_list_box',
            'create_tag_button'
        ]
        
        for method in methods:
            assert hasattr(registry, method)
            print(f"✓ Method exists: {method}")
        
        return True
    except Exception as e:
        print(f"✗ ComponentRegistry test failed: {e}")
        return False

def test_ui_blueprint_structure():
    """Test UI blueprint structure."""
    print("\nTesting UIBlueprint structure...")
    try:
        from cloud.ivanbotty.Launcher.blueprint.ui_blueprint import UIBlueprint
        
        # Test initialization
        ui = UIBlueprint()
        print("✓ UIBlueprint initialized")
        
        # Check that style and components are initialized
        assert hasattr(ui, 'style')
        assert hasattr(ui, 'components')
        print("✓ Style and components initialized")
        
        # Check that key methods exist
        methods = [
            'create_window',
            'create_search_bar',
            'create_main_list_view',
            'create_footer_layout',
            'create_progress_bar',
            'create_main_layout',
            'create_list_row'
        ]
        
        for method in methods:
            assert hasattr(ui, method)
            print(f"✓ Method exists: {method}")
        
        return True
    except Exception as e:
        print(f"✗ UIBlueprint test failed: {e}")
        return False

def test_integration():
    """Test integration with existing code."""
    print("\nTesting integration with existing code...")
    try:
        # Check that modified files still parse correctly
        import ast
        files = [
            'cloud/ivanbotty/Launcher/app.py',
            'cloud/ivanbotty/Launcher/widget/row.py',
            'cloud/ivanbotty/Launcher/widget/search_entry.py'
        ]
        
        for file in files:
            with open(file, 'r') as f:
                ast.parse(f.read())
            print(f"✓ {file} parses correctly")
        
        return True
    except Exception as e:
        print(f"✗ Integration test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("=" * 60)
    print("Blueprint Design Pattern Test Suite")
    print("=" * 60)
    
    tests = [
        test_imports,
        test_style_blueprint,
        test_component_structure,
        test_ui_blueprint_structure,
        test_integration
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    print("\n" + "=" * 60)
    passed = sum(results)
    total = len(results)
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("✓ All tests passed!")
        return 0
    else:
        print("✗ Some tests failed")
        return 1

if __name__ == '__main__':
    sys.exit(main())
