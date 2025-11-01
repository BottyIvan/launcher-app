import importlib
import logging

logger = logging.getLogger(__name__)

def load_class_instance(path: str):
    """
    Dynamically imports a class from a full path and returns an instance.

    path: full class path as a string, e.g.
          "cloud.ivanbotty.Launcher.handlers.math_handler.MathHandler"
    """
    module_path, class_name = path.rsplit(".", 1)
    try:
        module = importlib.import_module(module_path)
        logger.debug(f"Module imported successfully: module_path={module_path}")
    except ImportError as e:
        logger.error(f"Failed to import module module_path={module_path}: {e}")
        return None

    logger.debug(f"Looking for class class_name={class_name} in module module_path={module_path}")
    try:
        cls = getattr(module, class_name)
        logger.debug(f"Class found: class_name={class_name} in module_path={module_path}")
    except AttributeError:
        logger.error(f"Class not found: class_name={class_name} in module_path={module_path}")
        return None

    try:
        instance = cls()
        logger.debug(f"Instance created successfully: class_name={class_name}")
    except Exception as e:
        logger.error(f"Failed to instantiate class class_name={class_name}: {e}")
        return None

    return instance
