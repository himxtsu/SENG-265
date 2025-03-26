from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPlainTextEdit, QPushButton, QHBoxLayout
from clinic.dao.note_dao_pickle import NoteDAOPickle

class NoteInput(QDialog):
    def __init__(self, patient):
        super().__init__()

        self.patient = patient

        self.setWindowTitle("Add Note")
        self.resize(400, 300)

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.label = QLabel("Enter the patient's note below:")
        layout.addWidget(self.label)

        # Text input for the note.
        self.note_input = QPlainTextEdit()
        self.note_input.setPlaceholderText("Type the note here...")
        layout.addWidget(self.note_input)

        # Buttons for Submit and Cancel.
        button_layout = QHBoxLayout()
        self.submit_button = QPushButton("Submit")
        button_layout.addWidget(self.submit_button)

        layout.addLayout(button_layout)

        # Connect button signals.
        self.submit_button.clicked.connect(self.button_submit)  

        self.setLayout(layout)

    def button_submit(self):
        #Handles when submit button pressed.

        #Creates a note dao instance, takes the text from the text box, then sends the text to note dao to create a note.
        note_dao = NoteDAOPickle(self.patient.phn, autosave = True)
        note_text = self.note_input.toPlainText()
        note_dao.create_note(note_text)
        self.close()
