from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout
from clinic.controller import Controller

class LoginPage(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Login')
        self.setGeometry(400, 200, 300, 150)

        # Layout for the login window
        layout = QVBoxLayout()

        # Username input
        self.username_label = QLabel("Username:")
        self.username_input = QLineEdit()
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)

        # Password input
        self.password_label = QLabel("Password:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)

        # Login button
        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.login)
        layout.addWidget(self.login_button)

        # Bypass button
        self.bypass_button = QPushButton("Bypass")
        self.bypass_button.clicked.connect(self.bypass_login)
        layout.addWidget(self.bypass_button)

        # Error label (initially hidden)
        self.error_label = QLabel("")
        self.error_label.setStyleSheet("color: red;")
        layout.addWidget(self.error_label)

        self.setLayout(layout)

    def login(self):
        """Authenticate the user."""
        username = self.username_input.text()
        password = self.password_input.text()

        controller = Controller(autosave = True)  # Assuming Controller class handles authentication logic

        # Try to login with the credentials
        try:
            controller.login(username, password)
            self.accept()  # Close the login dialog and return success
        except:
            # Display error message if authentication fails
            self.error_label.setText("Invalid username or password!")

            
    def bypass_login(self):

        self.accept()

