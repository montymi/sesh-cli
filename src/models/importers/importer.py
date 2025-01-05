from abc import abstractmethod
from typing import List
from langchain_core.documents import Document

class Importer:
    def __init__(self, data=None):
        self.data = data

    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def execute(self, path) -> List[Document]:
        pass
