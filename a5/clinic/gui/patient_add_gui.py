import sys
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableView, \
    QVBoxLayout, QPushButton, QPlainTextEdit, QWidget, QHBoxLayout, \
    QDialog, QGridLayout, QLabel, QLineEdit, QMessageBox
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from clinic.dao.patient_dao_json import PatientDAOJSON
from clinic.dao.note_dao_pickle import NoteDAOPickle
from clinic.patient import Patient
from clinic.controller import Controller

class PatientAddGui(QWidget):
    patient_added = pyqtSignal()
    patient_saved = pyqtSignal()
    def __init__(self):
        super().__init__()


        self.setWindowTitle("Patient Info Page")
        self.resize(300, 200)

        self.layout = QGridLayout()
        self.setLayout(self.layout)

        label_phn = QLabel("Personal Health Number")
        label_name = QLabel("First name Last name")
        label_birthday = QLabel("Birthday (YYYY-MM-DD)")
        label_phone = QLabel("Phone Number (XXX-XXX-XXXX)")
        label_email = QLabel("Email Address")
        label_address = QLabel("Home Address")
        
        # Text box creation.
        self.input_phn = QLineEdit()
        self.input_name = QLineEdit()
        self.input_birthday = QLineEdit()
        self.input_phone = QLineEdit()
        self.input_email = QLineEdit()
        self.input_address = QLineEdit()

        #Button creation.
        self.button_add = QPushButton("Add")
        self.button_clear = QPushButton("Clear")
        self.button_update = QPushButton("Update")

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

        self.layout.addWidget(self.button_add, 6, 0)
        self.layout.addWidget(self.button_clear, 6, 1)

        #Mask for abnormal input
        self.input_phn.setInputMask("0000000000")
        self.input_phone.setInputMask("000-000-0000")
        self.input_birthday.setInputMask("0000-00-00")
        
        self.button_add.setEnabled(False)

        # Connect buttons to functions
        self.button_clear.clicked.connect(self.clear_button_clicked)
        self.button_add.clicked.connect(self.add_button_clicked)

        # Loops over all text boxes, checking that they have all been modified.
        # If they have then we can enable add button
        for field in [self.input_phn, self.input_name, self.input_birthday,
                      self.input_phone, self.input_email, self.input_address]:
            field.textChanged.connect(self.check_form_completion)

        # Patient dao instance
        self.patient_dao = PatientDAOJSON(autosave=True)        
        
    def clear_button_clicked(self):
    # Handle clear button


        # Loop over all text boxes and clear their input, set add button to disabled
        for field in [self.input_phn, self.input_name, self.input_birthday,
                      self.input_phone, self.input_email, self.input_address]:
            field.clear()
        self.button_add.setEnabled(False)        


    def check_form_completion(self):
    # Handles checking if form is complete

        # Connected to loop in init, if all are filled then we can enable button
        all_filled = all(field.text().strip() for field in [self.input_phn, self.input_name,
                                                            self.input_birthday, self.input_phone,
                                                            self.input_email, self.input_address])
        self.button_add.setEnabled(all_filled)


    def add_button_clicked(self):
    # Handles add button.

        # Cleans user input.
        phn = self.input_phn.text().strip()
        name = self.input_name.text().strip()
        birthday = self.input_birthday.text().strip()
        phone = self.input_phone.text().strip()
        email = self.input_email.text().strip()
        address = self.input_address.text().strip()

        # Create a new patient object
        new_patient = Patient(phn, name, birthday, phone, email, address)

        # Add the patient to the data store using DAO
        try:
            self.patient_dao.create_patient(new_patient)
            QMessageBox.information(self, "Success", "Patient added successfully!")
            self.clear_button_clicked()  # Clear form after successful addition

            #Emit to main gui to refresh patient list.
            self.patient_added.emit()
            self.patient_saved.emit()
            self.close()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to add patient: {str(e)}")        

