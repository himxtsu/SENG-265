from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPlainTextEdit, QPushButton, QHBoxLayout
from clinic.dao.note_dao_pickle import NoteDAOPickle

class NoteUpdate(QDialog):
# This is the actual note update class. Using the info from the search for note updatre class,
# we will update the desired note.

    def __init__(self, patient, note):
        super().__init__()

        self.patient = patient
        self.note = note

        self.setWindowTitle("Add Note")
        self.resize(400, 300)

        layout = QVBoxLayout()
        self.setLayout(layout)

        
        self.label = QLabel("Enter the patient's note below:")
        layout.addWidget(self.label)

        # Text input for the note.
        self.note_input = QPlainTextEdit()
        layout.addWidget(self.note_input)

        # Button for Submit.
        button_layout = QHBoxLayout()
        self.submit_button = QPushButton("Submit")
        button_layout.addWidget(self.submit_button)
        layout.addLayout(button_layout)

        # Connect button signal.
        self.submit_button.clicked.connect(self.button_submit)   

        self.setLayout(layout)

        # This chunk presets the notes textbox with the contents of the note that is
        # going to be updated by the user. A Little bit of formatting is done to avoid,
        # some strange bugs.
        self.note_dao = NoteDAOPickle(self.patient.phn, autosave = True)
        note_text = str(self.note_dao.read_note_by_code(note.code))
        note_text = note_text[2:]
        self.note_input.setPlainText(str(note_text))


    def button_submit(self):
    # Handles button press.

        # Takes the text that the user maniuplates, passes it to the note dao made earlier
        # then closes.
        updated_text = self.note_input.toPlainText()
        self.note_dao.update_note_by_code(self.note.code, updated_text)
        self.close()


        