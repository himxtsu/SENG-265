from unittest import TestCase
from unittest import main
from clinic.controller import Controller
from clinic.patient import Patient

class PatientTests(TestCase):

    def setUp(self):
        self.controller = Controller()


    def test_login_logout(self):
        self.assertFalse(self.controller.logout(), "log out only after being logged in")
        self.assertFalse(self.controller.login("theuser", "clinic2024"), "login in with incorrect username")
        self.assertFalse(self.controller.login("user", "123456"), "login in with incorrect password")
        self.assertTrue(self.controller.login("user", "clinic2024"), "login correctly")
        self.assertFalse(self.controller.login("user", "clinic2024"), "cannot login again while still logged in")
        self.assertTrue(self.controller.logout(), "log out correctly")
        self.assertTrue(self.controller.login("user", "clinic2024"), "can login again")
        self.assertTrue(self.controller.logout(), "can log out again")
        print("TEST LOGIN DONE")


    def test_create_search_patient(self):

        # Create expected patients
        expected_patient_1 = Patient(9790012000, "John Doe", "2000-10-10", "250 203 1010", "john.doe@gmail.com", "300 Moss St, Victoria")
        expected_patient_2 = Patient(9790014444, "Mary Doe", "1995-07-01", "250 203 2020", "mary.doe@gmail.com", "300 Moss St, Victoria")
        expected_patient_3 = Patient(9792225555, "Joe Hancock", "1990-01-15", "278 456 7890", "john.hancock@outlook.com", "5000 Douglas St, Saanich")

        # Test that patient creation fails without login
        self.assertIsNone(self.controller.create_patient(9790012000, "John Doe", "2000-10-10", "250 203 1010", "john.doe@gmail.com", "300 Moss St, Victoria"), 
            "cannot create patient without logging in")

        # Login to create a patient.
        self.assertTrue(self.controller.login("user", "clinic2024"), "login correctly")
        actual_patient = self.controller.create_patient(9790012000, "John Doe", "2000-10-10", "250 203 1010", "john.doe@gmail.com", "300 Moss St, Victoria")
        self.assertIsNotNone(actual_patient, "patient created cannot be null")
        self.assertEqual(actual_patient, expected_patient_1, "patient John Doe was created and their data are correct")

        # Search for the patient.
        actual_patient = self.controller.search_patient(9790012000)
        self.assertIsNotNone(actual_patient, "patient created and retrieved cannot be null")
        self.assertEqual(actual_patient, expected_patient_1, "patient John Doe was created, retrieved and their data are correct")

        # Test that creating a patient with same PHN fails.
        actual_patient = self.controller.create_patient(9790012000, "Mary Doe", "1995-07-01", "250 203 2020", "mary.doe@gmail.com", "300 Moss St, Victoria")
        self.assertIsNone(actual_patient, "cannot create patient with same personal health number as from an existing patient")

        # Create second patient.
        actual_patient = self.controller.create_patient(9790014444, "Mary Doe", "1995-07-01", "250 203 2020", "mary.doe@gmail.com", "300 Moss St, Victoria")
        self.assertIsNotNone(actual_patient, "second patient created cannot be null")
        self.assertEqual(actual_patient, expected_patient_2, "second patient, Mary Doe, was created and their data are correct")

        # Search for the second patient.
        actual_patient = self.controller.search_patient(9790014444)
        self.assertIsNotNone(actual_patient, "patient created and retrieved cannot be null")
        self.assertEqual(actual_patient, expected_patient_2, "second patient, Mary Doe, was created, retrieved and their data are correct")

        # Create 3rd patient.
        actual_patient = self.controller.create_patient(9792225555, "Joe Hancock", "1990-01-15", "278 456 7890", "john.hancock@outlook.com", "5000 Douglas St, Saanich")
        self.assertIsNotNone(actual_patient, "patient created cannot be null")
        self.assertEqual(actual_patient, expected_patient_3, "patient Joe Hancock was created and their data are correct")

        # Search for the 3rd patient.
        actual_patient = self.controller.search_patient(9792225555)
        self.assertIsNotNone(actual_patient, "patient created and retrieved cannot be null")
        self.assertEqual(actual_patient, expected_patient_3, "third patient, Joe Hancock, was created, retrieved and their data are correct")

        # Verify previous patients not changed.
        actual_patient = self.controller.search_patient(9790014444)
        self.assertIsNotNone(actual_patient, "patient created and retrieved cannot be null regardless of search order")
        self.assertEqual(actual_patient, expected_patient_2, "patient Mary Doe was created, retrieved and their data are correct regardless of search order")

        actual_patient = self.controller.search_patient(9790012000)
        self.assertIsNotNone(actual_patient, "patient created and retrieved cannot be null regardless of search order")
        self.assertEqual(actual_patient, expected_patient_1, "patient John Doe was created, retrieved and their data are correct regardless of search order")
        print("TEST PATIENT DONE")


if __name__ == "__main__":
    main()
