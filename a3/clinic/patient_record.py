from clinic.patient import *
from clinic.note import *
from typing import List
from datetime import *

class PatientRecord:
    def __init__(self):
        self.record_counter = 1
        self.records: List[Note] = []


    def add_note(self, text: str) -> None:
        # Add a new Note to the records list.

        # Create note, append it to note list of patient, and increment the code counter
        note = Note(self.record_counter, text)
        self.records.append(note)
        self.record_counter += 1

        return note


    def get_notes(self) -> List[Note]:
        # Return the list of Notes.

        return self.records


    def find_note_by_code(self, code: int) -> Note:
        # Find a note by its code and return it.

        # Search for desired note using its code and return note.
        for note in self.records:
            if note.get_note_code() == code:
                return note
        return 
    

    def retrieve_notes(self, text):
    # Retrieve notes from created instances using provided text.

        # Create list of potential matches by checking all note instances.
        text_matches = [
            note
            for note in self.records
            if text in note.get_note_text()
        ]
        
        return text_matches
    

    def update_note(self, code, text):
    # Retrieve note by code and update contents

        # Check note length.
        if len(self.records) < 1:
            return
        
        note_to_update = self.find_note_by_code(code)

        # Make sure we have note to update.
        if note_to_update is None:
            return None

        # Change the notes attributes.
        note_to_update.text = text
        note_to_update.update_time()

        return note_to_update
    

    def delete_note(self, code):
        # Create new list of notes excluding note that is slated for deletion

        if len(self.records) < 1:
            return

        # Generate new list by cyling though previous list but not including the note slated for deletion
        self.records = [
            note
            for note in self.records
            if note.get_note_code() != code
        ]

        return True
    

    def list_notes(self):
        # Return patients note list

        return list(reversed(self.records))