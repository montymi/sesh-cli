from langchain_community.document_loaders import PythonLoader

from models.importers.importer import Importer


class PythonImporter(Importer):
    def name(self):
        return ".py"

    def execute(self, path):
        return PythonLoader(path).load()
