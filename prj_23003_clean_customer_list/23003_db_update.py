# it is necessary to represent numbers of customer into text field not label

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QFileDialog
from PyQt5.QtCore import Qt
import sqlite3


class DatabaseManager:
    def __init__(self):
        self.connection = None
        self.cursor = None

    def connect(self, db_file):
        print("Connecting to the database...")
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()
        print("Connected!")

    def disconnect(self):
        if self.connection:
            self.connection.close()
            print("Connection Closed!")

    def search_company(self, search_term):
        query = "SELECT sold_to_customer, agent_person, company_code_n, customer_name, indirect_direct, channel, type, tier, tier_new, Comments FROM customers WHERE customer_name LIKE ? OR sold_to_customer LIKE ?"
        self.cursor.execute(query, (f"%{search_term}%", f"%{search_term}%"))
        first_result = self.cursor.fetchone()
        all_results = self.cursor.fetchall()
        sold_to_customers = [str(result[0]) for result in all_results]
        return first_result, sold_to_customers

    def save_all_changes(self, values):
        query = "UPDATE customers SET sold_to_customer = ?, agent_person = ?, company_code_n = ?, customer_name = ?, indirect_direct = ?, channel = ?, type = ?, tier = ?, tier_new = ?, Comments = ? WHERE sold_to_customer = ?"
        values_updated = values
        print("Saving changes...")
        self.cursor.execute(query, values_updated)
        self.connection.commit()
        print("Changes saved!")


class MainWindow(QMainWindow):
    def __init__(self, db_manager):
        super().__init__()
        self.setWindowTitle("Company Corrector")
        self.resize(400, 200)
        self.db_manager = db_manager

        # Add a new variable to store the original word
        self.original_company = None

        self.search_label = QLabel("Search company:")
        self.search_input = QLineEdit()
        self.search_input.textChanged.connect(self.clear_status_label)
        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.search_company_like)

        # Create fields and labels
        self.field_names = ['sold_to_customer', 'agent_person', 'company_code_n', 'customer_name', 'indirect_direct', 'channel', 'type', 'tier', 'tier_new', 'Comments']
        self.fields = []
        self.labels = []

        for field_name in self.field_names:
            label = QLabel(field_name + ":")
            field = QLineEdit()

            self.labels.append(label)
            self.fields.append(field)

        # Create buttons
        self.save_button = QPushButton("Save")
        self.close_button = QPushButton("Close")

        self.result_label = QLabel("Search result:")



        self.layout = QVBoxLayout()
        self.layout.addWidget(self.search_label)
        self.layout.addWidget(self.search_input)
        self.layout.addWidget(self.search_button)
        self.layout.addWidget(self.result_label)

        for label, field in zip(self.labels, self.fields):
            self.layout.addWidget(label)
            self.layout.addWidget(field)

        self.progress_label = QLabel("")

        self.layout.addWidget(self.save_button)
        self.layout.addWidget(self.close_button)
        self.layout.addWidget(self.progress_label)

        self.progress_label.setTextInteractionFlags(Qt.TextSelectableByMouse)

        self.central_widget = QWidget()
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

        # Connect button signals
        self.search_input.returnPressed.connect(self.search_button.click)

        self.save_button.clicked.connect(self.save_changes)
        self.close_button.clicked.connect(self.closeme)

    def search_company_like(self):
        self.progress_label.setText('')
        search_term = self.search_input.text()

        if not search_term:
            return

        result, sold_to_customers_list = self.db_manager.search_company(search_term)
        if result is None:
            # No matching record found
            for field in self.fields:
                field.clear()
            self.original_company = None  # Clear the original word
        else:
            # Update the fields with the fetched values
            for field, value in zip(self.fields, result):
                field.setText(str(value))
            self.original_company = result[0]
            self.progress_label.setText(', \n'.join(sold_to_customers_list))
            print(self.original_company)

    def save_changes(self):
        # Check if there is a word to update
        if self.original_company is None:
            return

        # Get the new values from the fields
        new_values = [field.text() for field in self.fields] + [self.original_company]

        # Check if the fields are empty
        if not all(new_values):
            return

        self.db_manager.save_all_changes(new_values)
        self.progress_label.setText('Changes saved!')

    def clear_status_label(self):
        self.progress_label.clear()

    def closeme(self):
        self.close()

    def closeEvent(self, event):
        self.db_manager.disconnect()
        event.accept()



if __name__ == '__main__':
    app = QApplication(sys.argv)

    #db_manager = DatabaseManager()
    #db_manager.connect("data_files/customer_data.db")

    # Prompt the user to select the database file
    file_dialog = QFileDialog()
    db_file, _ = file_dialog.getOpenFileName(None, "Select Database File", "", "SQLite Database Files (*.db)")

    if not db_file:
        sys.exit()

    db_manager = DatabaseManager()
    db_manager.connect(db_file)

    window = MainWindow(db_manager)
    window.move(100, 100)
    window.show()

    sys.exit(app.exec_())