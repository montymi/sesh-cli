from typing import List
from models.managers import PluginManager
from models.commands import ConversationServiceCommand, ExitServiceCommand, ExportServiceCommand, HelpServiceCommand, HabitsServiceCommand, ImportServiceCommand, NotesServiceCommand

class ServiceController:

    def __init__(self, model, view, plugin_directory="resources/plugins") -> None:
        self.clerk = model
        self.view = view
        self.services = {}
        self.plugin_directory = plugin_directory
        self._init_plugins_()
        self._init_services_()

    def _init_plugins_(self):
        plugin_manager = PluginManager(self.plugin_directory)
        try:
            for service in plugin_manager.discover_plugins():
                self.services[service.name()] = service
        except AttributeError as e:
            self.view.post_response(e)
 
    def _init_services_(self):
        try:
            for service in self.service_loader():
                self.services[service.name()] = service
        except AttributeError as e:
            self.view.post_response(e)
        self.view._load_services_(self.services.keys())
    
    def service_loader(self) -> List:
        services = []
        services.append(HelpServiceCommand())
        services.append(ExitServiceCommand())
        services.append(HabitsServiceCommand(self.clerk.habits))
        services.append(ImportServiceCommand(self.clerk.librarian))
        services.append(ExportServiceCommand(self.clerk.librarian))
        services.append(NotesServiceCommand(self.clerk.librarian.journal))
        services.append(ConversationServiceCommand(self.clerk.librarian))
        return services
        
    def execute(self, prompt, history: List):
        command = self.services.get(prompt)
        if command:
            if prompt == "export" or prompt == "conversation":
                command.execute(self.view, history)
            else: command.execute(self.view) 
            return 1
        return -1

