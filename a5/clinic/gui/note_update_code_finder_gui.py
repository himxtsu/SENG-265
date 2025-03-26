from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPlainTextEdit, QPushButton, QHBoxLayout, QLineEdit, QMessageBox
from PyQt6.QtCore import pyqtSignal
from clinic.dao.note_dao_pickle import NoteDAOPickle
from clinic.note import Note

class NoteUpdateSearch(QDialog):
# This class handles the popup dialouge that the user inputs to specify which
# note they want to edit. Once the user has submitted a correct note number,
# the actual note update class will be used.

    # Signal
    note_found = pyqtSignal(Note)

    def __init__(self, patient):
        super().__init__()

        self.patient = patient

        self.setWindowTitle("Retrieve Note")
        self.resize(150, 100)

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.label = QLabel("Input Note Code to Retrieve")
        layout.addWidget(self.label)

        # Text input for the note.
        self.note_code = QLineEdit()
        layout.addWidget(self.note_code)

        # Button.
        button_layout = QHBoxLayout()
        self.retrieve_button = QPushButton("Fetch")
        button_layout.addWidget(self.retrieve_button)
        layout.addLayout(button_layout)

        # Connect to function.
        self.retrieve_button.clicked.connect(self.button_retrieve)   

        self.setLayout(layout)

    def button_retrieve(self):
    #Handles button press

        # Create note DAO instance, gather number code input in text box,
        # Use said code to find specific note, then emit signal and the note
        # That was found back to the main function.
        try:
            note_dao = NoteDAOPickle(self.patient.phn, autosave = True)
            note_code = int(self.note_code.text())
            note_fetched = note_dao.read_note_by_code(note_code)
            self.note_found.emit(note_fetched)
        except:
        # If above fails, signal an error to the user with a popup.
            QMessageBox.critical(self, "Error", "Invalid/Missing Note Code")
        self.close()