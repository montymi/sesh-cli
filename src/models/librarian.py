from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from models.journal import Journal
from models.managers import ImporterManager
from datetime import datetime
from typing import Dict, List
import json
import os

class Librarian:
    def __init__(self, data_path, embedder) -> None:
        self.SESH_PATH = data_path
        self.__init__library__(data_path)
        self.journal = Journal(self._journal_path)
        self.importers = self.__init__importers__()
        self.splitter = self.__init__splitter__()
        self.embedder = embedder
        self.vector_store = Chroma(persist_directory=self._vector_path, embedding_function=self.embedder)
    
    def __init__library__(self, data_path):
        paths = []
        self._conv_path = data_path+'/resources/conversations/'
        self._vector_path = data_path+'/resources/vectors/'
        self._journal_path = data_path+'/resources/journal/'
        paths.append(self._conv_path)
        paths.append(self._vector_path)
        paths.append(self._journal_path)
        for path in paths:
            if not os.path.exists(path):
                os.makedirs(path)

    def __init__importers__(self):
        self._importer_path = 'models/importers/'
        importer_dict = {}
        importer_manager = ImporterManager(self._importer_path)
        try:
            for importer in importer_manager.discover_plugins():
                name = importer.name()
                if isinstance(name, list):
                    for ext in name:
                        importer_dict[ext] = importer
                else:
                    importer_dict[name] = importer
            return importer_dict
        except AttributeError as e:
            return e
    
    def __init__splitter__(self):
        return RecursiveCharacterTextSplitter(
            chunk_size=1024, chunk_overlap=80, length_function=len, is_separator_regex=False
        )

    def date(self):
        return datetime.now().strftime("%Y%m%d-%H%M%S")

    def export(self, data: List, path: str, name: str, note: str):
        try:
            os.mkdir(path)
        except FileExistsError:
            pass
        try:
            conversation_string = json.dumps(data)
            with open(path+"/"+name+'.conv', 'w') as file:
                file.write(conversation_string)
            if note != "":
                with open(path+'/note.txt', 'w') as file:
                    file.write(note)
            with open(path+"/"+name+'.txt', 'w') as file:
                for entry in data:
                    try:
                        role = entry['role'].upper()
                        content = entry['content']
                        file.write(f"<<{role}>>\n{content}\n\n")
                    except TypeError:
                        file.write(f"<<UNKNOWN>>\n{entry}\n\n")
            return 1
        except FileNotFoundError:
            pass
        return -1

    def save(self, conversation: List, title= None):
        if title == '':
            title = self.date()
        try:
            conversation_string = json.dumps(conversation)
            with open(self._conv_path+title+'.conv', 'w') as file:
                file.write(conversation_string)
        except FileNotFoundError:
            pass

    def _load(self, path: str) -> List:
        try:
            conv_file_path = os.path.join(path, f"{os.path.basename(path)}.conv")
            if os.path.isfile(conv_file_path):
                with open(conv_file_path, 'r') as file:
                    content_string = file.read()
                    return json.loads(content_string)
        except FileNotFoundError:
            pass
        return []

    def _load_note(self, path: str):
        try:
            note_file_path = os.path.join(path, "note.txt")
            if os.path.isfile(note_file_path):
                with open(note_file_path, 'r') as note_file:
                    return note_file.read()
        except FileNotFoundError:
            return None

    def load(self, title: str) -> List:
        try:
            with open(self._conv_path+title+'.conv', 'r') as file:
                content_string = file.read()
                return json.loads(content_string)
        except FileNotFoundError:
            return []

    def _remove_extension_(self, file):
        return file.split('.')[0]
    
    def list(self) -> List[str]:
        convos = os.listdir(self._conv_path)
        cleaned = []
        for file in convos:
            clean = self._remove_extension_(file)
            cleaned.append(clean)
        return cleaned

    def split(self, docs):
        return self.splitter.split_documents(docs)

    def embed(self, chunks):
        self.vector_store.add_documents(chunks)
    
    def similarity_search(self, query: str, num_docs: int=4) -> List[Document]:
        max_docs = self.vector_store._collection.count() # get doc count
        k = min(num_docs, max_docs) # find min value between doc count and num_docs var
        
        return self.vector_store.similarity_search(query, k=k) # Perform the similarity search with the adjusted k

    def format_context(self, docs: List[Document]) -> str:
        return "\n\n".join(doc.page_content for doc in docs)

    def get_template(self):
        return "Using the above context, answer the following prompt to the best of your ability:\n"

    def clear_embeddings(self):
        self.vector_store.delete_collection()
