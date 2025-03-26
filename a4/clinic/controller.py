from clinic.patient import Patient
from clinic.note import Note
from clinic.patient_record import *
from clinic.dao.patient_dao_json import PatientDAOJSON
from clinic.dao.patient_dao import PatientDAO
from clinic.exception.invalid_login_exception import InvalidLoginException
from clinic.exception.duplicate_login_exception import DuplicateLoginException
from clinic.exception.invalid_logout_exception import InvalidLogoutException
from clinic.exception.illegal_access_exception import IllegalAccessException
from clinic.exception.illegal_operation_exception import IllegalOperationException
from clinic.exception.no_current_patient_exception import NoCurrentPatientException
import os 
import hashlib

class Controller:

    def __init__(self, autosave) -> None:
    # Create the dict to store usernames & passwords and the current login state.

        self.patient_dao = PatientDAOJSON(autosave)
        self.credentials = {
            "user" : "123456",
            "ali" : "@G00dPassw0rd"
        }

        self.login_state = False
        self.current_patient = None
        self.autosave = autosave

    def login_check(self):
    # Reply with log in state for illegal access check, raise alert if not logged in
         
        if not self.login_state:
            raise IllegalAccessException("cannot search patient without logging in")
        
        return
    

    def patient_set_check(self):
    # Check if patient is set properly
        if not self.current_patient:
            raise NoCurrentPatientException("cannot work on notes without a valid current patient")
        
        return


    def load_users(self):
        # Lifted from lab9, function handles loading users from the users.txt file
        users = {}

        # Ensures that it always checks where controller.py is for the users.txt file
        base_dir = os.path.dirname(__file__)
        file_path = os.path.join(base_dir, 'users.txt')

        # Opens users.txt, extracts the lines and formats them properly, then stores in array
        with open(file_path, 'r') as file:
            for line in file:
                content = line.strip()
                content = content.split(",")
                users[content[0]] = content[1]
                

        return users
    

    def get_password_hash(self, password):
    # Lifted from lab9, password hash function

        encoded_password = password.encode('utf-8')     # Convert the password to bytes
        hash_object = hashlib.sha256(encoded_password)      # Choose a hashing algorithm (e.g., SHA-256)
        hex_dig = hash_object.hexdigest()       # Get the hexadecimal digest of the hashed password
        return hex_dig


    def login(self, username, password):
    # Login handler.

        if self.login_state:
            raise DuplicateLoginException("cannot login again while still logged in")


        # Login handler with autosave enabled
        if self.autosave:
            users_list = self.load_users()
            
            # Again lifted from lab9, interfaces with password hashing function to get back hash result
            if users_list.get(username):
                password_hash = self.get_password_hash(password)
                if users_list.get(username) == password_hash:
                    self.login_state = True
                else:
                    raise InvalidLoginException("login in with incorrect password")
            else:
                raise InvalidLoginException("login in with incorrect username")


        # Login hander with autosave disabled.
        else:
            if username in self.credentials: 
                if self.credentials[username] == password:
                    self.login_state = True
                else:
                    raise InvalidLoginException("login in with incorrect password")
            else:
                raise InvalidLoginException("login in with incorrect username")
            
        return self.login_state
        

    def logout(self):
    # Logout handler.

        # Handle if no user is logged in & someone attempts to logout.
        if not self.login_state:
            raise InvalidLogoutException("log out only after being logged in")
        

        self.login_state = False

        return True


    def create_patient(self, phn, name, DoB, phone, email, address):
    # Create new patient profile if a user is logged in.

        # Check if login_state is false.
        self.login_check() 
        
        # Check if patient exists with that phn already.
        if self.patient_dao.search_patient(phn):
            raise IllegalOperationException("cannot add a patient with a phn that is already registered")
        
        
        # self.patient_list.append(Patient(phn, name, DoB, phone, email, address))
        self.patient_dao.create_patient(Patient(phn, name, DoB, phone, email, address, self.autosave))
        
        return Patient(phn, name, DoB, phone, email, address, self.autosave)
    

    def search_patient(self, phn_for_lookup):
    # Search for the patient using phn_for_lookup and return desired patient, return null if no match.

        self.login_check()

        return self.patient_dao.search_patient(phn_for_lookup)
    

    def retrieve_patients(self, name):
    # Retrieve patient from created instances using provided name.

        # Check if logged in.
        self.login_check()
        
        # return name_matches
        return self.patient_dao.retrieve_patients(name)
    

    def update_patient(self, phn_for_lookup, phn, name, DoB, phone, email, address):
    # Retrieve patient using phn_for_lookup and update the with given info.

        patient_to_update = self.search_patient(phn_for_lookup)
        

        # Check if logged in and that patient exists.
        self.login_check()

        # Check that there is a current patient to update     
        if not patient_to_update: 
            raise IllegalOperationException("cannot update patient with a phn that is not registered")

        # **added**
        if self.current_patient and self.current_patient.get_phn() == phn_for_lookup:
            raise IllegalOperationException("cannot update the current patient")
        
        # Check if phn_for_lookup is not equal to phn and that a patient does not exist with phn already.
        if phn_for_lookup != phn and self.search_patient(phn):
            raise IllegalOperationException("cannot update patient and give them a registered phn")

        # return patient_to_update   
        updated_patient = Patient(phn, name, DoB, phone, email, address, self.autosave)
        self.patient_dao.update_patient(phn_for_lookup, updated_patient)
        
        return updated_patient        
        

    def delete_patient(self, phn_for_delete):
    # Find patient using phn_for_lookup and delete them from system.

        # Check if logged in and at least 1 patient exists currently.
        if not self.login_state:
            raise IllegalAccessException("cannot delete patient without logging in")
        
        # Check if deleting current patient
        if self.current_patient and self.current_patient.get_phn() == phn_for_delete:
            raise IllegalOperationException("cannot delete the current patient")  
        
        # Check if deleting non exist patient
        if not self.search_patient(phn_for_delete):
            raise IllegalOperationException("cannot delete patient with a phn that is not registered")

        self.patient_dao.delete_patient(phn_for_delete)

        return True
    

    def list_patients(self):
    # Return the length of the patient list.

        self.login_check()

        # return self.patient_list
        return list(self.patient_dao.list_patients())


    def set_current_patient(self, phn):
    # Sets the taken PHN of a patient as the current. 

        self.login_check()

        patient = self.search_patient(phn)

        if patient:
            self.current_patient = patient
            return True

        raise IllegalOperationException("cannot set non-existent patient as the current patient")       
    

    def get_current_patient(self):
    # Returns the current patient.    

        self.login_check()

        return self.current_patient


    def unset_current_patient(self):
    # Unsets the Current patient.

        self.login_check()

        self.current_patient = None

        return True


    def create_note(self, text):
        # Create a new note for the current patient.

        self.login_check()

        self.patient_set_check()

        return self.current_patient.create_note(text)


    def search_note(self, code):
        # Search for a note in the current patient's record by code.

        self.login_check()

        self.patient_set_check()

        return self.current_patient.search_note(code)
    

    def retrieve_notes(self, text):
        # Search for notes in current patient's record by text.

        self.login_check()

        self.patient_set_check()
        
        return self.current_patient.retrieve_notes(text)
    

    def update_note(self, code, text):
        # Retrieve note by code and update contents

        self.login_check()

        self.patient_set_check()

        return self.current_patient.update_note(text, code)
    

    def delete_note(self, code):
        # Delete note via its code.

        self.login_check()

        self.patient_set_check()


        return self.current_patient.delete_note(code)
    

    def list_notes(self):
        # Return list of patients notes

        self.login_check()

        self.patient_set_check()

        return self.current_patient.list_notes()