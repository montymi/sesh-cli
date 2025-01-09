from abc import ABC, abstractmethod
import os
import json
from typing import List, Tuple


class Command(ABC):
    def __init__(self, data=None):
        self.data = data
    
    @abstractmethod
    def name(self):
        pass

    @abstractmethod
    def execute(self, view):
        pass

class HelpServiceCommand(Command):
    def name(self):
        return "help"

    def execute(self, view):
        view.post_response("I am your personal Clerk, here to answer any questions, keep track of journal entries, and assist in research. Any settings such as habit forming and changing the AI model can be accessed by the autocomplete commands built into the prompt input.")

class ExitServiceCommand(Command):
    def name(self):
        return "exit"

    def execute(self, view):
        raise KeyboardInterrupt

class HabitsServiceCommand(Command):
    def name(self):
        return "habits"

    def execute(self, view):
        view.post_response(f"Habits service in progress. Would you like to add a habit or toggle an existing one? (add, toggle (all on, all off), back)\n{self.data}")
        self._habits_service_input_(view)
    
    def _habits_service_input_(self, view):
        selection = view.get_service_input()
        if selection == "back":
            return
        elif selection == "add":
            view.post_response("What habit would you like to add? Write a name first, and then a prompt/description. Note that this will be added to every input while the habit is toggled on.")
            name = view.get_service_input()
            description = view.get_service_input()
            self.data.add(name, description)
        elif selection == "toggle":
            view.post_response("Which habit would you like to toggle?")
            habit = view.get_service_input()
            self.data.toggle(habit)
        elif selection == "toggle all on":
            view.post_response("Toggling all habits on...")
            self.data.toggle_all(True)
        elif selection == "toggle all off":
            view.post_response("Toggling all habits on...")
            self.data.toggle_all(False)
        else:
            view.post_response("That service is not available for habits at this moment")
        view.post_response(f"What would you like to do next with the Habits service? (add, toggle, back)\n{self.data}")
        self._habits_service_input_(view)

class ImportServiceCommand(Command):
    def name(self):
        return "import"

    def execute(self, view):
        view.post_response(f"Import service in progress. Please input file path relative to \033[95m{os.getcwd()}\033[0m ('back' to return to Clerk).")
        self._import_service_input_(view)

    def _get_importer(self, selection):
        for name, importer in self.data.importers.items():
            if selection.endswith(name):
                return importer
        return None

    def _get_extra_importers(self):
        return [importer for name, importer in self.data.importers.items() if not any(char in str(name) for char in ['.'])]

    def _prompt_user_for_importer(self, view, importers):
        view.post_importers(importers)
        user_input = view.get_service_input()
        if user_input == "back":
            return
        try:
            selected_index = int(user_input) - 1
            if 0 <= selected_index < len(importers):
                return importers[selected_index]
        except ValueError:
            view.post_response("Invalid selection. Please enter a number corresponding to an importer. ('back' to return to Clerk)")
            self._prompt_user_for_importer(view, importers)

    def _import_service_input_(self, view):
        docs = []
        selection = view.get_service_input()
        if selection == "back":
            return
        else:
            if os.path.isfile(selection):
                importer = self._get_importer(selection)
                if importer:
                    docs = importer.execute(selection)
                else:
                    importer = self._get_importer(".txt")
                    docs = importer.execute(selection)
            else:
                extra_importers = self._get_extra_importers()
                importer = self._prompt_user_for_importer(view, extra_importers)
                if not importer:
                    return
            try:
                docs = importer.execute(selection)
                chunks = self.data.split(docs)
                self.data.embed(chunks)
                view.post_response(f"\033[92mSuccess\033[0m - uploaded {len(docs)} documents for {selection}")
            except Exception as e:
                view.post_response(e)
        view.post_response("Input another path to continue or 'back' to return to the Clerk")
        self._import_service_input_(view)

