import importlib
import inspect
import os
import sys
from models.commands import Command
from models.importers.importer import Importer

class PluginManager:
    def __init__(self, plugin_directory):
        self.plugin_directory = plugin_directory
        self.plugins = []

    def discover_plugins(self):
        sys.path.insert(0, self.plugin_directory)
        for module_name in os.listdir(self.plugin_directory):
            if module_name.endswith(".py") and module_name != "__init__.py":
                module_name = module_name[:-3]  # Remove the .py extension
                module = importlib.import_module(module_name)
                for name, obj in inspect.getmembers(module, inspect.isclass):
                    # Check if the class is a subclass of Command and not Command itself
                    if issubclass(obj, Command) and obj is not Command:
                        # Ensure the class implements the required methods
                        if hasattr(obj, 'name') and callable(getattr(obj, 'name')) and \
                           hasattr(obj, 'execute') and callable(getattr(obj, 'execute')):
                            self.plugins.append(obj())
                            print(f"Registered plugin: {name}") # TODO: change to logs for debugging
                        else:
                            print(f"Class {name} does not implement required methods.") # TODO: change to logs for debugging
        return self.plugins

class ImporterManager:
    def __init__(self, importer_directory):
        self.importer_directory = importer_directory
        self.importers = []

    def discover_plugins(self):
        sys.path.insert(0, self.importer_directory)
        for module_name in os.listdir(self.importer_directory):
            if module_name.endswith(".py") and module_name != "__init__.py":
                module_name = module_name[:-3]  # Remove the .py extension
                module = importlib.import_module(module_name)
                for name, obj in inspect.getmembers(module, inspect.isclass):
                    # Check if the class is a subclass of Command and not Command itself
                    if issubclass(obj, Importer) and obj is not Importer:
                        # Ensure the class implements the required methods
                        if hasattr(obj, 'name') and callable(getattr(obj, 'name')) and \
                           hasattr(obj, 'execute') and callable(getattr(obj, 'execute')):
                            self.importers.append(obj())
        return self.importers
