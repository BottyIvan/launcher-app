# Features

Explore the comprehensive feature set of Launcher.

## Table of Contents

- [Core Features](#core-features)
- [User Interface](#user-interface)
- [Search Capabilities](#search-capabilities)
- [Extension System](#extension-system)
- [Built-in Services](#built-in-services)
- [Performance Features](#performance-features)
- [Integration Features](#integration-features)
- [Upcoming Features](#upcoming-features)

## Core Features

### Modern GTK4 Interface

- **Native Linux Experience**: Built with GTK4 for seamless integration
- **Adwaita Design**: Follows GNOME design guidelines
- **Responsive UI**: Smooth animations and transitions
- **HiDPI Support**: Crisp rendering on high-resolution displays
- **Dark Mode**: Automatic theme switching based on system preferences

### Instant Search

- **Real-time Results**: See results as you type
- **Fuzzy Matching**: Find apps even with typos
- **Smart Ranking**: Most relevant results first
- **Case Insensitive**: No need to worry about capitalization
- **Fast Performance**: Optimized database queries

### Flatpak Support

- **Sandboxed Environment**: Run safely with limited permissions
- **All Dependencies Included**: No manual dependency management
- **Easy Updates**: Simple update process
- **Portable**: Works across different Linux distributions
- **Secure**: Controlled filesystem and network access

## User Interface

### Dual View Modes

**Compact Mode:**
- Grid layout with application icons
- Minimal design for quick access
- Icon-focused presentation
- Perfect for fast launches

**Extended Mode:**
- List view with detailed information
- Application descriptions
- Additional metadata
- Better for browsing

### Visual Design

- **SVG Icons**: Scalable vector graphics for any size
- **Custom Icons**: Support for custom application icons
- **Consistent Theming**: Adapts to system theme
- **Smooth Animations**: Polished user experience
- **Accessibility**: Screen reader support

### Window Management

- **Keyboard-first Design**: Optimized for keyboard users
- **Mouse Support**: Full mouse interaction available
- **Quick Dismiss**: Press Esc to close instantly
- **Position Memory**: Remembers window position
- **Size Adaptation**: Responsive to window resizing

## Search Capabilities

### Application Discovery

- **Desktop File Scanning**: Automatically finds installed applications
- **Multiple Sources**: Scans system and user application directories
- **Live Updates**: Detects newly installed applications
- **Icon Resolution**: Finds and displays appropriate icons
- **Metadata Parsing**: Extracts name, description, categories

### Search Algorithms

- **Instant Search**: Results appear as you type (no delay)
- **Prefix Matching**: Prioritizes matches at word start
- **Substring Matching**: Finds matches anywhere in name
- **Intelligent Ranking**: Most relevant results first
- **Performance Optimized**: Sub-millisecond search times

### Filter Options

- **By Name**: Search application names
- **By Category**: Filter by application category
- **By Keywords**: Match desktop file keywords
- **By Description**: Search in app descriptions (extended mode)

## Extension System

### Architecture

- **YAML Configuration**: Extensions defined in YAML files
- **Plug-and-Play**: Easy to add and remove
- **Service Registration**: Extensions can register custom services
- **Dynamic Loading**: Load extensions on demand
- **Isolated Execution**: Extensions run independently

### Extension Management

- **Enable/Disable**: Toggle extensions without restart
- **Search Extensions**: Find extensions by name
- **Extension List**: View all available extensions
- **Extension Info**: See details about each extension
- **Configuration**: Per-extension settings

### Available Extensions

#### 1. Application Search (Default)
- Search for installed desktop applications
- Access to all `.desktop` files
- Icon resolution and display
- Instant launch capability

#### 2. Math Calculator
- Evaluate mathematical expressions
- Support for common functions
- Constants (pi, e)
- Real-time calculation

#### 3. Command Runner (In Development)
- Execute shell commands
- Command history
- Output display
- Security controls

#### 4. AI Assistant (In Development)
- Natural language queries
- Google Gemini integration
- Context-aware responses
- API key configuration required

#### 5. File Manager (In Development)
- Browse file system
- Quick file search
- Recent files
- File actions (open, copy path)

#### 6. Link Management (In Development)
- Web bookmark management
- Quick link access
- Link organization
- URL search

## Built-in Services

### ApplicationsService

**Responsibilities:**
- Discover installed applications from `.desktop` files
- Parse desktop entry specifications
- Maintain application database
- Provide search functionality
- Handle icon resolution

**Features:**
- Instant search across all applications
- Dynamic, ordered list via `Gio.ListStore`
- Caching for improved performance
- Automatic refresh on application changes

### ExtensionService

**Responsibilities:**
- Manage extension lifecycle
- Load/unload extensions dynamically
- Track enabled/disabled state
- Register extension services
- Provide extension search

**Features:**
- Add, remove, enable, disable extensions
- Search and list extensions by name
- Service registration for custom extensions
- YAML-based configuration

### MathService

**Responsibilities:**
- Evaluate mathematical expressions
- Provide calculator functionality
- Support mathematical functions
- Safe expression evaluation

**Features:**
- Basic arithmetic: `+`, `-`, `*`, `/`, `**`
- Functions: `sqrt`, `sin`, `cos`, `tan`, `log`, `abs`
- Constants: `pi`, `e`
- Safe evaluation (no code execution)
- Error handling

### CommandService (In Development)

**Responsibilities:**
- Execute shell commands
- Manage command history
- Provide command output
- Security and permission control

**Planned Features:**
- Command execution with output
- Command history and suggestions
- Environment variable support
- Permission-based execution

### AIService (In Development)

**Responsibilities:**
- Integration with AI APIs
- Natural language query processing
- Context management
- Response formatting

**Planned Features:**
- Google Gemini API integration
- Conversation history
- Context-aware responses
- Customizable prompts

## Performance Features

### Caching

- **Desktop Entry Caching**: Avoid repeated file parsing
- **Icon Caching**: Store resolved icon paths
- **Database Connection Pooling**: Reuse connections
- **Class Instance Caching**: Avoid redundant instantiation
- **Regex Precompilation**: Compile patterns once

### Optimization

- **Lazy Loading**: Load resources on demand
- **Background Processing**: Non-blocking UI operations
- **Efficient Queries**: Optimized SQLite queries
- **Memory Management**: Careful resource cleanup
- **Thread Management**: Background thread pool

### Benchmarks

Typical performance metrics:
- **Startup Time**: < 1 second (cold start)
- **Search Latency**: < 50ms for instant results
- **Memory Usage**: ~30-50MB resident
- **Database Queries**: < 1ms for most operations

## Integration Features

### Desktop Integration

- **Desktop Files**: Standard `.desktop` entry support
- **Icon Themes**: Respects system icon themes
- **D-Bus Integration**: System bus communication
- **Portal Support**: XDG Desktop Portal integration
- **Application Launching**: Proper process spawning

### System Integration

- **Wayland Support**: Native Wayland compositor support
- **X11 Fallback**: Works on X11 when Wayland unavailable
- **Multi-monitor**: Proper handling of multiple displays
- **HiDPI Aware**: Scales correctly on high-DPI displays
- **Keyboard Layouts**: Respects system keyboard settings

### Platform Support

- **GNOME**: First-class support and integration
- **KDE Plasma**: Functional with Plasma desktop
- **XFCE**: Compatible with XFCE environment
- **Other DEs**: Works on most modern Linux desktops
- **Distribution Agnostic**: No distro-specific code

## Data Management

### Persistent Storage

- **SQLite Database**: Local data storage
- **User Preferences**: Saved settings and configurations
- **Extension State**: Enabled/disabled state
- **Search History**: Recent searches (if enabled)
- **Window State**: Position and size

### Configuration

- **YAML Files**: Extension and resource configuration
- **GSettings Support**: Desktop environment integration
- **Environment Variables**: Override default settings
- **Command-line Options**: Launch-time configuration

## Development Features

### Code Quality

- **Type Annotations**: Full type hints for IDE support
- **Docstrings**: Comprehensive documentation
- **Testing**: Unit test suite included
- **Linting**: Flake8 configuration provided
- **Formatting**: Black code style

### Architecture

- **MVC Pattern**: Clear separation of concerns
- **Service Layer**: Business logic abstraction
- **Handler Pattern**: Extensible input handling
- **Widget Components**: Reusable UI elements
- **Helper Utilities**: Common functionality

## Upcoming Features

Features currently in development:

### Short-term (Next Release)

- ⏳ **Command Service**: Full command execution capability
- ⏳ **AI Integration**: Complete Gemini API integration
- ⏳ **File Search**: File system search and navigation
- ⏳ **Link Manager**: Web bookmark management
- ⏳ **Keyboard Customization**: Custom keyboard shortcut configuration

### Mid-term (Future Releases)

- 🔮 **Plugin System**: Third-party plugin support
- 🔮 **Web Search**: Search engines integration
- 🔮 **Calculator History**: Math calculation history
- 🔮 **Clipboard Manager**: Clipboard history integration
- 🔮 **Window Manager**: Quick window switching

### Long-term (Roadmap)

- 🎯 **Cloud Sync**: Sync settings across devices
- 🎯 **Mobile Companion**: Mobile app integration
- 🎯 **Workflow Automation**: Custom automation scripts
- 🎯 **AI Learning**: Personalized suggestions
- 🎯 **Multi-language**: Localization support

## Feature Comparison

### vs. GNOME Shell Search
- ✅ Faster startup
- ✅ More customizable
- ✅ Extension system
- ✅ Standalone application
- ➖ Less integrated with system

### vs. Rofi/dmenu
- ✅ Modern GTK4 interface
- ✅ Mouse support
- ✅ Better visuals
- ✅ Extension system
- ➖ Higher resource usage

### vs. Albert/Ulauncher
- ✅ Native GTK4 (no Qt)
- ✅ Flatpak support
- ✅ Type-safe codebase
- ✅ Modern design
- ➖ Fewer extensions (currently)

## Accessibility Features

- **Keyboard Navigation**: Full keyboard control
- **Screen Reader**: Compatible with screen readers
- **High Contrast**: Support for high contrast themes
- **Large Text**: Scales with system font settings
- **Focus Indicators**: Clear keyboard focus indication

## Security Features

- **Sandboxing**: Flatpak provides isolated environment
- **Limited Permissions**: Minimal required permissions
- **Safe Evaluation**: Math expressions evaluated safely
- **No Code Execution**: User input not executed as code
- **Read-only Access**: Limited filesystem access

For detailed usage of these features, see the [Usage Guide](Usage-Guide.md).

For technical implementation details, see the [Architecture](Architecture.md) documentation.
