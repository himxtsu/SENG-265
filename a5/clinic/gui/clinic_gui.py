import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableView, \
    QVBoxLayout, QPushButton, QPlainTextEdit, QWidget, QHBoxLayout, \
    QDialog, QMenu
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from clinic.dao.patient_dao_json import PatientDAOJSON
from clinic.dao.note_dao_pickle import NoteDAOPickle
from clinic.patient import Patient
from clinic.controller import Controller
from clinic.gui.login_page_gui import LoginPage
from clinic.gui.patient_add_gui import PatientAddGui
from clinic.gui.patient_update_gui import PatientUpdateGui
from clinic.gui.patient_search_gui import PatientSearchGui
from clinic.gui.patient_delete_gui import PatientDeleteGui
from clinic.gui.patient_search_for_update_gui import PatientUpdateSearchGui
from clinic.gui.note_add_gui import NoteInput
from clinic.gui.note_delete_gui import NoteDelete
from clinic.gui.note_update_code_finder_gui import NoteUpdateSearch
from clinic.gui.note_update import NoteUpdate
from clinic.gui.note_text_search import NoteTextSearch


class ClinicGUI(QMainWindow):

    def __init__(self):
        super().__init__()

        # Initialize the main window
        self.setWindowTitle('Clinic Management')
        self.setGeometry(100, 100, 800, 600)

        # Create the central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Layout for the main window
        layout = QVBoxLayout()

        # Create and set up the table for patients
        self.patient_table = QTableView()
        self.patient_model = QStandardItemModel()
        self.patient_table.setModel(self.patient_model)

        # Context menu Stuff for the note function.
        self.context_menu = QMenu(self)
        action1 = self.context_menu.addAction("Add Note")
        action2 = self.context_menu.addAction("Delete Note")
        action3 = self.context_menu.addAction("Update Note")
        action4 = self.context_menu.addAction("Search Notes")
        
        # Connects context menu to actual functions
        action1.triggered.connect(self.handle_action1)
        action2.triggered.connect(self.handle_action2)
        action3.triggered.connect(self.handle_action3)
        action4.triggered.connect(self.handle_action4)


        # Add table headers
        self.patient_model.setHorizontalHeaderLabels(['PHN', 'Name', 'Birth Date', 'Phone', 'Email', 'Address'])

        # Create a button for viewing notes
        self.view_notes_button = QPushButton('View Notes')
        self.view_notes_button.clicked.connect(self.view_notes)

        # Create a button for adding patients.
        self.add_patient_button = QPushButton('Add New Patient')
        self.add_patient_button.clicked.connect(self.add_patient_gui)

        # Create button for updating patients.
        self.create_patient_button = QPushButton('Update Patient')
        self.create_patient_button.clicked.connect(self.search_for_update_gui)

        # Create button for searching patients.
        self.search_patient_button = QPushButton('Search For Patient')
        self.search_patient_button.clicked.connect(self.search_patient_gui)

        # Create button for searching patients.
        self.delete_patient_button = QPushButton('Delete A Patient')
        self.delete_patient_button.clicked.connect(self.delete_patient_gui)

        # Create button for logging out
        self.logout_button = QPushButton('Logout')
        self.logout_button.clicked.connect(self.logout)

        # Create the plain text edit widget for notes
        self.note_display = QPlainTextEdit()
        self.note_display.setReadOnly(True)

        # Create the layout for the buttons and table
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.view_notes_button)
        button_layout.addWidget(self.add_patient_button)
        button_layout.addWidget(self.create_patient_button)
        button_layout.addWidget(self.search_patient_button)
        button_layout.addWidget(self.delete_patient_button)
        button_layout.addWidget(self.logout_button)

        # Add widgets to the layout
        layout.addLayout(button_layout)
        layout.addWidget(self.patient_table)
        layout.addWidget(self.note_display)
  

        # Set the layout to the central widget
        central_widget.setLayout(layout)

        # Load patient data
        self.patient_dao = PatientDAOJSON(autosave=True)  # Use your existing DAO class
        self.load_patients()

        self.patient_crud_gui = None
        self.note_crud_gui = None

    def logout(self):
        """Handle logout and return to login page."""
        self.close()
        login_dialog = LoginPage()
        if login_dialog.exec() == QDialog.DialogCode.Accepted:
            self.show()

    def load_patients(self):
        """Loads patients from the PatientDAOJSON and populates the patient table."""
        patients = self.patient_dao.load_patients()
        
        # Clear the current rows in the model before adding new rows
        self.patient_model.clear()

        # Add headers again (optional)
        self.patient_model.setHorizontalHeaderLabels(['PHN', 'Name', 'Birth Date', 'Phone', 'Email', 'Address'])

        # Populate the table with patient data
        for patient in patients:
            self.patient_model.appendRow([
                self.create_non_editable_item(str(patient.phn)),
                self.create_non_editable_item(patient.name),
                self.create_non_editable_item(patient.birth_date),
                self.create_non_editable_item(patient.phone),
                self.create_non_editable_item(patient.email),
                self.create_non_editable_item(patient.address)
            ])
    
    
    def create_non_editable_item(self, text):
        """Creates a non-editable QStandardItem."""
        item = QStandardItem(text)
        item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        return item
    
    
    def view_notes(self):
        """Fetch and display notes for the selected patient in QPlainTextEdit."""
        selected_row = self.patient_table.selectionModel().selection().indexes()

        if not selected_row:
            self.note_display.setPlainText("No patient selected.")
            print("Yo")
            return

        selected_row = selected_row[0].row()  # Get the selected row
        patient_phn = self.patient_model.item(selected_row, 0).text()  # Get the PHN of the selected patient

        # Fetch the patient by PHN from the DAO
        print(patient_phn)
        patient = self.patient_dao.search_patient(patient_phn)
        print(patient)

        if patient is None:
            self.note_display.setPlainText("Patient not found.")
            print
            print("YoYo")
            return

        # Initialize NoteDAOPickle to fetch notes for this patient
        note_dao = NoteDAOPickle(patient_phn, autosave=True)
        notes = note_dao.read_all_notes()

        # Display the notes for the selected patient
        if notes:
            notes_text = f"Notes for {patient.name}:\n\n"
            for note in notes:
                notes_text += f"{note.get_note_code()}. {note.get_note_text()}\n"
            self.note_display.setPlainText(notes_text)
        else:
            self.note_display.setPlainText(f"No notes found for {patient.name}.")
    

    def view_notes_searched(self, patient, note_matches):
    # Used specifically by note text search function


        if note_matches:
            notes_text = f"Notes for {patient.name}:\n\n"
            for note in note_matches:
            # Loops over each note given by the note text search function. Displays them in the note box at the bottom
            # of the gui. Is functionally the same as the last part of the above view note function.
                notes_text += f"{note.get_note_code()}. {note.get_note_text()}\n"
            self.note_display.setPlainText(notes_text)
        else:
            self.note_display.setPlainText(f"No notes found for {patient.name}.")


    def show_main_window(self):
        """Function to show the main clinic window after successful login."""
        self.show()





    def search_patient_gui(self):
    # Opens patient search gui

        #Checks if another sub window is open. If it is close it
        if self.patient_crud_gui is not None:
            self.patient_crud_gui.close()  
        self.patient_crud_gui = PatientSearchGui()  
        self.patient_crud_gui.show()


    def delete_patient_gui(self):
    # Opens patient delete gui

        #Checks if another sub window is open. If it is close it
        if self.patient_crud_gui is not None:
            self.patient_crud_gui.close()  
        self.patient_crud_gui = PatientDeleteGui()  

        # Connects to main gui refresh capability, lets it know to refresh after delete
        self.patient_crud_gui.patient_deleted.connect(self.load_patients)
        self.patient_crud_gui.show()



    def add_patient_gui(self):
    # Opens add patient gui

        #Checks if another sub window is open. If it is close it
        if self.patient_crud_gui is not None:
            self.patient_crud_gui.close()  
        self.patient_crud_gui = PatientAddGui()
       # self.patient_crud_gui.patient_saved.connect(self.patient_dao.save_patients())
        # Connects to main gui refresh capability, lets it know to refresh after delete
        self.patient_crud_gui.patient_added.connect(self.load_patients)

        self.patient_crud_gui.show()


    def update_patient_gui(self, patient):
    # Opens update patient gui

        #Checks if another sub window is open. If it is close it
        if self.patient_crud_gui is not None:
            self.patient_crud_gui.close()  

        self.patient_crud_gui = PatientUpdateGui(patient)

        # Connects to main gui refresh capability, lets it know to refresh after delete
        self.patient_crud_gui.patient_updated.connect(self.load_patients)
        self.patient_crud_gui.show()


        
    def search_for_update_gui(self):
    # Opens gui for inputting which patient to target for the update patient feature

        #Checks if another sub window is open. If it is close it
        if self.patient_crud_gui is not None:
            self.patient_crud_gui.close()  
        self.patient_crud_gui = PatientUpdateSearchGui()  
        self.patient_crud_gui.show()

        # Once this signal is triggered, we know that this sub gui has found a valid patient to try and update
        # So it will call the main update function above it.
        self.patient_crud_gui.patient_found.connect(self.update_patient_gui)
        self.patient_crud_gui.show()


    def contextMenuEvent(self, event):
    # Used for the right click capabilities regarding note functions.

        if self.patient_table.underMouse():
            self.context_menu.exec(event.globalPos())


    def handle_action1(self):
    # Add note right click function

        selected_store = self.action_patient_check()

        # Specifies the patient we have right clicked as the one to work on.
        self.selected_patient = selected_store


        if self.selected_patient is None:
        # If valid patient not clicked, do nothing
            print("No patient selected")
            return
        
        if self.note_crud_gui is not None:
        # Close other sub menus
            self.note_crud_gui.close()  

        self.note_crud_gui = NoteInput(self.selected_patient)  
        self.note_crud_gui.show()


    def handle_action2(self):
    # Delete note function

        # Specifies the patient we have right clicked as the one to work on.
        self.selected_patient = self.action_patient_check()

        if self.selected_patient is None:
        # If valid patient not clicked, do nothing
            return
        
        if self.note_crud_gui is not None:
        # Close other sub menu.
            self.note_crud_gui.close()  

        self.note_crud_gui = NoteDelete(self.selected_patient)  
        self.note_crud_gui.show()


    def handle_action3(self):
    # Update note function

        # Specifies the patient we have right clicked as the one to work on.
        self.selected_patient = self.action_patient_check()

        if self.selected_patient is None:
        # If valid patient not clicked, do nothing
            return
        
        if self.note_crud_gui is not None:
        # Close other sub menu
            self.note_crud_gui.close()  

        self.note_crud_gui = NoteUpdateSearch(self.selected_patient)

        # If signal is found, then we launch the functiion handle_note_found and pass patient/ note code
        self.note_crud_gui.note_found.connect(self.handle_note_found)
        self.note_crud_gui.show()

    def handle_note_found(self, note_code):
    # Runs if above function has a signal emitted to it, this function actually launches the update gui.

        if self.note_crud_gui is not None:
        # Close any open sub menu.
            self.note_crud_gui.close()
        self.note_crud_gui = NoteUpdate(self.selected_patient, note_code)
        self.note_crud_gui.show()


    def handle_action4(self):
    # Searches desired patients notes for matching text.

        # Specifies the patient we have right clicked as the one to work on.
        self.selected_patient = self.action_patient_check()

        if self.selected_patient is None:
        # If valid patient not clicked, do nothing
            return
        
        if self.note_crud_gui is not None:
        # Close other sub menu open.
            self.note_crud_gui.close()  
        self.note_crud_gui = NoteTextSearch(self.selected_patient)
        # Connects to function below to actually display said notes.
        self.note_crud_gui.note_search.connect(self.handle_notes_found)
        self.note_crud_gui.show()


    def handle_notes_found(self, note_matches):
    # If action4 aka notes search finds notes, this function is passed the list of notes
    # and will then display them in the main notes section of the gui

        if self.note_crud_gui is not None:
        # Checks if sub gui is open
            self.note_crud_gui.close()
        self.view_notes_searched(self.selected_patient, note_matches)
        

    # def action_patient_check(self):
    # # Handles  checking that a valid patient has been right clicked.

    #     # Defines what selected row is.
    #     selected_row = self.patient_table.selectionModel().selection().indexes()

    #     if not selected_row:
    #     # If no row selected, no patient is selected
    #         self.note_display.setPlainText("No patient selected.")
    #         return

    #     # Takes selected row and sets patient_phn with patients phn
    #     selected_row = selected_row[0].row()  # Get the selected row
    #     patient_phn = self.patient_model.item(selected_row, 0).text()  # Get the PHN of the selected patient

    #     # Fetch the patient by PHN from the DAO
    #     patient = self.patient_dao.search_patient(patient_phn)

    #     if patient is None:
    #     # If no phn matches we have no patient
    #         self.note_display.setPlainText("Patient not found.")
    #         return
    #     # Returns valid patient
    #     return patient

    def action_patient_check(self):
        """Handles checking that a valid patient has been right-clicked."""
        selected_row = self.patient_table.selectionModel().selection().indexes()

        if not selected_row:
            self.note_display.setPlainText("No patient selected.")
            return None

        selected_row = selected_row[0].row()  # Get the selected row
        patient_phn = self.patient_model.item(selected_row, 0).text()
        print(f"Selected PHN: {patient_phn}, Row: {selected_row}")  # Debugging log

        # Fetch the patient by PHN from the DAO
        patient = self.patient_dao.search_patient(patient_phn)

        if patient is None:
            self.note_display.setPlainText("Patient not found.")
            return None

        print(f"Patient Found: {patient.name}, PHN: {patient_phn}")  # Debugging log
        return patient


def main():
    # app = QApplication(sys.argv)
    # window = ClinicGUI()
    # window.show()
    # app.exec()
    app = QApplication(sys.argv)

    # Show the login dialog first
    login_dialog = LoginPage()
    if login_dialog.exec() == QDialog.DialogCode.Accepted:
        # If login is successful, open the main clinic window
        window = ClinicGUI()
        window.show()
        app.exec()
    else:
        # If login fails, exit the application
        sys.exit()


if __name__ == '__main__':
    main()
