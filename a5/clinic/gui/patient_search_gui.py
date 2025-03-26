import sys

from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtWidgets import QGridLayout
from clinic.dao.patient_dao_json import PatientDAOJSON
from clinic.patient import Patient

class PatientSearchGui(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Patient Search")

        self.resize(300, 100)

        layout = QGridLayout()
        self.setLayout(layout)

        # Phn search box and button
        label_phn = QLabel("PHN:")
        self.input_phn = QLineEdit()
        self.button_search_phn = QPushButton("Search PHN")

        # Name search box and button
        label_name = QLabel("Name:")
        self.input_name = QLineEdit()
        self.button_search_name = QPushButton("Search Name")

        # Phn input mask
        self.input_phn.setInputMask("0000000000")

        layout.addWidget(label_phn, 0, 0)
        layout.addWidget(self.input_phn, 0, 1)
        layout.addWidget(self.button_search_phn, 0, 2)
        layout.addWidget(label_name, 1, 0)
        layout.addWidget(self.input_name, 1, 1)
        layout.addWidget(self.button_search_name, 1, 2)
        
        # Connect buttons to fuinctions.
        self.button_search_phn.clicked.connect(self.search_button_phn_clicked)
        self.button_search_name.clicked.connect(self.search_button_name_clicked)

        self.result_label = QLabel("")
        layout.addWidget(self.result_label, 2, 0, 1, 2)

    def search_button_phn_clicked(self):
    # Handle phn search button.

        phn = self.input_phn.text()

        # Create patient dao instance, set patient to input phn
        patient_dao = PatientDAOJSON(autosave = True)
        patient = patient_dao.search_patient(phn)

        if patient is None:
        # No Patient found
            self.result_label.setText("Patient not found.")
        else:
            #Display patient info
            patient_info = (f"PHN: {patient.phn}\n"
                            f"Name: {patient.name}\n"
                            f"Birthday: {patient.birth_date}\n"
                            f"Phone: {patient.phone}\n"
                            f"Email: {patient.email}\n"
                            f"Address: {patient.address}\n")
            self.result_label.setText(patient_info)

    def search_button_name_clicked(self):
    # Handle name search button.
        name = self.input_name.text().strip().lower()

        if not name:
            self.result_label.setText("Please enter a name to search.")
            return

        # Create patient DAO instance
        patient_dao = PatientDAOJSON(autosave=True)
        all_patients = patient_dao.load_patients()  # Load all patients from the DAO

        # Filter patients by name (case-insensitive partial match)
        matching_patients = [
            patient for patient in all_patients if name in patient.name.lower()
        ]

        if not matching_patients:
            self.result_label.setText("No patients found with that name.")
        else:
            # Display matching patient info
            result_text = "Matching Patients:\n\n"
            for patient in matching_patients:
                result_text += (f"PHN: {patient.phn}\n"
                                f"Name: {patient.name}\n"
                                f"Birthday: {patient.birth_date}\n"
                                f"Phone: {patient.phone}\n"
                                f"Email: {patient.email}\n"
                                f"Address: {patient.address}\n\n")
            self.result_label.setText(result_text)