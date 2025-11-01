project('launcher-app', 'python',
  version: '0.0.1',
  meson_version: '>= 0.59.0',
  default_options: [
    'warning_level=2',
  ],
)

# Get Python installation
python = import('python').find_installation('python3')

# Prefix and data directories
prefix = get_option('prefix')
bindir = prefix / get_option('bindir')
datadir = prefix / get_option('datadir')
pkgdatadir = datadir / meson.project_name()

# Python module directory
py_installation = python.install_sources(
  [],
  subdir: 'cloud/ivanbotty',
  pure: true,
)

# Install Python package structure
subdir('cloud')

# Install desktop file
install_data(
  'cloud.ivanbotty.Launcher.desktop',
  install_dir: datadir / 'applications',
)

# Install manifest.yaml
install_data(
  'manifest.yaml',
  install_dir: pkgdatadir,
)

# Install resources (icons, data files)
install_subdir(
  'cloud/ivanbotty/Launcher/resources',
  install_dir: pkgdatadir / 'Launcher',
  strip_directory: false,
)

# Create wrapper script for the launcher
configure_file(
  input: 'launcher-wrapper.sh.in',
  output: 'cloud-ivanbotty-launcher',
  configuration: {
    'PYTHON': python.full_path(),
    'pkgdatadir': pkgdatadir,
  },
  install: true,
  install_dir: bindir,
  install_mode: 'rwxr-xr-x',
)

# Summary
summary({
  'prefix': prefix,
  'bindir': bindir,
  'datadir': datadir,
  'pkgdatadir': pkgdatadir,
}, section: 'Directories')

summary({
  'Python': python.full_path(),
}, section: 'Programs')
