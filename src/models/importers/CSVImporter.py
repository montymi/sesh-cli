from langchain_community.document_loaders.csv_loader import CSVLoader

from models.importers.importer import Importer


class CSVImporter(Importer):
    def name(self):
        return ".csv"

    def execute(self, path):
        return CSVLoader(file_path=path).load()
