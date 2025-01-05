from langchain_community.document_loaders import DirectoryLoader, UnstructuredFileLoader

from models.importers.importer import Importer


class RecursiveDirectoryImporter(Importer):
    def name(self):
        return "recursive_directory"

    def execute(self, path):
        return DirectoryLoader(
                path,
                glob="**/*",
                use_multithreading=True,
                show_progress=True,
                loader_cls=UnstructuredFileLoader).load()
