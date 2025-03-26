from clinic.patient import *
from clinic.note import *
from typing import List
from datetime import *
from clinic.dao.note_dao_pickle import NoteDAOPickle

class PatientRecord:
    def __init__(self, phn, autosave):
        self.note_dao = NoteDAOPickle(phn, autosave)


    def add_note(self, text: str) -> None:
        # Add a new Note to the records list.

        return self.note_dao.create_note(text)


    def get_notes(self) -> List[Note]:
        # Return the list of Notes.

        return self.note_dao.read_all_notes()


    def find_note_by_code(self, code: int) -> Note:
        # Find a note by its code and return it.

        return self.note_dao.read_note_by_code(code)
    

    def retrieve_notes(self, text):
    # Retrieve notes from created instances using provided text.

        return self.note_dao.read_notes_by_text(text)        
    

    def update_note(self, code, text):
    # Retrieve note by code and update contents

        return self.note_dao.update_note_by_code(code, text)
    

    def delete_note(self, code):
        # Create new list of notes excluding note that is slated for deletion

        return self.note_dao.delete_note_by_code(code)
    

    def list_notes(self):
        # Return patients note list

        return list(reversed(self.note_dao.read_all_notes()))