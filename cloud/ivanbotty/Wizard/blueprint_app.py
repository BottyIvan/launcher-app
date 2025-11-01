#!/usr/bin/env python3
"""
Blueprint-based Wizard Application.
"""
import logging
import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Adw, Gtk, GObject

# Setup logger
logger = logging.getLogger("WelcomeWizard")
logging.basicConfig(level=logging.INFO)

# Global variables to store template classes
_WizardWindow = None
_WelcomePage = None
_SummaryPage = None


def initialize_templates():
    """
    Initialize all template classes after resources are loaded.
    This must be called after Gio.resources_register().
    """
    global _WizardWindow, _WelcomePage, _SummaryPage
    
    if _WizardWindow is not None:
        return  # Already initialized
    
    from typing import Callable
    
    # Define WelcomePage template class
    @Gtk.Template(resource_path="/cloud/ivanbotty/Wizard/welcome-page.ui")
    class WelcomePage(Gtk.Box):
        """Welcome page loaded from Blueprint UI."""
        
        __gtype_name__ = "WelcomePage"
        
        action_button = Gtk.Template.Child()
        
        def __init__(self, callback: Callable = None):
            super().__init__()
            if callback:
                self.action_button.connect("clicked", lambda *_: callback())

    # Define SummaryPage template class
    @Gtk.Template(resource_path="/cloud/ivanbotty/Wizard/summary-page.ui")
    class SummaryPage(Gtk.Box):
        """Summary page loaded from Blueprint UI."""
        
        __gtype_name__ = "SummaryPage"
        
        action_button = Gtk.Template.Child()
        
        def __init__(self, callback: Callable = None):
            super().__init__()
            if callback:
                self.action_button.connect("clicked", lambda *_: callback())
    
    # Define WizardWindow template class
    @Gtk.Template(resource_path="/cloud/ivanbotty/Wizard/wizard-window.ui")
    class WizardWindow(Adw.ApplicationWindow):
        """Main wizard window loaded from Blueprint UI."""
        
        __gtype_name__ = "WizardWindow"
        
        content_carousel = Gtk.Template.Child()
        window_title = Gtk.Template.Child()
        
        def __init__(self, application, **kwargs):
            super().__init__(application=application, **kwargs)
            self.application = application
            self.setup_pages()
        
        def setup_pages(self):
            """Setup wizard pages in the carousel."""
            # Create pages with callbacks
            welcome_page = _WelcomePage(callback=self.on_next)
            summary_page = _SummaryPage(callback=self.on_finish)
            
            # Add pages to carousel
            self.content_carousel.append(welcome_page)
            self.content_carousel.append(summary_page)
            
            logger.info("Wizard pages setup complete")
        
        def on_next(self):
            """Move to the next page."""
            cur = self.content_carousel.get_position()
            n = self.content_carousel.get_n_pages()
            if cur < n - 1:
                next_w = self.content_carousel.get_nth_page(int(cur) + 1)
                logger.info(f"Scrolling to page {int(cur) + 1}")
                self.content_carousel.scroll_to(next_w, True)
                self.window_title.set_title("Summary")
        
        def on_finish(self):
            """Finish the wizard."""
            logger.info("Wizard completed!")
            self.application.quit()
    
    # Store classes in global variables
    _WizardWindow = WizardWindow
    _WelcomePage = WelcomePage
    _SummaryPage = SummaryPage
    
    logger.info("Blueprint templates initialized")


class WelcomeWizard(Adw.Application):
    """Wizard Application using Blueprint UI."""
    
    def __init__(self, app):
        super().__init__(application_id=app)
        self.win = None
    
    def do_activate(self):
        """Activates the application and shows the window."""
        logger.info("Application activated")
        
        # Initialize templates if not already done
        initialize_templates()
        
        if self.win is None:
            self.win = _WizardWindow(application=self)
        self.win.present()
