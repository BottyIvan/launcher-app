# Architecture

Understand the design, structure, and technical implementation of Launcher.

## Table of Contents

- [Architecture Overview](#architecture-overview)
- [Design Principles](#design-principles)
- [Project Structure](#project-structure)
- [Core Components](#core-components)
- [Data Flow](#data-flow)
- [Technology Stack](#technology-stack)
- [Design Patterns](#design-patterns)
- [Module Dependencies](#module-dependencies)

## Architecture Overview

Launcher follows a modular, layered architecture that separates concerns and promotes maintainability:

```
┌─────────────────────────────────────────┐
│          User Interface Layer           │
│         (GTK4/Adwaita Widgets)         │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│          Controller Layer               │
│     (Event Handlers & Controllers)      │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│           Handler Layer                 │
│      (Input & Command Handlers)         │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│          Service Layer                  │
│   (Business Logic & Data Processing)    │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│           Data Layer                    │
│     (Database & File System Access)     │
└─────────────────────────────────────────┘
```

## Design Principles

### 1. Separation of Concerns
- **UI Layer**: Only responsible for presentation
- **Controller Layer**: Handles user interactions
- **Service Layer**: Contains business logic
- **Data Layer**: Manages persistence

### 2. Modularity
- Independent, reusable components
- Clear interfaces between modules
- Pluggable architecture for extensions

### 3. Type Safety
- Comprehensive type hints throughout
- Static type checking with MyPy
- Better IDE support and autocomplete

### 4. Performance First
- Lazy loading of resources
- Caching strategies at multiple levels
- Background processing for heavy operations
- Optimized database queries

### 5. Extensibility
- Plugin/extension system
- Service registration pattern
- Dynamic class loading
- YAML-based configuration

## Project Structure

```
launcher-app/
├── cloud/
│   └── ivanbotty/
│       ├── database/              # Data persistence
│       │   ├── sqlite3.py         # SQLite wrapper with type hints
│       │   └── __init__.py
│       │
│       ├── utils/                 # Shared utilities
│       │   ├── app_init.py        # Application initialization
│       │   └── __init__.py
│       │
│       ├── Launcher/              # Main application
│       │   ├── app.py             # Application class
│       │   ├── __main__.py        # Entry point
│       │   │
│       │   ├── config/            # Configuration constants
│       │   │   └── constants.py   # App-wide constants
│       │   │
│       │   ├── controller/        # Event controllers
│       │   │   ├── search_controller.py
│       │   │   ├── key_controller.py
│       │   │   └── click_controller.py
│       │   │
│       │   ├── handlers/          # Input handlers
│       │   │   ├── base_input_handler.py
│       │   │   ├── applications_handler.py
│       │   │   ├── math_handler.py
│       │   │   ├── command_handler.py
│       │   │   ├── ai_handler.py
│       │   │   ├── link_handler.py
│       │   │   └── extensions_handler.py
│       │   │
│       │   ├── helper/            # Helper utilities
│       │   │   ├── parser.py      # Input parsing
│       │   │   ├── thread_manager.py
│       │   │   └── dynamic_loader.py
│       │   │
│       │   ├── models/            # Data models
│       │   │   ├── applications_model.py
│       │   │   └── extension_model.py
│       │   │
│       │   ├── services/          # Business logic
│       │   │   ├── applications_service.py
│       │   │   ├── extensions_service.py
│       │   │   ├── math_service.py
│       │   │   ├── command_service.py
│       │   │   └── ai_service.py
│       │   │
│       │   ├── widget/            # UI components
│       │   │   ├── window.py      # Main window
│       │   │   ├── search_entry.py
│       │   │   ├── row.py         # Application row
│       │   │   ├── preferences.py
│       │   │   ├── progress_bar.py
│       │   │   └── footer.py
│       │   │
│       │   └── resources/         # Assets & configs
│       │       ├── *.svg          # Icon files
│       │       ├── appdata.xml    # AppStream metadata
│       │       ├── extensions.yaml
│       │       └── wizard.yaml
│       │
│       └── Wizard/                # Welcome wizard
│           ├── app.py
│           ├── __main__.py
│           └── components/
│
├── tests/                         # Test suite
│   ├── test_utils.py
│   ├── test_helpers.py
│   └── test_performance.py
│
├── manifest.yaml                  # Flatpak manifest
├── meson.build                    # Meson build config
├── pyproject.toml                 # Python project config
├── LICENSE                        # GPL-3.0-or-later
├── README.md                      # Project readme
└── CONTRIBUTING                   # Contribution guidelines
```

## Core Components

### 1. Application Layer

#### App (`app.py`)
The main application class that:
- Initializes GTK application
- Sets up UI components
- Manages application lifecycle
- Handles signals and events

```python
class LauncherApp(Adw.Application):
    def __init__(self):
        super().__init__(application_id="cloud.ivanbotty.Launcher")
        # Initialize services, UI, etc.
```

#### Main Window (`widget/window.py`)
The primary UI container:
- Creates and manages UI layout
- Handles window events
- Coordinates between widgets

### 2. Service Layer

#### ApplicationsService
**Purpose**: Manage application discovery and search

**Responsibilities**:
- Scan desktop files from standard locations
- Parse `.desktop` entries
- Maintain application database
- Provide search functionality
- Resolve application icons

**Key Methods**:
```python
def discover_applications(self) -> List[Application]
def search(self, query: str) -> List[Application]
def get_application(self, desktop_id: str) -> Optional[Application]
def launch_application(self, app: Application) -> None
```

#### ExtensionsService
**Purpose**: Manage extension lifecycle

**Responsibilities**:
- Load extension definitions from YAML
- Enable/disable extensions
- Track extension state
- Register extension services

**Key Methods**:
```python
def load_extensions(self) -> List[Extension]
def enable_extension(self, extension_id: str) -> None
def disable_extension(self, extension_id: str) -> None
def get_enabled_extensions(self) -> List[Extension]
```

#### MathService
**Purpose**: Evaluate mathematical expressions

**Responsibilities**:
- Parse math expressions
- Safely evaluate calculations
- Support functions and constants
- Format results

**Key Methods**:
```python
def calculate(self, expression: str) -> float
def format_result(self, value: float) -> str
```

### 3. Handler Layer

#### Base Input Handler
Abstract base class for all input handlers:

```python
class BaseInputHandler(ABC):
    @abstractmethod
    def can_handle(self, input_text: str) -> bool:
        """Check if this handler can process the input."""
        pass
    
    @abstractmethod
    def handle(self, input_text: str) -> List[Result]:
        """Process input and return results."""
        pass
```

#### Handler Implementations
- **ApplicationsHandler**: Handles app search queries
- **MathHandler**: Processes mathematical expressions
- **CommandHandler**: Executes shell commands
- **AIHandler**: Processes AI queries
- **LinkHandler**: Manages web links

### 4. Controller Layer

#### SearchController
Manages search input and coordination:
- Receives user input
- Routes to appropriate handlers
- Aggregates results
- Updates UI

#### KeyController
Handles keyboard interactions:
- Navigation (up/down arrows)
- Selection (Enter)
- Shortcuts (Ctrl+...)

#### ClickController
Manages mouse interactions:
- Click events
- Hover effects
- Context menus

### 5. Data Layer

#### Database (`database/sqlite3.py`)
SQLite database wrapper with type hints:

```python
class Database:
    def __init__(self, db_path: str):
        self.connection: sqlite3.Connection = ...
    
    def execute(self, query: str, params: tuple = ()) -> sqlite3.Cursor:
        """Execute a query with parameters."""
        pass
    
    def get_preference(self, key: str, default: Any = None) -> Any:
        """Get a user preference."""
        pass
    
    def set_preference(self, key: str, value: Any) -> None:
        """Save a user preference."""
        pass
```

#### Models
Data classes representing domain entities:

```python
@dataclass
class Application:
    desktop_id: str
    name: str
    description: str
    icon: str
    exec: str
    categories: List[str]

@dataclass
class Extension:
    id: str
    name: str
    enabled: bool
    handler: str
    service: str
```

## Data Flow

### Search Flow

```
User Input
    ↓
SearchEntry Widget
    ↓
SearchController
    ↓
Parser (determine input type)
    ↓
Router (select appropriate handler)
    ↓
Handler (ApplicationsHandler, MathHandler, etc.)
    ↓
Service (ApplicationsService, MathService, etc.)
    ↓
Data Layer (Database, File System)
    ↓
Results aggregated
    ↓
UI Update (display results)
```

### Launch Flow

```
User Selection (click or Enter)
    ↓
ClickController / KeyController
    ↓
Application Model
    ↓
ApplicationsService.launch_application()
    ↓
Gio.AppInfo.launch()
    ↓
Application Started
```

### Extension Loading Flow

```
Application Startup
    ↓
ExtensionsService.load_extensions()
    ↓
Read extensions.yaml
    ↓
Parse extension definitions
    ↓
For each enabled extension:
    ↓
    DynamicLoader.load_class_instance()
    ↓
    Register handler and service
    ↓
    Cache instance
    ↓
Extensions Ready
```

## Technology Stack

### Core Technologies

#### Python 3.11+
- Modern Python features
- Type hints and annotations
- Async/await support

#### GTK4
- Modern UI toolkit
- Hardware-accelerated rendering
- Native Linux integration
- Wayland and X11 support

#### Adwaita
- GNOME design language
- Adaptive layouts
- Dark mode support
- Modern widgets

#### PyGObject
- Python bindings for GTK
- GObject introspection
- Full GTK4 access

### Data & Storage

#### SQLite3
- Embedded database
- User preferences storage
- Application cache
- Extension state

#### YAML
- Configuration files
- Extension definitions
- Resource manifests

### Build & Distribution

#### Meson
- Build system
- Cross-platform support
- Fast incremental builds

#### Flatpak
- Sandboxed distribution
- Dependency management
- Cross-distro compatibility

### Development Tools

#### Black
- Code formatting
- Consistent style
- Line length: 100

#### Flake8
- Code linting
- Style checking
- Error detection

#### MyPy
- Static type checking
- Type hint validation

#### Unittest
- Unit testing framework
- Test discovery
- Assertions and mocking

## Design Patterns

### 1. Service Pattern
Services encapsulate business logic:
```python
class ApplicationsService:
    def __init__(self):
        self._cache = {}
    
    def search(self, query: str) -> List[Application]:
        # Business logic here
        pass
```

### 2. Handler Pattern
Handlers process specific input types:
```python
class MathHandler(BaseInputHandler):
    def can_handle(self, input_text: str) -> bool:
        return self._is_math_expression(input_text)
    
    def handle(self, input_text: str) -> List[Result]:
        result = self.math_service.calculate(input_text)
        return [Result(str(result))]
```

### 3. Observer Pattern
GTK signals for event handling:
```python
search_entry.connect("changed", self._on_search_changed)
```

### 4. Factory Pattern
Dynamic class loading:
```python
def load_class_instance(module_path: str, class_name: str):
    module = importlib.import_module(module_path)
    class_obj = getattr(module, class_name)
    return class_obj()
```

### 5. Singleton Pattern
Single database connection:
```python
class Database:
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
```

### 6. Strategy Pattern
Pluggable handlers for different input types:
```python
handlers = [
    ApplicationsHandler(),
    MathHandler(),
    CommandHandler(),
]

for handler in handlers:
    if handler.can_handle(input_text):
        results = handler.handle(input_text)
        break
```

## Module Dependencies

### Dependency Graph

```
app.py
  ├── widget/window.py
  │   ├── widget/search_entry.py
  │   ├── widget/row.py
  │   └── widget/footer.py
  │
  ├── controller/search_controller.py
  │   ├── handler/applications_handler.py
  │   │   └── services/applications_service.py
  │   │       └── models/applications_model.py
  │   │
  │   ├── handler/math_handler.py
  │   │   └── services/math_service.py
  │   │
  │   └── helper/parser.py
  │
  ├── services/extensions_service.py
  │   ├── models/extension_model.py
  │   └── helper/dynamic_loader.py
  │
  └── database/sqlite3.py
```

### External Dependencies

```
PyGObject (gi)
  ├── Gtk 4.0
  ├── Adw 1.0
  ├── Gio 2.0
  └── GLib 2.0

google-generativeai
  └── (for AI features)

Python Standard Library
  ├── sqlite3
  ├── pathlib
  ├── typing
  ├── dataclasses
  ├── importlib
  └── logging
```

## Performance Considerations

### Caching Strategy

1. **Desktop File Cache**: Parsed `.desktop` files cached in memory
2. **Icon Cache**: Resolved icon paths stored
3. **Database Connection Pool**: Reuse database connections
4. **Class Instance Cache**: Loaded classes cached to avoid reimport

### Threading Model

- **Main Thread**: UI rendering and event handling
- **Background Threads**: Heavy operations (file scanning, database queries)
- **Thread Pool**: Configurable size for concurrent operations

### Memory Management

- Weak references for cached objects
- Explicit cleanup in destructors
- Limited cache sizes with LRU eviction

## Security Architecture

### Sandboxing (Flatpak)

- Limited filesystem access
- Network access controlled
- No direct system modification
- Portal-based file access

### Input Validation

- Math expressions: Safe evaluation without `eval()`
- Commands: Optional whitelist
- SQL: Parameterized queries (no injection)
- File paths: Sanitized and validated

## Extensibility

### Adding New Extensions

1. Create handler class extending `BaseInputHandler`
2. Create service class with business logic
3. Define extension in `extensions.yaml`
4. Extension automatically loaded and registered

### Custom Services

Extensions can register custom services:
```python
class CustomService:
    def __init__(self):
        pass
    
    def custom_operation(self):
        pass

# Register with extension service
extensions_service.register_service("custom", CustomService())
```

## Next Steps

- See [API Reference](API-Reference.md) for detailed API documentation
- Read [Contributing](Contributing.md) for development guidelines
- Check [Features](Features.md) for implemented functionality
