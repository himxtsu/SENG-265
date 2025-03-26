from clinic.patient import Patient
from typing import List, Optional
from clinic.dao.patient_decoder import PatientDecoder
from clinic.dao.patient_encoder import PatientEncoder
from json import loads, dumps


class PatientDAOJSON:

    # Initialize the internal storage for patients
    def __init__(self, autosave) -> None:
        self.autosave = autosave
        self.filename = 'clinic/patients.json'

        try:
            self.patients = self.load_patients()
        except:
            self.patients: List[Patient] = []


    # Open file containing json patient info, decode it, create list of patients, return
    def load_patients(self):
        patients = []

        # Loop through said patient info in json file and append patients to list
        with open(self.filename, 'r') as file:
            for patient_json in file:
                patient = loads(patient_json, cls=PatientDecoder)
                patients.append(patient)
        return patients


    # Save any changes that were made to patients to a json file
    def save_patients(self):

        # Goes through patient objects and dumps them info json file, using json encoder we made
        with open(self.filename, 'w') as file:
            for patient in self.patients:
                patient_json = dumps(patient, cls=PatientEncoder)
                file.write("%s\n" % patient_json)


    # Check autosave enabled or not
    def autosave_check(self):

        if self.autosave:
            return True
        return False


    # Return a list of all patients
    def list_patients(self) -> List[Patient]:

        return self.patients


    # Return all patients matching the name
    def retrieve_patients(self, name: str) -> List[Patient]:

        return [patient for patient in self.patients if name.lower() in patient.get_name().lower()]


    # Search for a patient by PHN and return it
    def search_patient(self, phn: int) -> Optional[Patient]:

        # If autosave enabled, check using this
        if self.autosave_check():
            for patient in self.patients:
                if patient.phn == phn:
                    return patient
            return None

        # If autosave disabled, check using this
        for patient in self.patients:
            if patient.get_phn() == phn:
                return patient
        return None


    # Add a new patient if they do not already exist
    def create_patient(self, patient: Patient) -> None:

        # Raise is phn already exists
        if self.search_patient(patient.get_phn()):
            raise ValueError("Patient with this PHN already exists.")
        self.patients.append(patient)

        # If autosave enabled, save patients instance 
        if self.autosave_check():
            self.save_patients()


    # Update a patient's information
    def update_patient(self, phn: int, updated_patient: Patient) -> None:
        for i, patient in enumerate(self.patients):
            if patient.get_phn() == phn:
                self.patients[i] = updated_patient

                if self.autosave_check():
                    self.save_patients()

                return
            
        raise ValueError("Patient with this PHN does not exist.")


    def delete_patient(self, phn: int) -> None:
        # Remove a patient by PHN
        self.patients = [patient for patient in self.patients if patient.get_phn() != phn]

        if self.autosave_check():
            self.save_patients()


    def delete_all_patients(self) -> None:
        # Remove all patients
        self.patients.clear()

        if self.autosave_check():
            self.save_patients()
