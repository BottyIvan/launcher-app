"""Common utilities for the launcher application.

This module provides utility functions for locating resource files
in various installation environments (direct execution, Meson, Flatpak).
"""
import os
import sys
from typing import Optional

# Constants for resource paths
# Note: PKGDATADIR must match the project name in meson.build
PKGDATADIR = "launcher-app"
RESOURCE_SUBDIR = "Launcher/resources"
RESOURCE_FILE = "resources.gresource"


def find_resource_file() -> Optional[str]:
    """Find the resources.gresource file in various possible locations.
    
    This function searches for the resource file in multiple locations to support
    both direct Python execution from the repository and Meson-based installations,
    including Flatpak environments.
    
    Returns:
        Path to the resource file if found, None otherwise
    """
    # Build the resource filename path
    resource_filename = os.path.join(RESOURCE_SUBDIR, RESOURCE_FILE)
    
    # Define possible search paths
    search_paths = [
        # Direct execution from repository root
        os.path.join("cloud", "ivanbotty", resource_filename),
        # Flatpak installation (in /app)
        os.path.join("/app", "share", PKGDATADIR, resource_filename),
        # Meson installation (in pkgdatadir using sys.prefix)
        os.path.join(sys.prefix, "share", PKGDATADIR, resource_filename),
        # Standard installation locations
        os.path.join("/usr", "share", PKGDATADIR, resource_filename),
        os.path.join("/usr", "local", "share", PKGDATADIR, resource_filename),
    ]
    
    for path in search_paths:
        if os.path.exists(path):
            return path
    
    return None

