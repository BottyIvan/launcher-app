project('launcher-app',
  version: '0.0.1',
  meson_version: '>= 0.59.0',
)

# Find blueprint-compiler
blueprintc = find_program('blueprint-compiler', required: true)

# Blueprint source files
blueprint_sources = [
  'ui/main_window.blp',
  'ui/search_entry.blp',
  'ui/list_row.blp',
  'ui/footer.blp',
  'ui/preferences.blp',
]

# Compile Blueprint files to UI files
compiled_ui_files = []
foreach blueprint : blueprint_sources
  # Get the base name without extension
  base_name = blueprint.underscorify().replace('_blp', '')
  ui_file = base_name + '.ui'
  
  compiled_ui_files += custom_target(
    ui_file,
    input: blueprint,
    output: ui_file,
    command: [blueprintc, 'compile', '--output', '@OUTPUT@', '@INPUT@'],
    install: false,
  )
endforeach

# Make compiled UI files available as a dependency
ui_files = declare_dependency(
  sources: compiled_ui_files,
)
