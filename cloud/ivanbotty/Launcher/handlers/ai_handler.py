from gi.repository import Gtk
import cloud.ivanbotty.Launcher.handlers.base_input_handler as bih

class AIHandler(bih.BaseInputHandler):
    def can_handle(self, text):
        return text.startswith("ask")

    def handle(self, text, services, listbox):
        ai_service = services.get("ai")
        query = text.strip()
        listbox.remove_all()
        if ai_service:
            result = ai_service.ask(query)
            listbox.insert(Gtk.Label(label=f"AI: {result}"), 0)
