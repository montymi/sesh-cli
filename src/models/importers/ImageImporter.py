from langchain_community.document_loaders import UnstructuredImageLoader

from models.importers.importer import Importer


class ImageImporter(Importer):
    def name(self):
        return [".png",".jpg"]

    def execute(self, path):
        return UnstructuredImageLoader(path).load()
