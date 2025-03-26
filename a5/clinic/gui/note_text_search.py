from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPlainTextEdit, QPushButton, QHBoxLayout, QLineEdit, QMessageBox
from PyQt6.QtCore import pyqtSignal
from clinic.dao.note_dao_pickle import NoteDAOPickle
from clinic.note import Note

class NoteTextSearch(QDialog):

    # Signal
    note_search = pyqtSignal(list)

    def __init__(self, patient):
        super().__init__()

        self.patient = patient

        self.setWindowTitle("Search Notes")
        self.resize(150, 100)

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.label = QLabel("Input Text to Search")
        layout.addWidget(self.label)

        # Text box.
        self.note_text = QLineEdit()
        layout.addWidget(self.note_text)

        # Button.
        button_layout = QHBoxLayout()
        self.retrieve_button = QPushButton("Fetch")
        button_layout.addWidget(self.retrieve_button)
        layout.addLayout(button_layout)

        # Connect to function.
        self.retrieve_button.clicked.connect(self.button_retrieve)   

        self.setLayout(layout)


    def button_retrieve(self):
    # Handles button press.

        # Try to make note dao instance, use note text match function, then emit a signal and variable to the
        # main gui that we have matches.
        try:
            note_dao = NoteDAOPickle(self.patient.phn, autosave = True)
            note_matches = note_dao.read_notes_by_text(self.note_text.text())
            self.note_search.emit(note_matches)
        except:
        # If above fails, create a popup that alerts user.
            QMessageBox.critical(self, "Error", "Invalid/Missing Note Text")
        self.close()