from langchain_community.document_loaders import Docx2txtLoader

from models.importers.importer import Importer


class DocxImporter(Importer):
    def name(self):
        return ".docx"

    def execute(self, path):
        return Docx2txtLoader(path).load()
