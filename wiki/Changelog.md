# Changelog

All notable changes to Launcher will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned Features
- Full command service implementation
- Complete AI integration with Gemini
- File manager extension
- Link management extension
- Plugin system for third-party extensions
- Web search integration
- Clipboard manager integration
- Window switcher functionality

## [0.0.1] - 2024-11-02

### Added

#### Core Features
- Modern GTK4/Adwaita user interface
- Flatpak support for sandboxed distribution
- Instant application search with fuzzy matching
- Dual view modes: compact grid and extended list
- SVG icon rendering with proper scaling
- Persistent user preferences with SQLite
- Comprehensive type annotations throughout codebase
- Professional test suite with unit and performance tests

#### Services
- **ApplicationsService**: Application discovery and search
  - Desktop file scanning from multiple locations
  - Intelligent search with case-insensitive matching
  - Icon resolution with theme support
  - Application launching with Gio.AppInfo
  - Database caching for improved performance

- **ExtensionService**: Extension management system
  - YAML-based extension definitions
  - Dynamic extension loading and unloading
  - Enable/disable extensions at runtime
  - Extension search and listing
  - Custom service registration

- **MathService**: Built-in calculator
  - Safe mathematical expression evaluation
  - Support for basic arithmetic operators
  - Common mathematical functions (sqrt, sin, cos, tan, log, abs)
  - Constants (pi, e)
  - Error handling and validation

- **CommandService**: Command execution framework (in development)
- **AIService**: AI assistant integration (in development)

#### Extensions
- Application search extension (enabled by default)
- Math calculator extension (enabled by default)
- Command runner extension (in development)
- AI assistant extension (in development)
- File manager extension (planned)
- Link management extension (planned)

#### User Interface
- **MainWindow**: Primary application window
  - Responsive layout
  - Keyboard-first design
  - Window state persistence
  - Dark mode support

- **SearchEntry**: Search input widget
  - Real-time search as you type
  - Instant results display
  - Keyboard navigation support

- **ApplicationRow**: Result display widget
  - Icon and text layout
  - Click and keyboard activation
  - Hover effects

- **Preferences**: Settings dialog
  - General settings configuration
  - Extension management
  - Keyboard shortcut customization

- **Wizard**: Welcome wizard for first-time setup

#### Development Features
- Comprehensive documentation
  - Installation guide
  - Usage guide
  - Architecture documentation
  - API reference
  - Contributing guidelines
  - FAQ and troubleshooting

- Code Quality Tools
  - Black formatting (line length: 100)
  - Flake8 linting configuration
  - Type checking support
  - Unit test framework

- Build System
  - Meson build configuration
  - Flatpak manifest for distribution
  - PyProject.toml for Python packaging

#### Database
- SQLite database for persistent storage
- User preferences table
- Extension state tracking
- Application cache (optional)
- Type-safe database wrapper with proper error handling

#### Helper Utilities
- **Parser**: Input type detection and parsing
- **ThreadManager**: Background thread execution
- **DynamicLoader**: Runtime class loading with caching
- **AppInit**: Application initialization utilities

### Fixed
- N/A (initial release)

### Changed
- N/A (initial release)

### Deprecated
- N/A (initial release)

### Removed
- N/A (initial release)

### Security
- Safe mathematical expression evaluation without eval()
- Parameterized SQL queries to prevent injection
- Flatpak sandboxing for controlled environment
- Limited filesystem and network access
- Input validation throughout

## Version History

### Version Numbering

Launcher follows [Semantic Versioning](https://semver.org/):
- **MAJOR** version: Incompatible API changes
- **MINOR** version: New functionality (backward compatible)
- **PATCH** version: Bug fixes (backward compatible)

### Release Schedule

- **Development**: Active development on main branch
- **Alpha**: Feature testing (breaking changes possible)
- **Beta**: Stabilization phase (minimal breaking changes)
- **Stable**: Production-ready releases

### Support Policy

- **Current version**: Full support with bug fixes and features
- **Previous version**: Security fixes only
- **Older versions**: No support (please upgrade)

## Upgrade Guide

### From 0.0.1 to Future Versions

When upgrading:

1. **Backup your data**:
   ```bash
   cp -r ~/.local/share/cloud.ivanbotty.Launcher ~/launcher-backup
   ```

2. **Check breaking changes**: Review changelog for breaking changes

3. **Update installation**:
   ```bash
   # For Flatpak
   cd launcher-app
   git pull
   flatpak-builder --user --install --force-clean build-dir manifest.yaml
   
   # For source
   git pull
   python3 -m cloud.ivanbotty.Launcher
   ```

4. **Verify configuration**: Check preferences after upgrade

5. **Report issues**: If problems occur, report on GitHub

## Contributing

Found a bug or want to suggest a feature? See [Contributing Guide](Contributing.md).

## Links

- **Repository**: https://github.com/BottyIvan/launcher-app
- **Issues**: https://github.com/BottyIvan/launcher-app/issues
- **Releases**: https://github.com/BottyIvan/launcher-app/releases

## Acknowledgments

### Core Technologies
- GTK4 and Adwaita for beautiful UI
- PyGObject for Python bindings
- SQLite for data persistence
- Flatpak for distribution

### Contributors
- Ivan Bottigelli (@BottyIvan) - Project creator and maintainer

Thank you to all contributors and users! 🎉

---

## Legend

- `Added` - New features
- `Changed` - Changes to existing functionality
- `Deprecated` - Soon-to-be removed features
- `Removed` - Removed features
- `Fixed` - Bug fixes
- `Security` - Security improvements

## Future Roadmap

### v0.1.0 (Next Release)
- Complete command service implementation
- Full AI assistant with Gemini API
- File search functionality
- Link management system
- Performance optimizations
- Bug fixes from initial release

### v0.2.0
- Plugin system for third-party extensions
- Web search integration
- Calculator history
- Enhanced keyboard shortcuts
- Improved preferences UI

### v0.3.0
- Clipboard manager integration
- Window switcher
- Multi-monitor improvements
- Localization support (i18n)
- Additional themes

### v1.0.0 (Stable)
- Feature complete and stable
- Comprehensive documentation
- Full test coverage
- Performance optimized
- Production ready

See [Features](Features.md) for more details on upcoming features.
