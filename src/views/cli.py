from typing import Dict, List
from prompt_toolkit.completion import Completer, Completion, FuzzyCompleter
from prompt_toolkit.shortcuts import CompleteStyle, prompt


class ServiceCompleter(Completer):
    def __init__(self, services) -> None:
        self.services = services

    def get_completions(self, document, complete_event):
        text_before_cursor = document.text_before_cursor
        if ' ' not in text_before_cursor:
            word = document.get_word_before_cursor()
            for service in self.services:
                if service.startswith(word):
                    yield Completion(
                        service,
                        start_position=-len(word),
                        style="fg:" + "purple",
                        selected_style="fg:white bg:" + "purple",
                    )
class CLI:
    def __init__(self) -> None:
        pass

    def prompt_for_login(self):
        print("<<< Welcome to Sesh! Please log in to continue.")
        print("<<< If you don't have an account, ENTER to create one.")

    def prompt_for_username(self):
        return input("> Username: ")
    
    def prompt_for_register(self):
        username = input("<<< Please enter a 6 digit username to register (case does not matter): \n> Create Username: ")
        return username.lower()

    def _load_services_(self, services: List):
        self.services = services

    def get_entry(self):
        return prompt(">>> ", 
            completer=FuzzyCompleter(ServiceCompleter(self.services)),
            complete_style=CompleteStyle.MULTI_COLUMN)

    def get_service_input(self):
        return prompt("> ")

    def post_welcome(self, message):
        print(message)

    def post_save_request(self):
        print("<<< Would you like to save this conversation? y/N")

    def post_response(self, content):
        print("<<<", content)

    def post_context(self, context):
        print("<< Context")
        for doc in context:
            source = doc.metadata.get('source', 'Unknown Source')
            content = doc.page_content if doc.page_content else 'No Content'
            print(f"Source: {source}")
            print(f"Content: {content}\n")

    def post_logs(self, logs: List):
        if not logs:
            return
        print("Current conversations:\n" + "\n".join(logs) + "\n")
 
    def post_models(self, models: List):
        if not models:
            return
        print("Current models:\n" + "\n".join(models) + "\n")

    def post_importers(self, importers: Dict):
        print("Select an importer for the path:\n" + "\n".join([f"{idx + 1}. {importer.name()}" for idx, importer in enumerate(importers)]))

    def exit(self):
        print("<<< Arrivederci! Hope to talk soon.")

    def errors(self, message):
        print(message, "| \033[33mTry opening Ollama\033[0m")
