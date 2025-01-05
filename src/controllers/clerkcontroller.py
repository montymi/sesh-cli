from controllers.servicecontroller import ServiceController
from controllers.libcontroller import LibController
from models.clerk import Clerk

class ClerkController:
    def __init__(self, model: Clerk, view):
        self.view = view
        self.clerk = model
        self.sc = ServiceController(self.clerk, view)
        self.lc = LibController(self.clerk.librarian, view)
        self.entry = None
        self.response = None

    def handle_welcome(self):
        self.view.post_welcome(self.clerk.greeting())
        if self.lc.show_logs() == -1:
            return
        self.view.post_response("Would you like to continue a conversation? ENTER to start new conversation.")
        selection = self.view.get_service_input()
        self.lc.load_log(selection)
        return 1

    def handle_entry(self):
        prompt = self.view.get_entry() 
        if self.sc.execute(prompt, self.lc.logger) == -1:
            if prompt is None:
                return -1
            self.entry = { 'role': 'user', 'content': prompt }
        return 1

    def handle_response(self):
        if self.entry:
            answer = self.clerk.chat(self.entry, self.lc.logger)
            if answer:
                self.response = { 'role': 'assistant', 'content': answer }
                self.lc.update_log(self.response)
                self.view.post_response(answer)
                return 1
        return -1

    def handle_context(self):
        context = self.clerk.docs
        if context != []:
            self.view.post_context(context)

    def handle_save(self):
        self.view.post_response("Would you like to save the currently embedded documents? (y/N)")
        doc_selection = self.view.get_service_input()
        if doc_selection not in ['y', 'Y', 'yes', 'Yes', 'YES']:
            self.lc.reset_docs()
        self.view.post_save_request()
        selection = self.view.get_service_input()
        if selection in ['', 'N', 'n', 'No', 'no']:
            return -1
        self.view.post_response("What would you like to name the conversation? Default to datetime")
        title = self.view.get_service_input()
        self.lc.save_logs(title, self.user)
        return 1
