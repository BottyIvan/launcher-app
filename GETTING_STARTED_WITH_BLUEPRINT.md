# Getting Started with GTK Blueprint

Welcome! This guide will help you start using the GTK Blueprint infrastructure in the Launcher project.

## 🚀 Quick Start (3 minutes)

### Step 1: Verify Setup

```bash
python3 verify_blueprints.py
```

Expected output: All checks pass with ✓ marks.

### Step 2: Look at the Examples

```bash
cat examples_blueprint.py
```

This file shows how to use Gtk.Template with each UI component.

### Step 3: Try Running the App

```bash
python3 -m cloud.ivanbotty.Launcher
```

The app runs normally - Blueprint files are ready for future use!

## �� Learn More (10 minutes)

### Understanding Blueprint

Blueprint is a markup language for GTK that lets you define UI declaratively:

**Before (Python):**
```python
box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
label = Gtk.Label(label="Hello")
box.append(label)
```

**After (Blueprint):**
```blueprint
Box {
  orientation: vertical;
  spacing: 6;
  Label { label: "Hello"; }
}
```

### Key Files to Read

1. **BLUEPRINT_REFERENCE.md** (5 min) - Quick syntax reference
2. **examples_blueprint.py** (5 min) - Working code examples
3. **README.md** (Blueprint section) - Complete overview

## 🛠️ Common Tasks

### Task 1: Edit an Existing Blueprint

```bash
# 1. Edit the file
vim ui/search_entry.blp

# 2. Compile it
python3 compile_blueprints.py

# 3. Test your changes
python3 -m cloud.ivanbotty.Launcher
```

### Task 2: Create a New Blueprint Widget

```bash
# 1. Create the .blp file
cat > ui/my_widget.blp << 'BLUEPRINT'
using Gtk 4.0;

template $MyWidget : Gtk.Box {
  orientation: vertical;
  spacing: 6;
  
  Label {
    label: "My Widget";
  }
}
BLUEPRINT

# 2. Compile it
python3 compile_blueprints.py

# 3. Use it in Python (see examples_blueprint.py for pattern)
```

### Task 3: Migrate an Existing Widget

Follow the guide in **BLUEPRINT_MIGRATION.md** for step-by-step instructions.

## 🎓 Learning Path

### Beginner (Day 1)
1. Run `verify_blueprints.py`
2. Read `BLUEPRINT_REFERENCE.md` 
3. Look at `ui/search_entry.blp` (simplest example)
4. Study the corresponding example in `examples_blueprint.py`

### Intermediate (Day 2-3)
1. Read `BLUEPRINT_MIGRATION.md`
2. Study `ui/main_window.blp` (complex layout)
3. Look at `ui/footer.blp` (Adwaita widgets)
4. Try modifying a .blp file and recompiling

### Advanced (Week 1)
1. Migrate a simple widget to use Gtk.Template
2. Read the full README Blueprint section
3. Study `ui/preferences.blp` (multi-page dialog)
4. Create a new custom widget with Blueprint

## 💡 Tips for Success

### Do's ✅
- Start with simple widgets
- Use meaningful IDs for template children
- Follow the examples in examples_blueprint.py
- Test after each change
- Read error messages carefully

### Don'ts ❌
- Don't put business logic in Blueprint (only UI)
- Don't forget to compile after editing .blp
- Don't worry if you make mistakes (just recompile)
- Don't skip the documentation

## 🔧 Troubleshooting

### "blueprint-compiler not found"

Install it:
```bash
# Ubuntu/Debian
sudo apt install blueprint-compiler

# Fedora
sudo dnf install blueprint-compiler

# Arch
sudo pacman -S blueprint-compiler
```

### "Template class not found"

Check that `__gtype_name__` matches the template name:
```python
template $MyWidget : Gtk.Box { }  # In .blp

class MyWidget(Gtk.Box):
    __gtype_name__ = 'MyWidget'  # Must match
```

### "Child widget not found"

Verify the ID in the .blp file matches the Python variable:
```blueprint
Button my_button { }  # In .blp
```
```python
my_button = Gtk.Template.Child()  # In Python
```

## 📖 Documentation Quick Links

- **Quick Reference**: BLUEPRINT_REFERENCE.md
- **Migration Guide**: BLUEPRINT_MIGRATION.md
- **Examples**: examples_blueprint.py
- **Full Docs**: README.md (Blueprint section)
- **Summary**: BLUEPRINT_SUMMARY.md
- **Deliverables**: DELIVERABLES.md

## 🎯 Next Steps

Choose your path:

**I want to learn Blueprint:**
→ Read BLUEPRINT_REFERENCE.md
→ Study examples_blueprint.py
→ Try editing ui/search_entry.blp

**I want to migrate a widget:**
→ Read BLUEPRINT_MIGRATION.md
→ Follow the step-by-step guide
→ Start with a simple widget

**I want to create new UI:**
→ Look at existing .blp files
→ Use BLUEPRINT_REFERENCE.md as guide
→ Follow patterns in examples_blueprint.py

**I want to understand the system:**
→ Read BLUEPRINT_SUMMARY.md
→ Review DELIVERABLES.md
→ Check README.md Blueprint section

## 🤝 Need Help?

1. Check **BLUEPRINT_REFERENCE.md** for syntax
2. Check **BLUEPRINT_MIGRATION.md** for how-to guides
3. Look at **examples_blueprint.py** for working code
4. Read error messages carefully (they're usually helpful)
5. Verify setup with `verify_blueprints.py`

## 🎉 You're Ready!

You now have everything you need to start using Blueprint in the Launcher project. Pick a task from the "Common Tasks" section above and dive in!

Remember: Blueprint makes UI development easier and more maintainable. Start small, learn the patterns, and enjoy building beautiful GTK interfaces!
