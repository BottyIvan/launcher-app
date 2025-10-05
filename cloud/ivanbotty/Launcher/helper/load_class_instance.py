import importlib

def load_class_instance(path: str):
    """
    Dynamically imports a class from a full path and returns an instance.

    path: full class path as a string, e.g.
          "cloud.ivanbotty.Launcher.handlers.math_handler.MathHandler"
    """
    module_path, class_name = path.rsplit(".", 1)
    try:
        module = importlib.import_module(module_path)
        print(f"Module '{module_path}' imported successfully.")
    except ImportError as e:
        print(f"Failed to import module '{module_path}': {e}")
        return None

    print(f"Looking for class '{class_name}' in module '{module_path}'.")
    try:
        cls = getattr(module, class_name)
        print(f"Class '{class_name}' found in module '{module_path}'.")
    except AttributeError:
        print(f"Class '{class_name}' not found in module '{module_path}'.")
        return None

    try:
        instance = cls()
        print(f"Instance of '{class_name}' created successfully.")
    except Exception as e:
        print(f"Failed to instantiate class '{class_name}': {e}")
        return None

    return instance
