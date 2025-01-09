from models.habits import Habits
from models.librarian import Librarian
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI


class Clerk:
    def __init__(self, model: str, librarian: Librarian, llm, api=None):
        self.model = model
        self.llm = llm
        self.api = api
        self.librarian = librarian
        self.habits = Habits(self.librarian.SESH_PATH)
        self.clock_in = self.librarian.date()
        self.docs = []

    def greeting(self):
        return (f"Welcome!\n"
                f"        (o_  Current Model: {self.model}\n"
                f"  c_  \\\\\_\  Clock-In Time: {self.clock_in}\n"
                f"\\\)   <____) Habits: {', '.join([habit for habit in self.habits.active()])}\n")

    def chat(self, prompt: dict, history=[]):
        try:
            self.docs = self.librarian.similarity_search(prompt['content'])
            context = self.librarian.format_context(self.docs)
            template = self.librarian.get_template()
            query = prompt['content'] + ''.join(self.habits.load())
            prompt['content'] = context + template + query

            history.append(prompt)
            response = self.llm.invoke(history)
            return response.content
        except Exception as e:
            return e

class OllamaClerk(Clerk):
    def __init__(self, model: str, librarian: Librarian, api=None):
        super().__init__(model, librarian, ChatOllama(model=model), api)

class GPTClerk(Clerk):
    def __init__(self, model: str, librarian: Librarian, api=None):
        super().__init__(model, 
                         librarian, 
                         ChatOpenAI(
                            model="gpt-4o-mini",
                            temperature=0,
                            max_tokens=None,
                            timeout=None,
                            max_retries=2),
                        api)

