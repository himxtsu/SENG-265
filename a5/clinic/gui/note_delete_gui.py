from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPlainTextEdit, QPushButton, QHBoxLayout, QLineEdit, QMessageBox
from clinic.dao.note_dao_pickle import NoteDAOPickle

class NoteDelete(QDialog):
    def __init__(self, patient):
        super().__init__()

        # Generic ui setup parameters, adding buttons, labels, and textboxes.
        self.patient = patient

        self.setWindowTitle("Delete Note")
        self.resize(150, 100)

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.label = QLabel("Input Note Code to Delete")
        layout.addWidget(self.label)

        # Text input for the note.
        self.note_code = QLineEdit()
        layout.addWidget(self.note_code)

        # Button creation.
        button_layout = QHBoxLayout()
        self.delete_button = QPushButton("Submit")
        button_layout.addWidget(self.delete_button)
        layout.addLayout(button_layout)

        #Connects the button to the delete function itself
        self.delete_button.clicked.connect(self.button_delete)   

        self.setLayout(layout)

    def button_delete(self):
    #Handles deleting the specified note    

        #Attempts to make an instance of the noteDAO to use its functions, takes the int typed by the
        #user, then tries to delete it
        try:
            note_dao = NoteDAOPickle(self.patient.phn, autosave = True)
            note_code = int(self.note_code.text())
            note_dao.delete_note_by_code(note_code)

        #If above fails, either we are missing the note code or it was an incorrect code
        except:
            QMessageBox.critical(self, "Error", "Invalid/Missing Note Code")
        self.close()