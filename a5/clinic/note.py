from datetime import *

class Note:
    def __init__(self, code, text) -> None:
        self.code = code
        self.text = text
        self.timestamp = datetime.now()


    def __eq__(self, other: 'Note') -> bool:
        # Compare self note vs other notes attributes and return result    

        return self.code == other.code and self.text == other.text
    
    def __str__(self) -> str:
        # Return a formatted string with code and text of self Note

        return f'{self.code}: {self.text}'

    def __repr__(self) -> str:
        # Return a formatted string with Note attributes

        return f'Note({repr(self.code)}, {repr(self.text)})'
    
    def get_note_code(self):
        # Return notes number order.

        return self.code
    

    def get_note_text(self):
        # Return notes text.

        return self.text
    

    def update_time(self):
        # Update time.

        self.timestamp = datetime.now()

        return