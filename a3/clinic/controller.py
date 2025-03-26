from clinic.patient import Patient
from clinic.note import Note
from clinic.patient_record import *

class Controller:

    def __init__(self) -> None:
    # Create the dict to store usernames & passwords and the current login state.

        self.credentials = {
            "user" : "clinic2024",
            "admin" : "password"
        }

        self.login_state = False
        self.patient_list = []
        self.current_patient = None



    def login(self, username, password):
    # Login handler.

        # Handle if a user is already logged in & another user tries to login
        if self.login_state:
            print("User: " + username + " is already logged in")
            return False


        # Check for correct username & password, change login_state depending on success.
        if username in self.credentials:
            self.login_state = True if self.credentials[username] == password else print("Incorrect username or password")

        
        return self.login_state
        

    def logout(self):
    # Logout handler.

        # Handle if no user is logged in & someone attempts to logout.
        if not self.login_state:
            print("A user is not currently logged in")
            return False
        

        self.login_state = False
        print("Logged out")

        return True


    def create_patient(self, phn, name, DoB, phone, email, address):
    # Create new patient profile if a user is logged in.

        # Check if login_state is false or a patient exists with that phn already.
        if not self.login_state or self.search_patient(phn):
            return 
        
        
        self.patient_list.append(Patient(phn, name, DoB, phone, email, address))
        
        return Patient(phn, name, DoB, phone, email, address)
    

    def search_patient(self, phn_for_lookup):
    # Search for the patient using phn_for_lookup and return desired patient, return null if no match.

        # Loop through list of created patient instances and return patient if a phn matches.
        for patient in self.patient_list:
            if patient.get_p_health_number() == phn_for_lookup:   
                return patient 
        return
    

    def retrieve_patients(self, name):
    # Retrieve patient from created instances using provided name.

        # Check if logged in.
        if not self.login_state:
            return
        
        # Create list of potential matches by checking all patient instances.
        name_matches = [
            patient
            for patient in self.patient_list
            if name in patient.get_name()
        ]
        
        return name_matches
    

    def update_patient(self, phn_for_lookup, phn, name, DoB, phone, email, address):
    # Retrieve patient using phn_for_lookup and update the with given info.

        patient_to_update = self.search_patient(phn_for_lookup)
        

        # Check if logged in and that patient exists.
        if not self.login_state or not patient_to_update:
            return 

        # **added**
        if self.current_patient and self.current_patient.get_p_health_number() == phn_for_lookup:
            return False
        
        # Check if phn_for_lookup is not equal to phn and that a patient does not exist with phn already.
        if phn_for_lookup != phn and self.search_patient(phn):
            return False


        # ^^^^ Clean up later, 2 seperate if chunks is odd but works for now ^^^^

        patient_to_update.p_health_number = phn 
        patient_to_update.name = name
        patient_to_update.birth_date = DoB
        patient_to_update.phone_number = phone
        patient_to_update.email = email
        patient_to_update.address = address
        
        return patient_to_update    

    def delete_patient(self, phn_for_delete):
    # Find patient using phn_for_lookup and delete them from system.

        # Check if logged in and at least 1 patient exists currently.
        if not self.login_state or len(self.patient_list) <= 0:
            return
        
        # **added**
        if self.current_patient and self.current_patient.get_p_health_number() == phn_for_delete:
            return False  

        # Create new patient list excluding the patient who is slated for deletion.
        self.patient_list = [
            patient
            for patient in self.patient_list
            if patient.get_p_health_number() != phn_for_delete
        ] 

        return True
    

    def list_patients(self):
    # Return the length of the patient list.

        if not self.login_state:
            return

        return self.patient_list


    def set_current_patient(self, phn):
    # Sets the taken PHN of a patient as the current. 

        if not self.login_state:
            return False

        patient = self.search_patient(phn)

        if patient:
            self.current_patient = patient
            return True

        return False       
    

    def get_current_patient(self):
    # Returns the current patient.    

        if not self.login_state:
            return None

        return self.current_patient


    def unset_current_patient(self):
    # Unsets the Current patient.

        self.current_patient = None

        return True


    def create_note(self, text):
        # Create a new note for the current patient.

        if not self.login_state or not self.current_patient:
            return None

        return self.current_patient.create_note(text)


    def search_note(self, code):
        # Search for a note in the current patient's record by code.

        if not self.login_state or not self.current_patient:
            return None

        return self.current_patient.search_note(code)
    

    def retrieve_notes(self, text):
        # Search for notes in current patient's record by text.

        if not self.login_state or not self.current_patient:
            return None
        
        return self.current_patient.retrieve_notes(text)
    

    def update_note(self, code, text):
        # Retrieve note by code and update contents

        if not self.login_state or not self.current_patient:
            return None

        return self.current_patient.update_note(text, code)
    

    def delete_note(self, code):
        # Delete note via its code.

        if not self.login_state or not self.current_patient:
            return 


        return self.current_patient.delete_note(code)
    

    def list_notes(self):
        # Return list of patients notes

        if not self.login_state or not self.current_patient:
            return

        return self.current_patient.list_notes()