# Install cloud.ivanbotty.Wizard package
wizard_sources = [
  '__init__.py',
  '__main__.py',
  'app.py',
  'blueprint_ui.py',
]

python.install_sources(
  wizard_sources,
  subdir: 'cloud/ivanbotty/Wizard',
  pure: true,
)

# Install components submodule
python.install_sources(
  'components/__init__.py',
  'components/page.py',
  subdir: 'cloud/ivanbotty/Wizard/components',
  pure: true,
)

# Blueprint compilation
gnome = import('gnome')

# Detect blueprint-compiler (minimum recommended version: 0.4.0)
# Graceful fallback: if not found, app will use programmatic UI creation
blueprint_compiler = find_program('blueprint-compiler', required: false)

if blueprint_compiler.found()
  # Blueprint files to compile
  blp_files = files(
    'resources/blueprints/wizard-window.blp',
    'resources/blueprints/welcome-page.blp',
    'resources/blueprints/summary-page.blp',
    'resources/blueprints/wizard-page.blp',
  )

  # Compile blueprints to UI files
  compiled_ui = custom_target(
    'compile-blueprints',
    input: blp_files,
    output: [
      'wizard-window.ui',
      'welcome-page.ui',
      'summary-page.ui',
      'wizard-page.ui',
    ],
    command: [
      blueprint_compiler,
      'batch-compile',
      '@OUTDIR@',
      '@CURRENT_SOURCE_DIR@/resources/blueprints',
      '@INPUT@',
    ],
    build_by_default: true,
    install: false,
  )

  # Compile GResource bundle
  wizard_resources = gnome.compile_resources(
    'wizard-resources',
    'resources/wizard.gresource.xml',
    gresource_bundle: true,
    source_dir: meson.current_build_dir(),
    dependencies: compiled_ui,
    install: true,
    install_dir: get_option('datadir') / meson.project_name() / 'Wizard',
  )
else
  warning('blueprint-compiler not found. Blueprint UI files will not be compiled.')
endif
