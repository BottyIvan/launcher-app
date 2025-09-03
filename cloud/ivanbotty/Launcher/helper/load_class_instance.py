import importlib

def load_class_instance(path: str):
    """
    Dynamically imports a class from a full path and returns an instance.

    path: full class path as a string, e.g.
          "cloud.ivanbotty.Launcher.handlers.math_handler.MathHandler"
    """
    module_path, class_name = path.rsplit(".", 1)      # split module and class
    try:
        module = importlib.import_module(module_path)  # import the module
    except ImportError as e:
        print(f"Error importing {module_path}: {e}")
        return None
    cls = getattr(module, class_name)                  # get the class
    instance = cls()                                   # create the instance
    return instance
