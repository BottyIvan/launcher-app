import gi

gi.require_version("Adw", "1")
gi.require_version("Gtk", "4.0")
from gi.repository import Adw, Gtk
import cloud.ivanbotty.database.sqlite3 as db


class Preferences(Adw.PreferencesDialog):
    """Enhanced preferences dialog with better organization and modern styling.
    
    Features:
    - Organized into logical pages
    - Better visual hierarchy
    - Improved descriptions and help text
    - Modern Adwaita widgets
    """
    
    def __init__(self, app):
        super().__init__(title="Preferences")
        self.app = app
        
        # Create the main preferences pages
        self._create_general_page()
        self._create_appearance_page()
        self._create_extensions_page()
        self._create_api_page()

    def _create_general_page(self):
        """Create the general settings page."""
        page_general = Adw.PreferencesPage()
        page_general.set_title("General")
        page_general.set_icon_name("preferences-system-symbolic")

        # About group for application info
        about_group = Adw.PreferencesGroup(title="About")
        about_group.set_description("Information about Launcher")

        # Information row with app details
        info_row = Adw.ActionRow(
            title="Launcher",
            subtitle="Modern application launcher for Linux"
        )
        info_row.set_activatable(True)
        info_row.add_suffix(Gtk.Image.new_from_icon_name("go-next-symbolic"))

        # Show about dialog when activated
        def on_info_row_activated(row):
            about = Adw.AboutDialog.new_from_appdata(
                "/cloud/ivanbotty/Launcher/resources/appdata.xml", "0.0.1"
            )
            about.set_developers(["Ivan Bottigelli https://ivanbotty.cloud"])
            about.set_copyright("© 2025 Ivan Bottigelli.")
            about.present()

        info_row.connect("activated", on_info_row_activated)
        about_group.add(info_row)

        page_general.add(about_group)
        self.add(page_general)

    def _create_appearance_page(self):
        """Create the appearance settings page."""
        page_appearance = Adw.PreferencesPage()
        page_appearance.set_title("Appearance")
        page_appearance.set_icon_name("applications-graphics-symbolic")

        # Layout settings group
        layout_group = Adw.PreferencesGroup(
            title="Layout",
            description="Customize the application window appearance"
        )

        # Switch row for enabling/disabling compact layout
        self.layout_switch = Adw.SwitchRow(
            active=(db.get_pref("layout", "default") == "compact"),
            title="Compact Layout",
            subtitle="Use a smaller, more condensed interface",
        )
        # Save layout preference when toggled
        self.layout_switch.connect(
            "notify::active",
            lambda sw, _: db.set_pref("layout", "compact" if sw.get_active() else "default"),
        )
        layout_group.add(self.layout_switch)

        # Add info about restart if needed
        restart_label = Gtk.Label(
            label="Note: Some appearance changes may require restarting the application",
            wrap=True,
            xalign=0,
        )
        restart_label.add_css_class("dim-label")
        restart_label.add_css_class("caption")
        restart_label.set_margin_top(6)
        layout_group.add(restart_label)

        page_appearance.add(layout_group)
        self.add(page_appearance)

    def _create_extensions_page(self):
        """Create the extensions settings page."""
        page_extensions = Adw.PreferencesPage()
        page_extensions.set_title("Extensions")
        page_extensions.set_icon_name("application-x-addon-symbolic")

        # Extensions settings group
        extension_group = Adw.PreferencesGroup(
            title="Available Extensions",
            description="Enable or disable functionality modules"
        )

        # Get available extensions and their saved states
        extension_list = self.app.extensions_service.list_extensions()
        saved_exts = db.get_extensions()

        # Add a switch for each extension to enable/disable it
        for extension in extension_list:
            ext_switch = Adw.SwitchRow(
                active=saved_exts.get(extension.name, extension.enabled),
                title=extension.name or "Unnamed Extension",
                subtitle=extension.description or "No description available",
            )
            
            # Disable toggling for extensions that can't be disabled
            if hasattr(extension, 'cant_disable') and extension.cant_disable:
                ext_switch.set_sensitive(False)
                ext_switch.set_subtitle(f"{extension.description} (Required)")
            
            # Save extension enabled state when toggled
            ext_switch.connect(
                "notify::active",
                lambda sw, _, ext_id=extension.service: db.set_extension_enabled(
                    ext_id, sw.get_active()
                ),
            )
            extension_group.add(ext_switch)

        page_extensions.add(extension_group)
        self.add(page_extensions)

    def _create_api_page(self):
        """Create the API keys settings page."""
        page_api = Adw.PreferencesPage()
        page_api.set_title("API Keys")
        page_api.set_icon_name("network-server-symbolic")

        # API keys settings group
        api_group = Adw.PreferencesGroup(
            title="API Configuration",
            description="Configure external service integrations"
        )

        # Info banner
        info_banner = Adw.Banner()
        info_banner.set_title("Gemini API Key Required")
        info_banner.set_button_label("Get API Key")
        info_banner.connect("button-clicked", lambda b: Gtk.show_uri(
            None, "https://aistudio.google.com/app/apikey", 0
        ))
        api_group.add(info_banner)

        label_info = Gtk.Label(
            label=(
                "To use AI-powered features, you need a Gemini API key. "
                "Visit the link above to create an account and generate your key. "
                "Keep your API key secure and do not share it with others."
            ),
            wrap=True,
            xalign=0,
            margin_top=12,
            margin_bottom=12,
        )
        label_info.add_css_class("dim-label")
        label_info.set_halign(Gtk.Align.START)
        api_group.add(label_info)

        # Row for Gemini API key input
        gemini_row = Adw.PasswordEntryRow(
            title="Gemini API Key",
            text=db.get_api_key("gemini") or ""
        )
        gemini_row.set_show_apply_button(True)
        gemini_row.connect("apply", self.on_api_key_apply, "gemini")
        api_group.add(gemini_row)

        # Model selection group
        model_group = Adw.PreferencesGroup(
            title="Model Selection",
            description="Choose which AI model to use"
        )

        # Gemini model selection row
        gemini_model_row = Adw.ComboRow(
            title="Gemini Model",
            subtitle="Different models offer varying capabilities and speed",
            model=Gtk.StringList.new(["gemini-1.5-flash", "gemini-1.5-pro", "gemini-2.0-flash"]),
        )
        gemini_model_row.set_selected(0)
        model_group.add(gemini_model_row)

        page_api.add(api_group)
        page_api.add(model_group)
        self.add(page_api)

    def on_api_key_apply(self, row, service):
        """Save the API key when applied."""
        text = row.get_text().strip()
        if text:
            db.set_api_key(service, text)
