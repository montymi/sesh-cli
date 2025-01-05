import os
import json
from whoosh import index
from whoosh.fields import Schema, TEXT, ID
from whoosh.qparser import QueryParser

class Journal:
    def __init__(self, notes_directory: str):
        self.notes_directory = notes_directory
        if not os.path.exists(notes_directory):
            os.makedirs(notes_directory)
        
        # Create schema and index directory for Whoosh
        self.index_directory = os.path.join(notes_directory, 'index')
        if not os.path.exists(self.index_directory):
            os.makedirs(self.index_directory)

        self.schema = Schema(title=TEXT(stored=True), content=TEXT(stored=True), note_id=ID(stored=True))
        if not index.exists_in(self.index_directory):
            self.ix = index.create_in(self.index_directory, self.schema)
        else:
            self.ix = index.open_dir(self.index_directory)

    def _get_note_path(self, note_id: str):
        return os.path.join(self.notes_directory, f'{note_id}.json')

    def create_note(self, title: str, content: str):
        note_id = str(len(os.listdir(self.notes_directory)) + 1)
        note_path = self._get_note_path(note_id)
        
        note_data = {
            'note_id': note_id,
            'title': title,
            'content': content
        }
        with open(note_path, 'w') as f:
            json.dump(note_data, f)

        # Index the new note
        writer = self.ix.writer()
        writer.add_document(title=title, content=content, note_id=note_id)
        writer.commit()

        return note_id

    def read_note(self, note_id: str):
        note_path = self._get_note_path(note_id)
        if os.path.exists(note_path):
            with open(note_path, 'r') as f:
                note = json.load(f)
            return note['content']
        else:
            raise ValueError("Note not found")

    def update_note(self, note_id: str, new_content: str):
        note_path = self._get_note_path(note_id)
        if os.path.exists(note_path):
            with open(note_path, 'r') as f:
                note = json.load(f)
            
            note['content'] = new_content
            
            with open(note_path, 'w') as f:
                json.dump(note, f)

            # Update the index
            writer = self.ix.writer()
            writer.update_document(title=note['title'], content=new_content, note_id=note_id)
            writer.commit()
        else:
            raise ValueError("Note not found")

    def delete_note(self, note_id: str):
        note_path = self._get_note_path(note_id)
        if os.path.exists(note_path):
            os.remove(note_path)

            # Delete from the index
            writer = self.ix.writer()
            writer.delete_by_term('note_id', note_id)
            writer.commit()
        else:
            raise ValueError("Note not found")

    def search_notes(self, keyword: str):
        search_results = []
        with self.ix.searcher() as searcher:
            query = QueryParser("content", self.ix.schema).parse(keyword)
            results = searcher.search(query)
            for result in results:
                search_results.append((result['note_id'], result['title']))
        return search_results

    def list_all_note_ids(self):
        note_ids = []
        for filename in os.listdir(self.notes_directory):
            if filename.endswith('.json'):
                note_id = filename.split('.')[0]
                note_ids.append((note_id, self.read_note(note_id)))
        return note_ids

