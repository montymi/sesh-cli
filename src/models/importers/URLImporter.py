from langchain_community.document_loaders import SeleniumURLLoader

from models.importers.importer import Importer 

class URLImporter(Importer):
    def name(self):
        return 'url'

    def execute(self, path):
        try:
            return SeleniumURLLoader(urls=[path], browser='firefox', headless=True).load()
        except Exception:
            return []
