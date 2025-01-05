from langchain_community.document_loaders import PyPDFLoader

from models.importers.importer import Importer


class PDFImporter(Importer):
    def name(self):
        return ".pdf"

    def execute(self, path):
        return PyPDFLoader(path).load()
