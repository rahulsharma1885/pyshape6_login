import sys
import mysql.connector

from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QFormLayout,
    QMessageBox,
    QHBoxLayout
)

from PySide6.QtCore import Qt


class LoginWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Company Login")
        self.setFixedSize(400, 250)

        self.create_widgets()
        self.create_layout()
        self.connect_events()

    # -------------------------
    # Widgets
    # -------------------------

    def create_widgets(self):

        self.title = QLabel("Employee Login")
        self.title.setAlignment(Qt.AlignCenter)

        self.username = QLineEdit()
        self.username.setPlaceholderText("Enter username")

        self.password = QLineEdit()
        self.password.setPlaceholderText("Enter password")
        self.password.setEchoMode(QLineEdit.Password)

        self.login_btn = QPushButton("Login")
        self.cancel_btn = QPushButton("Cancel")

        # Button size
        self.login_btn.setFixedSize(100, 35)
        self.cancel_btn.setFixedSize(100, 35)

    # -------------------------
    # Layout
    # -------------------------

    def create_layout(self):

        # Form Layout
        form = QFormLayout()

        form.setSpacing(15)

        form.addRow("Username:", self.username)
        form.addRow("Password:", self.password)

        # Button Layout
        button_layout = QHBoxLayout()

        button_layout.addStretch()
        button_layout.addWidget(self.login_btn)
        button_layout.addWidget(self.cancel_btn)
        button_layout.addStretch()

        # Main Layout
        layout = QVBoxLayout()

        layout.setContentsMargins(40, 30, 40, 30)
        layout.setSpacing(15)

        layout.addWidget(self.title)

        layout.addSpacing(10)

        layout.addLayout(form)

        # Empty space
        layout.addStretch()

        # Buttons at bottom
        layout.addLayout(button_layout)

        self.setLayout(layout)

    # -------------------------
    # Events
    # -------------------------

    def connect_events(self):

        self.login_btn.clicked.connect(self.login)
        self.cancel_btn.clicked.connect(self.close)

    # -------------------------
    # Database Connection
    # -------------------------

    def connect_database(self):

        try:

            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="rahul123",
                database="company"
            )

            return connection

        except mysql.connector.Error as error:

            QMessageBox.critical(
                self,
                "Database Error",
                f"Database connection failed:\n{error}"
            )

            return None

    # -------------------------
    # Login
    # -------------------------

    def login(self):

        username = self.username.text().strip()
        password = self.password.text()

        # Validation
        if not username or not password:

            QMessageBox.warning(
                self,
                "Validation",
                "Username and password are required."
            )

            return

        # Connect database
        connection = self.connect_database()

        if connection is None:
            return

        try:

            cursor = connection.cursor()

            query = """
                SELECT id, username
                FROM users
                WHERE username = %s
                AND password = %s
            """

            cursor.execute(
                query,
                (username, password)
            )

            user = cursor.fetchone()

            if user:

                QMessageBox.information(
                    self,
                    "Login Successful",
                    f"Welcome {user[1]}!"
                )

                self.open_dashboard()

            else:

                QMessageBox.warning(
                    self,
                    "Login Failed",
                    "Invalid username or password."
                )

            cursor.close()

        except mysql.connector.Error as error:

            QMessageBox.critical(
                self,
                "Database Error",
                str(error)
            )

        finally:

            connection.close()

    # -------------------------
    # Dashboard
    # -------------------------

    def open_dashboard(self):

        self.dashboard = DashboardWindow()

        self.dashboard.show()

        self.close()


# ==================================================
# Dashboard Window
# ==================================================

class DashboardWindow(QWidget):

    def __init__(self):

        super().__init__()

        self.setWindowTitle("Dashboard")
        self.resize(600, 400)

        label = QLabel("Welcome to Employee Dashboard")

        label.setAlignment(Qt.AlignCenter)

        layout = QVBoxLayout()

        layout.addWidget(label)

        self.setLayout(layout)


# ==================================================
# Application
# ==================================================

if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = LoginWindow()

    window.show()

    sys.exit(app.exec())