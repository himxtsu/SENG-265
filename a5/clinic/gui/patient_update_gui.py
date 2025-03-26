import sys
from PyQt6.QtCore import Qt
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableView, \
    QVBoxLayout, QPushButton, QPlainTextEdit, QWidget, QHBoxLayout, \
    QDialog, QGridLayout, QLabel, QLineEdit, QMessageBox
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from clinic.dao.patient_dao_json import PatientDAOJSON
from clinic.dao.note_dao_pickle import NoteDAOPickle
from clinic.patient import Patient
from clinic.controller import Controller

class PatientUpdateGui(QWidget):
# Takes the found patient from its helper function and will actually update the
# patients info in the database. 
    patient_updated = pyqtSignal()  

    def __init__(self, patient):
        super().__init__()

        self.patient = patient

        self.setWindowTitle("Patient Info Page")
        self.resize(300, 200)

        self.layout = QGridLayout()
        self.setLayout(self.layout)

        # Text box creation.
        label_phn = QLabel("Personal Health Number")
        label_name = QLabel("First name Last name")
        label_birthday = QLabel("Birthday (YYYY-MM-DD)")
        label_phone = QLabel("Phone Number (XXX-XXX-XXXX)")
        label_email = QLabel("Email Address")
        label_address = QLabel("Home Address")
        self.input_phn = QLineEdit()
        self.input_name = QLineEdit()
        self.input_birthday = QLineEdit()
        self.input_phone = QLineEdit()
        self.input_email = QLineEdit()
        self.input_address = QLineEdit()

        # Button creation.
        self.button_update = QPushButton("Update")

        # Placement.
        self.layout.addWidget(label_phn, 0, 0)
        self.layout.addWidget(label_name, 1, 0)
        self.layout.addWidget(label_birthday, 2, 0)
        self.layout.addWidget(label_phone, 3, 0)
        self.layout.addWidget(label_email, 4, 0)
        self.layout.addWidget(label_address, 5, 0)

        self.layout.addWidget(self.input_phn, 0, 1)
        self.layout.addWidget(self.input_name, 1, 1)
        self.layout.addWidget(self.input_birthday, 2, 1)
        self.layout.addWidget(self.input_phone, 3, 1)
        self.layout.addWidget(self.input_email, 4, 1)
        self.layout.addWidget(self.input_address, 5, 1)


        self.layout.addWidget(self.button_update, 6, 0)


        # Connect to function.
        self.button_update.clicked.connect(self.update_button_clicked)


        # Preset text boxes with patients current info.
        self.input_phn.setText(patient.phn)
        self.input_name.setText(patient.name)
        self.input_birthday.setText(patient.birth_date)
        self.input_phone.setText(patient.phone)
        self.input_email.setText(patient.email)
        self.input_address.setText(patient.address)

        # Masks to prevent abnormal input.
        self.input_phn.setInputMask("0000000000")
        self.input_phone.setInputMask("000-000-0000")
        self.input_birthday.setInputMask("0000-00-00")

        # Alert box formatting.
        self.error_label = QLabel("")
        self.error_label.setStyleSheet("color: red;")
        self.layout.addWidget(self.error_label)
        
        self.button_update.setEnabled(True)

    def update_button_clicked(self):
    # Handles button press.  
        
        # Stores text that user input from all fields
        phn = self.input_phn.text()
        name = self.input_name.text()
        birth_date = self.input_birthday.text()
        phone = self.input_phone.text()
        email = self.input_email.text()
        address = self.input_address.text()

        # Check if either name or phn is empty so that patient is always findable.
        if not self.input_phn.text().strip() or not self.input_name.text().strip():
            QMessageBox.critical(self, "Error", "Missing Info")
            return

        # Patient dao instnace
        patient_dao = PatientDAOJSON(autosave = True)

        
        if self.patient.phn != self.input_phn.text():
        # Edge case for if the patient PHN is changing.   

            try:
            # Using our already made functions, we quickly try to create then delete a patient
            # so that we can tell if that phn is already used. If it works, leave our flag false.
                patient_dao.create_patient(Patient(phn, name, birth_date, phone, email, address))
                patient_dao.delete_patient(phn)
                update_flag = False

            except: 
            # If above fails then we know that the phn that patient is trying to change to
            # is already in use. Update flag to prevent any patient info updating.
                QMessageBox.critical(self, "Error", "PHN Already Exists")
                update_flag = True
                
            if not update_flag:
            # If flag is false, go ahead and pass patient dao update what it needs and emite signal back to main
            # To refresh list of patients.
                patient_dao.update_patient(self.patient.phn, Patient(phn, name, birth_date, phone, email, address))
                self.patient_updated.emit()
                self.close()

        else:
        # Go ahead and pass patient dao update what it needs and emite signal back to main
        # To refresh list of patients.    
            patient_dao.update_patient(self.patient.phn, Patient(phn, name, birth_date, phone, email, address))
            self.patient_updated.emit()
            self.close()






