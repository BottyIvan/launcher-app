from gi.repository import Gio
from cloud.ivanbotty.LightFlow.models.applications_model import ApplicationModel

import cloud.ivanbotty.LightFlow.handlers.base_input_handler as bih


class AIHandler(bih.BaseInputHandler):
    def can_handle(self, text):
        return text.startswith("ask")

    def handle(self, text, services):
        list_model = Gio.ListStore(item_type=ApplicationModel)
        ai_service = services.get("ai")
        query = text.strip()
        if ai_service and query:
            try:
                answer = ai_service.ask(query)
                name = "AI Answer"
                description = answer
                icon = "dialog-information"
            except Exception as e:
                name = "Error"
                description = str(e)
                icon = "dialog-error"
        else:
            name = "Error"
            description = "AI service not available or query is empty."
            icon = "dialog-error"
        list_model.append(
            ApplicationModel(
                type="ai", name=name, description=description, exec_cmd=None, icon=icon
            )
        )
        return list_model
