import unittest
from datetime import datetime
from clinic.note import Note

class TestNote(unittest.TestCase):
    
    def setUp(self):

        # Set up a Note instance
        self.note = Note(code = 1, text = "Their poopoo is very wet")


    def test_initialization(self):

        # Test if the Note is initialized with correct attributes
        self.assertEqual(self.note.code, 1)
        self.assertEqual(self.note.text, "Their poopoo is very wet")
        print("TEST INITIAL DONE")

    def test_equality(self):

        # Test the equality of two Note instances with the same data
        other_note_1 = Note(code = 1, text = "Their poopoo is very wet")
        self.assertEqual(self.note, other_note_1)

        # Test with different text or code to ensure inequality
        other_note_2 = Note(code = 2, text = "Their poopoo not coming out")
        self.assertNotEqual(self.note, other_note_2)
        print("TEST EQ DONE")

    def test_str_representation(self):

        # Test the __str__ method for formatted string output. 
        expected_str = "1: Their poopoo is very wet"
        self.assertEqual(str(self.note), expected_str)
        print("TEST STR DONE")

    def test_repr_representation(self):

        # Test the __repr__ method for a detailed string representation
        expected_repr = "Note(1, 'Their poopoo is very wet')"
        self.assertEqual(repr(self.note), expected_repr)
        print("TEST REPR DONE")    

    def test_get_note_code(self):

        # Test the get_note_code method
        self.assertEqual(self.note.get_note_code(), 1)
        self.assertNotEqual(self.note.get_note_code(), 2)
        print("TEST GET CODE DONE")

    def test_get_note_text(self):

        # Test the get_note_text method
        self.assertEqual(self.note.get_note_text(), "Their poopoo is very wet")
        self.assertNotEqual(self.note.get_note_text(), "Their poopoo is very hard")
        print("TEST GET TEXT DONE")

if __name__ == "__main__":
    unittest.main()
