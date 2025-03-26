from clinic.patient_record import *

class Patient:
    def __init__(self, phn: int, name: str, DoB: str, phone: str, email: str, address: str) -> None:
    # Initializes an instance of a Patient with the given arguments.

        self.p_health_number = phn
        self.name = name
        self.birth_date = DoB
        self.phone_number = phone
        self.email = email
        self.address = address
        self.patient_record = PatientRecord()


    def __eq__(self, other: 'Patient') -> bool:
    # Return True if all attributes of self and other are equal.


        return self.p_health_number == other.p_health_number and self.name == other.name and self.birth_date == other.birth_date \
               and self.phone_number == other.phone_number and self.email == other.email and self.address == other.address 
    
    def __str__(self) -> str:
    # Returns a formatted string listing a Patient's attributes

        return f'PHN: {self.p_health_number}, Name: {self.name}, DoB: {self.birth_date}, Phone: {self.phone_number}, Email: {self.email}, Address: {self.address}'

    def __repr__(self) -> str:
    # Returns a formatted string with Patient attributes

        return f'Patient({repr(self.p_health_number)}, {repr(self.name)}, {repr(self.birth_date)}, {repr(self.phone_number)}, {repr(self.email)}, {repr(self.address)}'

    def get_p_health_number(self) -> int:
        # Return a Patient's PHN.

        return self.p_health_number
    

    def get_name(self) -> str:
        # Return name of the Patient.

        return self.name


    def get_birth_date(self) -> str:
        # Return the birthday of the Patient.

        return self.birth_date


    def get_phone_number(self) -> str:
        # Return the phone number of the Patient.

        return self.phone_number
    

    def get_email(self) -> str:
        # Return the email of the Patient.

        return self.email


    def get_address(self) -> str:
        # Return the address of the Patient.

        return self.address
    

    def create_note(self, text):
        # Create new note for patient.
    
        return self.patient_record.add_note(text)
    

    def search_note(self, code):
        # Search for note by code.

        return self.patient_record.find_note_by_code(code)
    

    def retrieve_notes(self, text):
        # Search for notes by text.

        return self.patient_record.retrieve_notes(text)
    

    def update_note(self, code, text):
        # Retrieve note by code and update contents

        return self.patient_record.update_note(text, code)
    

    def delete_note(self, code):
        # Delete desired note via its code.

        return self.patient_record.delete_note(code)
    

    def list_notes(self):
        # Return list of patients notes

        return self.patient_record.list_notes()