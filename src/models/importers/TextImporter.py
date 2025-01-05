from langchain_community.document_loaders import TextLoader

from models.importers.importer import Importer


class TextImporter(Importer):
    def name(self):
        return ".txt"

    def execute(self, path):
        return TextLoader(path).load()
