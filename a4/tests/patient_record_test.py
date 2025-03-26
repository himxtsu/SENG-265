from unittest import TestCase, main
from clinic.patient_record import PatientRecord

class PatientRecordTests(TestCase):
    
    def setUp(self):

        # Initialize PatientRecord instance for testing.
        self.patient_record = PatientRecord()
    

    def test_add_note(self):

        # Test add a note.
        note = self.patient_record.add_note("Initial consult")
        self.assertIsNotNone(note, "Note created cannot be null")
        self.assertEqual(note.get_note_code(), 1, "Note code should start from 1")
        self.assertEqual(note.get_note_text(), "Initial consult", "Note text should match input")
        print("TEST ADD DONE")
    

    def test_get_notes(self):

        # Test retrieving all notes.
        self.patient_record.add_note("First note")
        self.patient_record.add_note("Second note")
        notes = self.patient_record.get_notes()
        self.assertEqual(len(notes), 2, "Should have 2 notes")
        self.assertEqual(notes[0].get_note_text(), "First note", "First note text should match")
        self.assertEqual(notes[1].get_note_text(), "Second note", "Second note text should match")
        print("TEST GET DONE")   

    def test_find_note_by_code(self):

        # Test finding a note by its code.
        self.patient_record.add_note("Find me")
        note = self.patient_record.find_note_by_code(1)
        self.assertIsNotNone(note, "Note with code 1 should exist")
        self.assertEqual(note.get_note_text(), "Find me", "Note text should match")
        print("TEST FIND DONE")

        # Test searching for a non existent note.
        note = self.patient_record.find_note_by_code(999)
        self.assertIsNone(note, "Non existent note should return None")


    def test_retrieve_notes(self):

        # Test retrieving notes by text content.
        self.patient_record.add_note("Follow up visit")
        self.patient_record.add_note("Initial consult")
        matching_notes = self.patient_record.retrieve_notes("consult")
        self.assertEqual(len(matching_notes), 1, "Should find 1 note matching 'consult'")
        self.assertEqual(matching_notes[0].get_note_text(), "Initial consult", "Matching note text should be 'Initial consult'")
        print("TEST RETRIEVE DONE")

    def test_update_note(self):

        # Test updating an existing note.
        self.patient_record.add_note("Old text")
        updated_note = self.patient_record.update_note(1, "Updated text")
        self.assertIsNotNone(updated_note, "Updated note should not be None")
        self.assertEqual(updated_note.get_note_text(), "Updated text", "Note text should be updated")

        # Test updating a non existent note.
        updated_note = self.patient_record.update_note(999, "This should not work")
        self.assertIsNone(updated_note, "Updating non existent note should return None")
        print("TEST UPDATE DONE")

    def test_delete_note(self):

        # Test deleting an existing note.
        self.patient_record.add_note("To be deleted")
        deleted = self.patient_record.delete_note(1)
        self.assertTrue(deleted, "Delete operation should return True")
        self.assertEqual(len(self.patient_record.get_notes()), 0, "Note should be deleted")
    
        # Attempt to delete a non existent note.
        deleted = self.patient_record.delete_note(999)
        self.assertIsNone(deleted, "Delete operation on non existent note should return None")
    
        # Confirm that no notes exist in the record.
        self.assertEqual(len(self.patient_record.get_notes()), 0, "Patient record should remain empty when deleting non existent note")
        print("TEST DELETE DONE")

    def test_list_notes(self):

        # Test listing notes in reverse order.
        self.patient_record.add_note("First note")
        self.patient_record.add_note("Second note")
        notes = self.patient_record.list_notes()
        self.assertEqual(len(notes), 2, "Should return 2 notes in reversed order")
        self.assertEqual(notes[0].get_note_text(), "Second note", "First note in list should be the most recent")
        print("TEST LIST DONE")

if __name__ == "__main__":
    main()