class ExportServiceCommand(Command):
    def name(self):
        return "export"

    def execute(self, view, desired_data: List):
        view.post_response(f"Export service in progress. Please input directory path relative to \033[95m{os.getcwd()}\033[0m ('back' to return to Clerk).")
        self._export_service_input(view, desired_data)

    def _export_service_input(self, view, desired_data):
        selection = view.get_service_input()
        if selection == "back":
            return
        elif os.path.exists(selection):
            if not os.path.isdir(selection):
                view.post_response("Input a directory path please.")
                self._export_service_input(view, desired_data)
            else:
                view.post_response("Would you like to name the shared conversation? Defaults to datetime.")
                name = view.get_service_input() or self.data.date()
                view.post_response("Add any note you would like to add to the conversation below.")
                note = view.get_service_input() or ""
                path = selection+"/"+name
                if self.data.export(desired_data, path, name, note) == 1:
                    view.post_response(f"\033[92mSuccess\033[0m - exported conversation to {path}.")
        else: view.post_response("You have inputted an invalid directory path.")
        view.post_response("Input another path to continue or 'back' to return to the Clerk.")
        self._export_service_input(view, desired_data)

class NotesServiceCommand(Command):
    def name(self):
        return "notes"

    def execute(self, view):
        view.post_response(f"Notes service in progress. What would you like to do? (create, read, update, delete, search, list, back)")
        self._notes_service_input_(view)

    def _notes_service_input_(self, view):
        selection = view.get_service_input()
        if selection == "back":
            return
        elif selection == "create":
            self._handle_create(view)
        elif selection == "read":
            self._handle_read(view)
        elif selection == "update":
            self._handle_update(view)
        elif selection == "delete":
            self._handle_delete(view)
        elif selection == "search":
            self._handle_search(view)
        elif selection == "list":
            self._handle_list(view)
        else:
            view.post_response("Invalid selection. Please choose a valid option.")

        if selection != "back":
            view.post_response(f"What would you like to do next with the Notes service? (create, read, update, delete, search, list, back)")
            self._notes_service_input_(view)

    def _handle_create(self, view):
        view.post_response("To create a note, provide a title and content. First, enter the title:")
        title = view.get_service_input()
        if title.lower() == "back":
            return
        view.post_response("Now, enter the content:")
        content = view.get_service_input()
        if content.lower() == "back":
            return
        note_id = self.data.create_note(title, content)
        view.post_response(f"Note created with ID: {note_id}")

    def _handle_read(self, view):
        view.post_response("Which note would you like to read? Provide the note ID:")
        note_id = view.get_service_input()
        if note_id.lower() == "back":
            return
        try:
            content = self.data.read_note(note_id)
            view.post_response(f"Note Content:\n{content}")
        except ValueError as e:
            view.post_response(str(e))

    def _handle_update(self, view):
        view.post_response("Which note would you like to update? Provide the note ID:")
        note_id = view.get_service_input()
        if note_id.lower() == "back":
            return
        view.post_response("Provide the new content for the note:")
        new_content = view.get_service_input()
        if new_content.lower() == "back":
            return
        try:
            self.data.update_note(note_id, new_content)
            view.post_response("Note updated successfully.")
        except ValueError as e:
            view.post_response(str(e))

    def _handle_delete(self, view):
        view.post_response("Which note would you like to delete? Provide the note ID:")
        note_id = view.get_service_input()
        if note_id.lower() == "back":
            return
        try:
            self.data.delete_note(note_id)
            view.post_response("Note deleted successfully.")
        except ValueError as e:
            view.post_response(str(e))

    def _handle_search(self, view):
        view.post_response("Enter a keyword to search for notes:")
        keyword = view.get_service_input()
        if keyword.lower() == "back":
            return
        results = self.data.search_notes(keyword)
        if results:
            response = "Search Results:\n" + "\n".join([f"ID: {note_id}, Title: {title}" for note_id, title in results])
        else:
            response = "No notes found."
        view.post_response(response)

    def _handle_list(self, view):
        notes = self.data.list_all_note_ids()
        if notes:
            response = "All Notes:\n" + "\n".join([f"ID: {note_id}, Title: {title}" for note_id, title in notes])
        else:
            response = "No notes available."
        view.post_response(response)

