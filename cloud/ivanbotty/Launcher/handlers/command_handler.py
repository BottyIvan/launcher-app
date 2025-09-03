from gi.repository import Gtk
import cloud.ivanbotty.Launcher.handlers.base_input_handler as bih

class CommandHandler(bih.BaseInputHandler):
    def can_handle(self, text):
        return text.startswith(">")

    def handle(self, text, services, listbox):
        command_name = text[1:].strip()
        commands_service = services.get("command")
        listbox.remove_all()
        if commands_service:
            commands = commands_service.filter_commands(command_name)
            for cmd in commands:
                listbox.insert(Gtk.Label(label=cmd.name), 0)
            if commands:
                commands[0].run()
