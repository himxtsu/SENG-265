from PyQt6.QtCore import QObject, pyqtSignal

class PatientManager(QObject):
    # Define signals for different operations
    patients_updated = pyqtSignal(list)  # Emitted when the patient list changes

    def __init__(self):
        super().__init__()
        self.patients = []  # This should be loaded from your data source initially

    def load_patients(self, patient_list):
        self.patients = patient_list
        self.patients_updated.emit(self.patients)

    def add_patient(self, new_patient):
        self.patients.append(new_patient)
        self.patients_updated.emit(self.patients)

    def delete_patient(self, patient_phn):
        self.patients = [p for p in self.patients if p.phn != patient_phn]
        self.patients_updated.emit(self.patients)

    def update_patient(self, updated_patient):
        for idx, patient in enumerate(self.patients):
            if patient.phn == updated_patient.phn:
                self.patients[idx] = updated_patient
                break
        self.patients_updated.emit(self.patients)

    def search_patient(self, keyword):
        result = [p for p in self.patients if keyword.lower() in p.name.lower()]
        self.patients_updated.emit(result)
    