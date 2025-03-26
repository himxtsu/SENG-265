from clinic.note import Note
from datetime import datetime
from typing import List
import pickle

class NoteDAOPickle:
    def __init__(self, phn, autosave):

        #Uses phn of each patient for the file name
        self.filename = f'clinic/records/{phn}.dat'

        # Attempt to load nodes using load_notes() function, also works if autosave enabled
        try:
            self.notes = self.load_notes()

            # If there exists notes when we use load, get the counter and add 1 to it
            if self.notes:
                self.counter = max(note.get_note_code() for note in self.notes) + 1
            # If no notes exist, set counter to 1 to start
            else:
                self.counter = 1
        # Runs if no note to load or autosave is disabled
        except:
            self.notes = []
            self.counter = 1


    # Opens pickle .dat file that contains all of patients notes
    def load_notes(self):
        notes = []

        with open(self.filename, 'rb') as file:
            notes = pickle.load(file)

        return notes


    # Saves all the patients notes and dumps them into a pickle file
    def save_notes(self):

        with open(self.filename, 'wb') as file:
            pickle.dump(self.notes, file)


    # Create a new note and add it to the notes list
    def create_note(self, text: str) -> Note:
        note = Note(self.counter, text)
        self.notes.append(note)
        self.counter += 1

        self.save_notes()
        return note


    # Return all notes
    def read_all_notes(self) -> List[Note]:
        return self.notes


    # Find and return a note by its code
    def read_note_by_code(self, code: int) -> Note:
        for note in self.notes:
            if note.get_note_code() == code:
                return note
        return None


    # Find and return notes containing the given text
    def read_notes_by_text(self, text: str) -> List[Note]:
        return [note for note in self.notes if text in note.get_note_text()]


    # Update the text of a note by its code
    def update_note_by_code(self, code: int, text: str) -> Note:
        note = self.read_note_by_code(code)
        if note:
            note.text = text
            note.update_time()
            self.save_notes()
        return note


    # Delete a note by its code
    def delete_note_by_code(self, code: int) -> bool:
        original_length = len(self.notes)
        self.notes = [note for note in self.notes if note.get_note_code() != code]
        self.save_notes()
        return len(self.notes) < original_length
