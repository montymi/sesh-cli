from controllers.clerkcontroller import ClerkController
from langchain_ollama import OllamaEmbeddings
from langchain_openai import OpenAIEmbeddings
from models.app import App
from models.clerk import GPTClerk, OllamaClerk
from models.librarian import Librarian
from views.cli import CLI
import ollama
import os

class AppController:
    def __init__(self, args) -> None:
        self.model = App()
        self.view = self.__init__view__(args)
        self.model_result = self.__init__models__()
        self.cc = ClerkController(self.clerk, self.view)
 
    def __init__embedder__(self):
        if self.model.CLERK == "gpt":
            os.environ["OPENAI_API_KEY"] = self.model.OPENAI_API
            return OpenAIEmbeddings(model=self.model.LLM)
        return OllamaEmbeddings(model=self.model.LLM)
    
    def __init__librarian__(self):
        librarian = self.model.LIBRARIAN
        return Librarian(embedder=self.embedder, data_path=self.model.FILE_DATA_DIRECTORY)

    def __init__models__(self):
        clerk = self.model.CLERK # if statement after
        if clerk == "gpt":
            self.model.LLM = "text-embedding-ada-002"
            self.embedder = self.__init__embedder__()
            self.librarian = self.__init__librarian__()
            self.model.LLM = "gpt-4o"
            self.clerk = GPTClerk(model=self.model.LLM, librarian=self.librarian)
        else:
            try:
                available_models = ollama.list()
                model_names = [model['model'] for model in available_models['models']]
                self.view.post_models(model_names)
                llm = None
                if model_names:
                    llm = self.view.get_service_input()
                if not llm:
                    llm = self.model.LLM
                if llm not in model_names:
                    try:
                        ollama.pull(llm)
                    except Exception as e:
                        self.view.post_response(e)
                        self.model.LLM = model_names[0]
                self.model.LLM = llm
            except Exception as e:
                self.view.errors(e)
                return -1
            self.embedder = self.__init__embedder__()
            self.librarian = self.__init__librarian__()
            self.clerk = OllamaClerk(model=self.model.LLM, librarian=self.librarian)
        return 1

    def __init__view__(self, args):
        if args.ui:
            print("Starting application in CLI mode because UI is WIP...")
        elif args.cli:
            print("Starting application in CLI mode...")
        else:
            print("Starting application in CLI mode...")
        return CLI()

    def test(self):
        return self.model_result

    def setup(self):
        try:
            self.cc.handle_welcome()
        except KeyboardInterrupt:
            raise KeyboardInterrupt

    def loop(self):
        while True:    
            try:
                self.cc.handle_entry()
                self.cc.handle_response()
                self.cc.handle_context()
            except KeyboardInterrupt:
                self.cc.handle_save()
                raise KeyboardInterrupt

    def run(self):
        try:
            self.setup()
            self.loop()
        except KeyboardInterrupt:
            self.view.exit()
