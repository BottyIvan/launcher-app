# API Reference

Comprehensive API documentation for Launcher modules and classes.

## Table of Contents

- [Services API](#services-api)
- [Handlers API](#handlers-api)
- [Models API](#models-api)
- [Database API](#database-api)
- [Helper Utilities API](#helper-utilities-api)
- [Widget API](#widget-api)

## Services API

### ApplicationsService

Located: `cloud.ivanbotty.Launcher.services.applications_service`

Manages application discovery, search, and launching.

#### Class Definition

```python
class ApplicationsService:
    """Service for managing desktop applications."""
    
    def __init__(self, database: Database):
        """
        Initialize the applications service.
        
        Args:
            database: Database instance for caching
        """
```

#### Methods

##### discover_applications()

```python
def discover_applications(self) -> List[Application]:
    """
    Discover all installed applications from desktop files.
    
    Scans standard application directories:
    - /usr/share/applications
    - /usr/local/share/applications
    - ~/.local/share/applications
    
    Returns:
        List[Application]: List of discovered applications
    
    Raises:
        IOError: If application directories cannot be accessed
    """
```

##### search()

```python
def search(self, query: str, limit: int = 50) -> List[Application]:
    """
    Search for applications matching the query.
    
    Performs case-insensitive search with fuzzy matching support.
    Results are ranked by relevance.
    
    Args:
        query: Search query string
        limit: Maximum number of results (default: 50)
    
    Returns:
        List[Application]: Matching applications, sorted by relevance
    
    Example:
        >>> service.search("fire")
        [Application(name="Firefox", ...), ...]
    """
```

##### get_application()

```python
def get_application(self, desktop_id: str) -> Optional[Application]:
    """
    Get a specific application by its desktop ID.
    
    Args:
        desktop_id: Desktop file ID (e.g., "firefox.desktop")
    
    Returns:
        Optional[Application]: Application if found, None otherwise
    """
```

##### launch_application()

```python
def launch_application(self, app: Application) -> bool:
    """
    Launch an application.
    
    Args:
        app: Application instance to launch
    
    Returns:
        bool: True if launched successfully, False otherwise
    
    Raises:
        RuntimeError: If application cannot be launched
    """
```

##### get_icon_path()

```python
def get_icon_path(self, icon_name: str, size: int = 64) -> Optional[str]:
    """
    Resolve icon path from icon name.
    
    Args:
        icon_name: Icon name or path
        size: Desired icon size in pixels (default: 64)
    
    Returns:
        Optional[str]: Full path to icon file, or None if not found
    """
```

---

### ExtensionsService

Located: `cloud.ivanbotty.Launcher.services.extensions_service`

Manages extension loading, enabling/disabling, and registration.

#### Class Definition

```python
class ExtensionsService:
    """Service for managing extensions."""
    
    def __init__(self, config_path: str):
        """
        Initialize the extensions service.
        
        Args:
            config_path: Path to extensions.yaml configuration file
        """
```

#### Methods

##### load_extensions()

```python
def load_extensions(self) -> List[Extension]:
    """
    Load all extension definitions from configuration.
    
    Parses extensions.yaml and creates Extension objects.
    Does not instantiate handler/service classes yet.
    
    Returns:
        List[Extension]: All defined extensions
    
    Raises:
        yaml.YAMLError: If configuration file is invalid
        FileNotFoundError: If configuration file doesn't exist
    """
```

##### enable_extension()

```python
def enable_extension(self, extension_id: str) -> None:
    """
    Enable an extension.
    
    Loads and registers the extension's handler and service.
    Updates extension state in database.
    
    Args:
        extension_id: Unique extension identifier
    
    Raises:
        ValueError: If extension doesn't exist
        ImportError: If extension classes cannot be loaded
    """
```

##### disable_extension()

```python
def disable_extension(self, extension_id: str) -> None:
    """
    Disable an extension.
    
    Unregisters handler and service, updates state.
    
    Args:
        extension_id: Unique extension identifier
    
    Raises:
        ValueError: If extension doesn't exist
    """
```

##### get_enabled_extensions()

```python
def get_enabled_extensions(self) -> List[Extension]:
    """
    Get all currently enabled extensions.
    
    Returns:
        List[Extension]: Enabled extensions, sorted by priority
    """
```

##### register_service()

```python
def register_service(self, service_name: str, service_instance: Any) -> None:
    """
    Register a custom service for an extension.
    
    Args:
        service_name: Unique service name
        service_instance: Service instance
    
    Raises:
        ValueError: If service name already registered
    """
```

---

### MathService

Located: `cloud.ivanbotty.Launcher.services.math_service`

Evaluates mathematical expressions safely.

#### Class Definition

```python
class MathService:
    """Service for mathematical expression evaluation."""
    
    def __init__(self):
        """Initialize the math service with safe evaluation context."""
```

#### Methods

##### calculate()

```python
def calculate(self, expression: str) -> float:
    """
    Evaluate a mathematical expression.
    
    Supports:
    - Basic operators: +, -, *, /, **, %
    - Functions: sqrt, sin, cos, tan, log, abs, etc.
    - Constants: pi, e
    - Parentheses for grouping
    
    Args:
        expression: Mathematical expression as string
    
    Returns:
        float: Result of evaluation
    
    Raises:
        ValueError: If expression is invalid
        ZeroDivisionError: If division by zero
    
    Example:
        >>> service.calculate("2 + 2")
        4.0
        >>> service.calculate("sqrt(16)")
        4.0
    """
```

##### format_result()

```python
def format_result(self, value: float, decimal_places: int = 2) -> str:
    """
    Format a numeric result for display.
    
    Args:
        value: Numeric value to format
        decimal_places: Number of decimal places (default: 2)
    
    Returns:
        str: Formatted string representation
    
    Example:
        >>> service.format_result(3.14159, 2)
        "3.14"
    """
```

---

## Handlers API

### BaseInputHandler

Located: `cloud.ivanbotty.Launcher.handlers.base_input_handler`

Abstract base class for all input handlers.

#### Class Definition

```python
class BaseInputHandler(ABC):
    """Abstract base class for input handlers."""
    
    @abstractmethod
    def can_handle(self, input_text: str) -> bool:
        """
        Check if this handler can process the input.
        
        Args:
            input_text: User input string
        
        Returns:
            bool: True if handler can process, False otherwise
        """
        pass
    
    @abstractmethod
    def handle(self, input_text: str) -> List[Result]:
        """
        Process the input and return results.
        
        Args:
            input_text: User input string
        
        Returns:
            List[Result]: List of results from processing
        
        Raises:
            Exception: If processing fails
        """
        pass
    
    @abstractmethod
    def get_priority(self) -> int:
        """
        Get handler priority (lower = higher priority).
        
        Returns:
            int: Priority value
        """
        pass
```

---

### ApplicationsHandler

Located: `cloud.ivanbotty.Launcher.handlers.applications_handler`

Handles application search queries.

#### Class Definition

```python
class ApplicationsHandler(BaseInputHandler):
    """Handler for application search queries."""
    
    def __init__(self, service: ApplicationsService):
        """
        Initialize the applications handler.
        
        Args:
            service: ApplicationsService instance
        """
```

#### Methods

```python
def can_handle(self, input_text: str) -> bool:
    """
    Always returns True - handles all non-special input.
    
    Args:
        input_text: User input
    
    Returns:
        bool: True (default handler)
    """

def handle(self, input_text: str) -> List[Result]:
    """
    Search for applications matching input.
    
    Args:
        input_text: Search query
    
    Returns:
        List[Result]: Matching applications as results
    """

def get_priority(self) -> int:
    """Returns: int: Priority (default: 100)"""
```

---

### MathHandler

Located: `cloud.ivanbotty.Launcher.handlers.math_handler`

Handles mathematical expression evaluation.

#### Methods

```python
def can_handle(self, input_text: str) -> bool:
    """
    Check if input is a mathematical expression.
    
    Detects:
    - Numbers and operators
    - Mathematical functions
    - Parentheses
    
    Args:
        input_text: User input
    
    Returns:
        bool: True if input appears to be math expression
    """

def handle(self, input_text: str) -> List[Result]:
    """
    Evaluate mathematical expression.
    
    Args:
        input_text: Math expression
    
    Returns:
        List[Result]: Single result with calculation outcome
    """

def get_priority(self) -> int:
    """Returns: int: Priority (50 - higher than app search)"""
```

---

## Models API

### Application

Located: `cloud.ivanbotty.Launcher.models.applications_model`

Represents a desktop application.

#### Class Definition

```python
@dataclass
class Application:
    """Data model for a desktop application."""
    
    desktop_id: str          # Unique desktop file ID
    name: str                # Application name
    description: str         # Application description
    icon: str                # Icon name or path
    exec: str                # Executable command
    categories: List[str]    # Application categories
    keywords: List[str]      # Search keywords
    terminal: bool           # Whether app runs in terminal
    no_display: bool         # Whether to hide from menus
    
    def __str__(self) -> str:
        """String representation."""
        return f"{self.name} ({self.desktop_id})"
```

---

### Extension

Located: `cloud.ivanbotty.Launcher.models.extension_model`

Represents an extension definition.

#### Class Definition

```python
@dataclass
class Extension:
    """Data model for an extension."""
    
    id: str                  # Unique extension ID
    name: str                # Display name
    description: str         # Extension description
    enabled: bool            # Whether extension is enabled
    priority: int            # Loading priority
    handler: str             # Handler class path
    service: str             # Service class path
    icon: str                # Icon name
    settings: Dict[str, Any] # Extension settings
    
    def __str__(self) -> str:
        """String representation."""
        return f"{self.name} ({'enabled' if self.enabled else 'disabled'})"
```

---

## Database API

### Database

Located: `cloud.ivanbotty.database.sqlite3`

SQLite database wrapper with type hints.

#### Class Definition

```python
class Database:
    """Type-safe SQLite database wrapper."""
    
    def __init__(self, db_path: str):
        """
        Initialize database connection.
        
        Args:
            db_path: Path to SQLite database file
        
        Raises:
            sqlite3.Error: If database cannot be opened
        """
```

#### Methods

##### execute()

```python
def execute(self, query: str, params: Tuple = ()) -> sqlite3.Cursor:
    """
    Execute a SQL query.
    
    Args:
        query: SQL query string
        params: Query parameters (for parameterized queries)
    
    Returns:
        sqlite3.Cursor: Cursor for result iteration
    
    Raises:
        sqlite3.Error: If query execution fails
    
    Example:
        >>> db.execute("SELECT * FROM apps WHERE name = ?", ("Firefox",))
    """
```

##### get_preference()

```python
def get_preference(self, key: str, default: Any = None) -> Any:
    """
    Get a user preference value.
    
    Args:
        key: Preference key
        default: Default value if key doesn't exist
    
    Returns:
        Any: Preference value, or default if not found
    
    Example:
        >>> db.get_preference("window.width", 800)
        600  # stored value
    """
```

##### set_preference()

```python
def set_preference(self, key: str, value: Any) -> None:
    """
    Save a user preference value.
    
    Automatically determines type and serializes complex values.
    
    Args:
        key: Preference key
        value: Value to store (str, int, bool, dict, list)
    
    Raises:
        TypeError: If value type is not supported
    
    Example:
        >>> db.set_preference("window.width", 800)
        >>> db.set_preference("recent_searches", ["firefox", "chrome"])
    """
```

##### commit()

```python
def commit(self) -> None:
    """
    Commit pending transactions.
    
    Raises:
        sqlite3.Error: If commit fails
    """
```

##### close()

```python
def close(self) -> None:
    """
    Close database connection.
    
    Should be called when database is no longer needed.
    """
```

---

## Helper Utilities API

### DynamicLoader

Located: `cloud.ivanbotty.Launcher.helper.dynamic_loader`

Dynamically loads classes at runtime.

#### Functions

##### load_class_instance()

```python
def load_class_instance(
    module_path: str,
    class_name: str,
    *args,
    **kwargs
) -> Any:
    """
    Dynamically load and instantiate a class.
    
    Uses caching to avoid repeated imports of same class.
    
    Args:
        module_path: Full module path (e.g., "cloud.ivanbotty.Launcher.services.math_service")
        class_name: Class name (e.g., "MathService")
        *args: Positional arguments for class constructor
        **kwargs: Keyword arguments for class constructor
    
    Returns:
        Any: Instance of the loaded class
    
    Raises:
        ImportError: If module cannot be imported
        AttributeError: If class doesn't exist in module
    
    Example:
        >>> instance = load_class_instance(
        ...     "cloud.ivanbotty.Launcher.services.math_service",
        ...     "MathService"
        ... )
    """
```

---

### Parser

Located: `cloud.ivanbotty.Launcher.helper.parser`

Parses and categorizes user input.

#### Class Definition

```python
class Parser:
    """Parse and categorize user input."""
    
    def parse(self, input_text: str) -> InputType:
        """
        Determine the type of user input.
        
        Args:
            input_text: User input string
        
        Returns:
            InputType: Enum indicating input type
                (APP_SEARCH, MATH, COMMAND, AI, LINK, etc.)
        
        Example:
            >>> parser.parse("2 + 2")
            InputType.MATH
            >>> parser.parse("firefox")
            InputType.APP_SEARCH
        """
```

---

### ThreadManager

Located: `cloud.ivanbotty.Launcher.helper.thread_manager`

Manages background thread execution.

#### Class Definition

```python
class ThreadManager:
    """Manage background thread execution."""
    
    def __init__(self, pool_size: int = 4):
        """
        Initialize thread manager.
        
        Args:
            pool_size: Number of worker threads in pool
        """
```

#### Methods

##### run_in_thread()

```python
def run_in_thread(
    self,
    func: Callable,
    callback: Optional[Callable] = None,
    *args,
    **kwargs
) -> None:
    """
    Execute function in background thread.
    
    Args:
        func: Function to execute
        callback: Optional callback for result (called in main thread)
        *args: Arguments for func
        **kwargs: Keyword arguments for func
    
    Example:
        >>> def heavy_task(x):
        ...     return x * 2
        >>> def on_complete(result):
        ...     print(f"Result: {result}")
        >>> thread_manager.run_in_thread(heavy_task, on_complete, 21)
    """
```

---

## Widget API

### MainWindow

Located: `cloud.ivanbotty.Launcher.widget.window`

Main application window.

#### Class Definition

```python
class MainWindow(Adw.ApplicationWindow):
    """Main application window."""
    
    def __init__(self, application: Gtk.Application):
        """
        Initialize main window.
        
        Args:
            application: GTK Application instance
        """
```

#### Signals

- `"close-request"`: Emitted when window is closing
- `"show"`: Emitted when window is shown
- `"hide"`: Emitted when window is hidden

---

### SearchEntry

Located: `cloud.ivanbotty.Launcher.widget.search_entry`

Search input widget.

#### Class Definition

```python
class SearchEntry(Gtk.SearchEntry):
    """Search entry widget."""
    
    def __init__(self):
        """Initialize search entry."""
```

#### Signals

- `"search-changed"`: Emitted when search text changes
- `"activate"`: Emitted when Enter is pressed
- `"stop-search"`: Emitted when Escape is pressed

---

## Type Definitions

Common type aliases used throughout the codebase:

```python
from typing import List, Dict, Optional, Callable, Any, Tuple

# Result type for handlers
Result = Any  # Typically Application or str

# Callback type
Callback = Callable[[Any], None]

# Settings dictionary
Settings = Dict[str, Any]

# Path type
Path = str
```

---

## Constants

Located: `cloud.ivanbotty.Launcher.config.constants`

Application-wide constants:

```python
# Application info
APP_ID = "cloud.ivanbotty.Launcher"
APP_NAME = "Launcher"
VERSION = "0.0.1"

# Paths
DATA_DIR = "~/.local/share/cloud.ivanbotty.Launcher"
CONFIG_DIR = "~/.config/cloud.ivanbotty.Launcher"
CACHE_DIR = "~/.cache/cloud.ivanbotty.Launcher"

# Search
MAX_RESULTS = 50
SEARCH_DELAY_MS = 0

# Icons
DEFAULT_ICON = "application-x-executable"
ICON_SIZE = 64
```

---

## Usage Examples

### Basic Service Usage

```python
from cloud.ivanbotty.Launcher.services.applications_service import ApplicationsService
from cloud.ivanbotty.database.sqlite3 import Database

# Initialize
db = Database("~/.local/share/cloud.ivanbotty.Launcher/launcher.db")
service = ApplicationsService(db)

# Search for apps
results = service.search("firefox")
for app in results:
    print(f"{app.name}: {app.description}")

# Launch an app
if results:
    service.launch_application(results[0])
```

### Extension Development

```python
from cloud.ivanbotty.Launcher.handlers.base_input_handler import BaseInputHandler

class CustomHandler(BaseInputHandler):
    def can_handle(self, input_text: str) -> bool:
        return input_text.startswith("custom:")
    
    def handle(self, input_text: str) -> List[Result]:
        # Process input
        processed = input_text.replace("custom:", "").strip()
        return [f"Processed: {processed}"]
    
    def get_priority(self) -> int:
        return 10  # High priority
```

---

For more information:
- [Architecture](Architecture.md) - System design details
- [Contributing](Contributing.md) - Development guidelines
- [Features](Features.md) - Available functionality
