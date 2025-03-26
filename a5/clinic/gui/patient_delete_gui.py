import sys

from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtWidgets import QGridLayout
from clinic.dao.patient_dao_json import PatientDAOJSON
from PyQt6.QtCore import Qt, pyqtSignal


class PatientDeleteGui(QWidget):
    patient_deleted = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Patient Delete")

        self.resize(200, 100)

        layout = QGridLayout()
        self.setLayout(layout)


        label_phn = QLabel("PHN:")
        self.input_phn = QLineEdit()
        self.button_delete = QPushButton("Delete")

        self.input_phn.setInputMask("0000000000")

        layout.addWidget(label_phn, 0, 0)
        layout.addWidget(self.input_phn, 0, 1)
        layout.addWidget(self.button_delete, 1, 0)

        self.button_delete.clicked.connect(self.delete_button_clicked)

    def delete_button_clicked(self):
        '''Handles delete button'''
        phn = self.input_phn.text()  # Get the PHN from the input field
        patient_dao = PatientDAOJSON(autosave=True)
        
        # Search for the patient by PHN
        patient = patient_dao.search_patient(phn)

        if patient:
            # If the patient exists, delete them
            patient_dao.delete_patient(phn)
            QMessageBox.information(self, "Success", f"Patient with PHN {phn} has been deleted.")
            self.patient_deleted.emit()
            self.close()        
        else:
            # If the patient doesn't exist, show an error message
            QMessageBox.warning(self, "Error", f"No patient found with PHN {phn}.")        