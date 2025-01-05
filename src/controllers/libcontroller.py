from typing import List
import os

from models.librarian import Librarian

class LibController:
    def __init__(self, model: Librarian, view):
        self.librarian = model
        self.view = view
        self.logger = []
 
    def show_logs(self):
        convos = self.librarian.list()
        if convos:
            self.view.post_logs(convos)
            return 1
        else: return -1

    def load_log(self, title):
        if title not in self.librarian.list() and os.path.isdir(title):
            self.logger = self.librarian._load(title)
            note = self.librarian._load_note(title)
            if note:
                self.view.post_response(note)
        else:
            loaded_log = self.librarian.load(title)
            self.logger = loaded_log if loaded_log is not None else []

    def load_logs(self) -> List:
        return [self.librarian.load(convo) for convo in self.librarian.list()]

    def save_logs(self, title, user):
        conversations = self.logger
        self.librarian.save(conversations, title, user)

    def update_log(self, response):
        self.logger.append(response)

    def reset_docs(self):
        self.librarian.clear_embeddings()
