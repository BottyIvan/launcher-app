"""Dynamic class loading utilities.

This module provides functionality for dynamically importing and instantiating
classes from full module paths, used for loading extensions and handlers.
"""

import importlib
import logging
from typing import Any, Optional

logger = logging.getLogger(__name__)

# Cache for loaded class instances
_instance_cache = {}


def load_class_instance(path: str) -> Optional[Any]:
    """Dynamically import a class from a full path and return an instance.

    Args:
        path: Full class path as a string, e.g.
              "cloud.ivanbotty.Launcher.handlers.math_handler.MathHandler"

    Returns:
        Instance of the specified class, or None if import/instantiation fails
    """
    # Check cache first
    if path in _instance_cache:
        logger.debug(f"Returning cached instance for: {path}")
        return _instance_cache[path]

    try:
        module_path, class_name = path.rsplit(".", 1)
    except ValueError:
        logger.error(f"Invalid path format: {path}")
        return None

    try:
        module = importlib.import_module(module_path)
        logger.debug(f"Module imported successfully: {module_path}")
    except ImportError as e:
        logger.error(f"Failed to import module {module_path}: {e}")
        return None

    logger.debug(f"Looking for class {class_name} in module {module_path}")
    try:
        cls = getattr(module, class_name)
        logger.debug(f"Class found: {class_name} in {module_path}")
    except AttributeError:
        logger.error(f"Class not found: {class_name} in {module_path}")
        return None

    try:
        instance = cls()
        logger.debug(f"Instance created successfully: {class_name}")
        # Cache the instance for future use
        _instance_cache[path] = instance
    except Exception as e:
        logger.error(f"Failed to instantiate class {class_name}: {e}")
        return None

    return instance
