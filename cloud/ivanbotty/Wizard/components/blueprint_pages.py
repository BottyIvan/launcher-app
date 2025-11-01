#!/usr/bin/env python3
"""
Blueprint-based page components for the Wizard.
"""
import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw, GObject
from typing import Callable


@Gtk.Template(resource_path="/cloud/ivanbotty/Wizard/welcome-page.ui")
class WelcomePage(Gtk.Box):
    """Welcome page loaded from Blueprint UI."""
    
    __gtype_name__ = "WelcomePage"
    
    action_button = Gtk.Template.Child()
    
    def __init__(self, callback: Callable = None):
        super().__init__()
        if callback:
            self.action_button.connect("clicked", lambda *_: callback())


@Gtk.Template(resource_path="/cloud/ivanbotty/Wizard/summary-page.ui")
class SummaryPage(Gtk.Box):
    """Summary page loaded from Blueprint UI."""
    
    __gtype_name__ = "SummaryPage"
    
    action_button = Gtk.Template.Child()
    
    def __init__(self, callback: Callable = None):
        super().__init__()
        if callback:
            self.action_button.connect("clicked", lambda *_: callback())