class ConversationServiceCommand(Command):
    def __init__(self, librarian):
        self.librarian = librarian

    def name(self):
        return "conversation"

    def execute(self, view, desired_data: List):
        view.post_response("Conversation service in progress. Actions include 'trim', 'clear', 'delete', 'search', 'list', and 'back' to return to Clerk.")
        updated_convo = self._conversation_service_input(view, desired_data)
        if updated_convo is not None:
            desired_data.clear()
            desired_data.extend(updated_convo)

    def _conversation_service_input(self, view, convo: List):
        selection = view.get_service_input()
        if selection == "back":
            return convo
        elif selection == "trim":
            convo = self._handle_trim(view, convo)
        elif selection == "clear":
            convo = self._handle_clear(view, convo)
        elif selection == "save":
            self._handle_save(view, convo)
        elif selection == "load":
            convo = self._handle_load(view)
        elif selection == "delete":
            self._handle_delete(view)
        elif selection == "search":
            self._handle_search(view)
        elif selection == "list":
            self._handle_list(view)
        else:
            view.post_response("Invalid selection. Please choose a valid option.")

        if selection != "back":
            view.post_response("What would you like to do next with the Notes service? (trim, clear, save, load, delete, search, list, back)")
            return self._conversation_service_input(view, convo)

        return convo

    def _handle_trim(self, view, convo: List) -> List:
        if not convo:
            view.post_response("No conversation to trim.")
            return convo
        convo_length = len(convo)
        convo_content = "\n".join(message['content'] for message in convo)
        view.post_response(f"Current conversation length: {convo_length}\nConversation content:\n{convo_content}")
        view.post_response("Enter start index to trim below.")
        start_idx = int(view.get_service_input())
        view.post_response("Enter end index to trim below.")
        end_idx = int(view.get_service_input())

        if start_idx < 0 or end_idx > len(convo) or start_idx >= end_idx:
            view.post_response("Invalid indices. Please try again.")
            return convo

        trimmed_conversation = convo[start_idx:end_idx]
        view.post_response(f"Trimmed conversation: {trimmed_conversation}")
        return trimmed_conversation

    def _handle_clear(self, view, convo: List) -> List:
        view.post_response("Are you sure you want to clear the conversation? (yes/no): ")
        confirmation = view.get_service_input()
        if confirmation.lower() == "yes":
            view.post_response("Conversation cleared.")
            return []
        else:
            view.post_response("Clear operation cancelled.")
            return convo

    def _handle_save(self, view, convo: List):
        view.post_response("Enter title to save the conversation: ")
        title = view.get_service_input()
        self.librarian.save(convo, title)
        view.post_response(f"Conversation saved as {title}.")

    def _handle_load(self, view) -> List:
        view.post_response("Enter title to load the conversation: ")
        title = view.get_service_input()
        loaded_conversation = self.librarian.load(title)
        view.post_response(f"Conversation loaded: {loaded_conversation}")
        return loaded_conversation

    def _handle_delete(self, view):
        view.post_response("Enter title to delete the conversation: ")
        title = view.get_service_input()
        conv_path = os.path.join(self.librarian._conv_path, title + '.conv')
        try:
            os.remove(conv_path)
            view.post_response(f"Deleted conversation: {title}")
        except FileNotFoundError:
            view.post_response(f"Conversation {title} not found.")

    def _handle_search(self, view):
        view.post_response("Enter search query: ")
        query = view.get_service_input()
        results = self._search_conversations(query)
        if results:
            formatted_results = "\n".join([f"{name}: {snippet}" for name, snippet in results])
            view.post_response(f"Search results:\n{formatted_results}")
        else:
            view.post_response("No matching conversations found.")

    def _search_conversations(self, query: str) -> List[Tuple[str, str]]:
        matches = []
        conversations = self.librarian.list()
        for conv_name in conversations:
            conv_content = self.librarian.load(conv_name)
            for entry in conv_content:
                if isinstance(entry, dict) and 'content' in entry and query.lower() in entry['content'].lower():
                    snippet = entry['content']
                    matches.append((conv_name, snippet))
        return matches

    def _handle_list(self, view):
        conversations = self.librarian.list()
        view.post_logs(conversations)
