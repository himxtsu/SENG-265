from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtWidgets import QGridLayout
from clinic.dao.patient_dao_json import PatientDAOJSON
from clinic.patient import Patient

class PatientUpdateSearchGui(QWidget):
# This class will handle finding the gui that pops up to input a users phn or name. It will then
# pass the patient and a signal to the main gui which will cause the actual patient update
# gui to launch.
    patient_found = pyqtSignal(Patient)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Patient Search")

        self.resize(200, 100)

        layout = QGridLayout()
        self.setLayout(layout)


        # Button and text box creation
        label_phn = QLabel("PHN:")
        self.input_phn = QLineEdit()
        self.button_search = QPushButton("Search")

        # Mask to prevent abnormal long phn
        self.input_phn.setInputMask("0000000000")

        layout.addWidget(label_phn, 0, 0)
        layout.addWidget(self.input_phn, 0, 1)
        layout.addWidget(self.button_search, 1, 0)

        # Connect button to function
        self.button_search.clicked.connect(self.search_button_clicked)

        self.result_label = QLabel("")
        layout.addWidget(self.result_label, 2, 0, 1, 2)

    def search_button_clicked(self):
    # Handles search button.

        phn = self.input_phn.text()

        # Create patient dao instance
        patient_dao = PatientDAOJSON(autosave = True)
        patient = patient_dao.search_patient(phn)

        if patient is None:
        # If no patient is found, do nothing.
            self.result_label.setText("Patient not found.")
        else:
        # If patient is found, emit a signal to main clinic gui and pass said patient.
            self.patient_found.emit(patient)