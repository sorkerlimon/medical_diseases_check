# data_loading_tab.py
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QGroupBox, 
                            QTableWidget, QTableWidgetItem, QMessageBox, 
                            QDialog, QFormLayout, QLineEdit, QDialogButtonBox,QHBoxLayout,QLabel,QFileDialog)
from database import DatabaseManager
import sqlite3
from pathlib import Path
import shutil
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

class ImageDelegate(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(50, 50)
        self.setScaledContents(True)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
class InsertPatientDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.selected_image_path = None
        self.setup_ui()
    
    def setup_ui(self):
        self.setWindowTitle("Insert New Patient Data")
        self.setMinimumWidth(400)
        layout = QFormLayout(self)
        
        # Create input fields
        self.name_input = QLineEdit()
        self.age_input = QLineEdit()
        self.gender_input = QLineEdit()
        self.contact_input = QLineEdit()
        
        # Image upload section
        image_layout = QHBoxLayout()
        
        # Image preview label
        self.preview_label = QLabel()
        self.preview_label.setFixedSize(100, 100)
        self.preview_label.setScaledContents(True)
        self.preview_label.setStyleSheet("border: 1px solid gray;")
        
        # Upload button
        self.upload_button = QPushButton("Upload Image")
        self.upload_button.clicked.connect(self.upload_image)
        
        image_layout.addWidget(self.preview_label)
        image_layout.addWidget(self.upload_button)
        
        # Add fields to form
        layout.addRow("Patient Name:", self.name_input)
        layout.addRow("Patient Age:", self.age_input)
        layout.addRow("Patient Gender:", self.gender_input)
        layout.addRow("Patient Contact:", self.contact_input)
        layout.addRow("Patient Image:", image_layout)
        
        # Add OK/Cancel buttons
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | 
            QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addRow(button_box)
    
    def upload_image(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Select Image",
            "",
            "Image Files (*.png *.jpg *.jpeg)"
        )
        if file_name:
            self.selected_image_path = file_name
            pixmap = QPixmap(file_name)
            self.preview_label.setPixmap(pixmap.scaled(100, 100))
    
    def get_data(self):
        return {
            'patient_name': self.name_input.text(),
            'patient_age': self.age_input.text(),
            'patient_gender': self.gender_input.text(),
            'patient_contact': self.contact_input.text(),
            'patient_image': self.selected_image_path
        }


class DataLoadingTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.db = DatabaseManager()
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Data source group
        source_group = QGroupBox("Data Source")
        source_layout = QVBoxLayout(source_group)
        
        self.connect_db_btn = QPushButton("Connect to Database")
        self.connect_db_btn.clicked.connect(self.connect_to_database)
        
        source_layout.addWidget(self.connect_db_btn)
        
        # Database operations group
        db_group = QGroupBox("Database Operations")
        db_layout = QVBoxLayout(db_group)
        
        # Create operation buttons with connections
        self.insert_btn = QPushButton("Insert New Data")
        self.retrieve_btn = QPushButton("Retrieve Data")
        self.update_btn = QPushButton("Update Data")
        self.delete_btn = QPushButton("Delete Data")
        
        self.insert_btn.clicked.connect(self.insert_data)
        self.retrieve_btn.clicked.connect(self.retrieve_data)
        self.update_btn.clicked.connect(self.update_data)
        self.delete_btn.clicked.connect(self.delete_data)
        
        for btn in [self.insert_btn, self.retrieve_btn, self.update_btn, self.delete_btn]:
            db_layout.addWidget(btn)
            btn.setEnabled(False)  # Disabled until database connection
        
        # Table view
        self.table = QTableWidget()
        
        # Add all to main layout
        layout.addWidget(source_group)
        layout.addWidget(db_group)
        layout.addWidget(self.table)
    
    def connect_to_database(self):
        if self.db.connect():
            QMessageBox.information(self, "Success", "Connected to database successfully!")
            for btn in [self.insert_btn, self.retrieve_btn, self.update_btn, self.delete_btn]:
                btn.setEnabled(True)
            self.connect_db_btn.setEnabled(False)
        else:
            QMessageBox.critical(self, "Error", "Failed to connect to database!")

    # def insert_data(self):
    #     try:
    #         # Fetch table schema dynamically
    #         self.db.cursor.execute("PRAGMA table_info(patients)")
    #         columns = self.db.cursor.fetchall()
            
    #         if not columns:
    #             QMessageBox.warning(self, "Warning", "No columns found in the 'patients' table.")
    #             return
            
    #         # Open a custom dialog for data input
    #         dialog = QDialog(self)
    #         dialog.setWindowTitle("Insert New Data")
            
    #         form_layout = QFormLayout(dialog)
    #         input_fields = {}
            
    #         # Create input fields for each column except auto-handled ones
    #         for column in columns:
    #             col_name = column[1]
    #             col_type = column[2]
    #             default_value = column[4]  # Default value for the column
                
    #             # Skip auto-handled columns (id and created_at)
    #             if col_name in ["id", "created_at"]:
    #                 continue
                
    #             # Create a QLineEdit for each column
    #             input_field = QLineEdit()
    #             if default_value is not None:
    #                 input_field.setPlaceholderText(f"Default: {default_value}")
                
    #             # Save the input field for later reference
    #             input_fields[col_name] = input_field
    #             form_layout.addRow(col_name, input_field)
            
    #         # Add buttons for submission
    #         button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
    #         button_box.accepted.connect(dialog.accept)
    #         button_box.rejected.connect(dialog.reject)
    #         form_layout.addWidget(button_box)
            
    #         # Show dialog
    #         if dialog.exec():
    #             # Collect data from fields
    #             data = {col: field.text() for col, field in input_fields.items()}
                
    #             # Filter out empty fields
    #             filtered_data = {k: v for k, v in data.items() if v.strip() != ""}
                
    #             # Prepare and execute the insert query
    #             placeholders = ", ".join(["?"] * len(filtered_data))
    #             column_names = ", ".join(filtered_data.keys())
    #             query = f"INSERT INTO patients ({column_names}) VALUES ({placeholders})"
                
    #             # Execute query
    #             self.db.cursor.execute(query, tuple(filtered_data.values()))
    #             self.db.connection.commit()
                
    #             QMessageBox.information(self, "Success", "Data inserted successfully!")
    #             # self.retrieve_data()  # Refresh the table view
    #         else:
    #             QMessageBox.information(self, "Info", "Insertion canceled.")
        
    #     except sqlite3.Error as e:
    #         QMessageBox.critical(self, "Error", f"Failed to insert data: {str(e)}")



  
    def insert_data(self):
        try:
            dialog = InsertPatientDialog(self)
            
            if dialog.exec():
                data = dialog.get_data()
                
                # Handle image if uploaded
                if data['patient_image']:
                    # Create images directory if it doesn't exist
                    image_dir = Path("patient_images")
                    image_dir.mkdir(exist_ok=True)
                    
                    # Copy image to images directory with unique name
                    image_path = Path(data['patient_image'])
                    new_image_name = f"patient_{len(list(image_dir.glob('*')))}{image_path.suffix}"
                    new_image_path = image_dir / new_image_name
                    shutil.copy2(data['patient_image'], new_image_path)
                    
                    # Update image path in data
                    data['patient_image'] = str(new_image_name)
                
                # Filter out empty fields
                filtered_data = {k: v for k, v in data.items() if v and str(v).strip()}
                
                # Prepare and execute the insert query
                placeholders = ", ".join(["?"] * len(filtered_data))
                column_names = ", ".join(filtered_data.keys())
                query = f"INSERT INTO patients ({column_names}) VALUES ({placeholders})"
                
                # Execute query
                self.db.cursor.execute(query, tuple(filtered_data.values()))
                self.db.connection.commit()
                
                QMessageBox.information(self, "Success", "Patient data inserted successfully!")
                self.retrieve_data()  # Refresh the table view
            else:
                QMessageBox.information(self, "Info", "Insertion canceled.")
        
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Error", f"Failed to insert data: {str(e)}")

    # def retrieve_data(self):
    #     try:
    #         # Open a dialog to get filter criteria
    #         dialog = QDialog(self)
    #         dialog.setWindowTitle("Retrieve Data with Filters")
            
    #         form_layout = QFormLayout(dialog)
    #         filter_fields = {}
            
    #         # Define filter fields for 'id' and 'name'
    #         filter_fields['id'] = QLineEdit()
    #         filter_fields['name'] = QLineEdit()
            
    #         form_layout.addRow("ID (Leave blank for no filter):", filter_fields['id'])
    #         form_layout.addRow("Name (Leave blank for no filter):", filter_fields['name'])
            
    #         # Add buttons for submission
    #         button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
    #         button_box.accepted.connect(dialog.accept)
    #         button_box.rejected.connect(dialog.reject)
    #         form_layout.addWidget(button_box)
            
    #         # Show dialog
    #         if dialog.exec():
    #             # Collect filter values
    #             id_filter = filter_fields['id'].text().strip()
    #             name_filter = filter_fields['name'].text().strip()

    #                         # Check if both fields are blank
    #             if not id_filter and not name_filter:
    #                 QMessageBox.information(self, "Info", "No filters provided. Retrieving all data.")
                
                    
    #             # Construct the query with filters
    #             query = "SELECT * FROM patients WHERE 1=1"  # 1=1 ensures the query is always valid
    #             params = []
                
    #             if id_filter:
    #                 query += " AND id = ?"
    #                 params.append(id_filter)
                
    #             if name_filter:
    #                 query += " AND image_name LIKE ?"
    #                 params.append(f"%{name_filter}%")
                
    #             # Execute the query
    #             self.db.cursor.execute(query, params)
    #             data = self.db.cursor.fetchall()
                
    #             # Get column names
    #             columns = [description[0] for description in self.db.cursor.description]
                
    #             # Set up the table
    #             self.table.setRowCount(len(data))
    #             self.table.setColumnCount(len(columns))
    #             self.table.setHorizontalHeaderLabels(columns)
                
    #             # Fill table with data
    #             for row_idx, row_data in enumerate(data):
    #                 for col_idx, value in enumerate(row_data):
    #                     self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))
                        
    #             self.table.resizeColumnsToContents()
            
    #         else:
    #             QMessageBox.information(self, "Info", "Data retrieval canceled.")
        
    #     except sqlite3.Error as e:
    #         QMessageBox.critical(self, "Error", f"Failed to retrieve data: {str(e)}")


    def retrieve_data(self):
        try:
            # Open a dialog to get filter criteria
            dialog = QDialog(self)
            dialog.setWindowTitle("Retrieve Data with Filters")
            
            form_layout = QFormLayout(dialog)
            filter_fields = {}
            
            # Define filter fields for 'patient_id' and 'patient_name'
            filter_fields['patient_id'] = QLineEdit()
            filter_fields['patient_name'] = QLineEdit()
            
            form_layout.addRow("Patient ID (Leave blank for no filter):", filter_fields['patient_id'])
            form_layout.addRow("Patient Name (Leave blank for no filter):", filter_fields['patient_name'])
            
            # Add buttons for submission
            button_box = QDialogButtonBox(
                QDialogButtonBox.StandardButton.Ok | 
                QDialogButtonBox.StandardButton.Cancel
            )
            button_box.accepted.connect(dialog.accept)
            button_box.rejected.connect(dialog.reject)
            form_layout.addWidget(button_box)
            
            # Show dialog
            if dialog.exec():
                # Collect filter values
                id_filter = filter_fields['patient_id'].text().strip()
                name_filter = filter_fields['patient_name'].text().strip()

                # Check if both fields are blank
                if not id_filter and not name_filter:
                    QMessageBox.information(self, "Info", "No filters provided. Retrieving all data.")
                
                # Construct the query with filters
                query = "SELECT * FROM patients WHERE 1=1"  # 1=1 ensures the query is always valid
                params = []
                
                if id_filter:
                    query += " AND patient_id = ?"
                    params.append(id_filter)
                
                if name_filter:
                    query += " AND patient_name LIKE ?"
                    params.append(f"%{name_filter}%")
                
                # Execute the query
                self.db.cursor.execute(query, params)
                data = self.db.cursor.fetchall()
                
                # Get column names
                columns = [description[0] for description in self.db.cursor.description]
                
                # Set up the table
                self.table.setRowCount(len(data))
                self.table.setColumnCount(len(columns))
                self.table.setHorizontalHeaderLabels(columns)
                
                # Fill table with data
                for row_idx, row_data in enumerate(data):
                    for col_idx, value in enumerate(row_data):
                        if columns[col_idx] == 'patient_image' and value:
                            # Create cell widget for image
                            cell_widget = ImageDelegate(self.table)
                            image_path = Path("patient_images") / value
                            
                            if image_path.exists():
                                pixmap = QPixmap(str(image_path))
                                cell_widget.setPixmap(pixmap)
                                self.table.setCellWidget(row_idx, col_idx, cell_widget)
                            else:
                                self.table.setItem(row_idx, col_idx, 
                                                QTableWidgetItem("Image not found"))
                        else:
                            self.table.setItem(row_idx, col_idx, 
                                            QTableWidgetItem(str(value)))
                
                # Adjust row heights for images
                self.table.verticalHeader().setDefaultSectionSize(50)
                
                # Adjust column widths
                self.table.resizeColumnsToContents()
                
                # Add double-click handler for images
                self.table.cellDoubleClicked.connect(self.show_full_image)
            
            else:
                QMessageBox.information(self, "Info", "Data retrieval canceled.")
        
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Error", f"Failed to retrieve data: {str(e)}")

    def show_full_image(self, row, col):
        """Show full-size image when double-clicking a cell"""
        header_text = self.table.horizontalHeaderItem(col).text()
        if header_text == 'patient_image':
            image_name = self.table.item(row, col)
            if image_name and image_name.text():
                image_path = Path("patient_images") / image_name.text()
                if image_path.exists():
                    dialog = QDialog(self)
                    dialog.setWindowTitle("Full Image View")
                    layout = QVBoxLayout(dialog)
                    
                    # Create image label
                    image_label = QLabel()
                    pixmap = QPixmap(str(image_path))
                    
                    # Scale pixmap while maintaining aspect ratio
                    scaled_pixmap = pixmap.scaled(400, 400, 
                                                Qt.AspectRatioMode.KeepAspectRatio,
                                                Qt.TransformationMode.SmoothTransformation)
                    image_label.setPixmap(scaled_pixmap)
                    
                    layout.addWidget(image_label)
                    
                    # Add close button
                    close_button = QPushButton("Close")
                    close_button.clicked.connect(dialog.close)
                    layout.addWidget(close_button)
                    
                    dialog.exec()

    def update_data(self):
        try:
            # Open a dialog to get search criteria (id or name)
            search_dialog = QDialog(self)
            search_dialog.setWindowTitle("Search for Data to Update")
            
            search_layout = QFormLayout(search_dialog)
            search_fields = {}
            
            # Define search fields for 'id' and 'name'
            search_fields['id'] = QLineEdit()
            search_fields['name'] = QLineEdit()
            
            search_layout.addRow("ID (Leave blank for no filter):", search_fields['id'])
            search_layout.addRow("Name (Leave blank for no filter):", search_fields['name'])
            
            # Add buttons for submission
            button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
            button_box.accepted.connect(search_dialog.accept)
            button_box.rejected.connect(search_dialog.reject)
            search_layout.addWidget(button_box)
            
            # Show dialog
            if search_dialog.exec():
                # Collect search values
                id_filter = search_fields['id'].text().strip()
                name_filter = search_fields['name'].text().strip()
                
                # Construct the search query
                query = "SELECT * FROM patients WHERE 1=1"
                params = []
                
                if id_filter:
                    query += " AND id = ?"
                    params.append(id_filter)
                
                if name_filter:
                    query += " AND name LIKE ?"
                    params.append(f"%{name_filter}%")
                
                # Execute the search query
                self.db.cursor.execute(query, params)
                data = self.db.cursor.fetchall()
                
                if not data:
                    QMessageBox.information(self, "Info", "No matching records found.")
                    return
                
                # Display matching records to confirm
                record_info = "\n".join([", ".join(map(str, row)) for row in data])
                QMessageBox.information(self, "Matching Records", f"Found the following records:\n\n{record_info}")
                
                # Open a dialog to get update values
                update_dialog = QDialog(self)
                update_dialog.setWindowTitle("Update Data")
                
                update_layout = QFormLayout(update_dialog)
                update_fields = {}
                
                # Define update fields for 'name', 'age', and 'gender'
                update_fields['name'] = QLineEdit()
                update_fields['image_name'] = QLineEdit()
                update_fields['disease'] = QLineEdit()
                
                update_layout.addRow("New Name (Leave blank to keep current):", update_fields['name'])
                update_layout.addRow("image_name (Leave blank to keep current):", update_fields['image_name'])
                update_layout.addRow("disease (Leave blank to keep current):", update_fields['disease'])
                
                # Add buttons for submission
                update_button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
                update_button_box.accepted.connect(update_dialog.accept)
                update_button_box.rejected.connect(update_dialog.reject)
                update_layout.addWidget(update_button_box)
                
                # Show update dialog
                if update_dialog.exec():
                    # Collect update values
                    update_values = {field: update_fields[field].text().strip() for field in update_fields}
                    
                    # Construct the update query
                    update_query = "UPDATE patients SET "
                    update_params = []
                    
                    for field, value in update_values.items():
                        if value:  # Only include non-empty fields
                            update_query += f"{field} = ?, "
                            update_params.append(value)
                    
                    # Remove trailing comma and space
                    update_query = update_query.rstrip(", ")
                    
                    # Add WHERE clause to the query
                    update_query += " WHERE 1=1"
                    if id_filter:
                        update_query += " AND id = ?"
                        update_params.append(id_filter)
                    if name_filter:
                        update_query += " AND name LIKE ?"
                        update_params.append(f"%{name_filter}%")
                    
                    # Execute the update query
                    self.db.cursor.execute(update_query, update_params)
                    self.db.connection.commit()
                    
                    QMessageBox.information(self, "Success", "Data updated successfully!")
                    # self.retrieve_data()  # Refresh the view
                else:
                    QMessageBox.information(self, "Info", "Update canceled.")
            else:
                QMessageBox.information(self, "Info", "Search canceled.")
        
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Error", f"Failed to update data: {str(e)}")

        
    def delete_data(self):
        try:
            # Open a dialog to get search criteria (id or image_name)
            search_dialog = QDialog(self)
            search_dialog.setWindowTitle("Search for Data to Delete")
            
            search_layout = QFormLayout(search_dialog)
            search_fields = {}
            
            # Define search fields for 'id' and 'image_name'
            search_fields['id'] = QLineEdit()
            search_fields['image_name'] = QLineEdit()
            
            search_layout.addRow("ID (Leave blank for no filter):", search_fields['id'])
            search_layout.addRow("Image Name (Leave blank for no filter):", search_fields['image_name'])
            
            # Add buttons for submission
            button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
            button_box.accepted.connect(search_dialog.accept)
            button_box.rejected.connect(search_dialog.reject)
            search_layout.addWidget(button_box)
            
            # Show dialog
            if search_dialog.exec():
                # Collect search values
                id_filter = search_fields['id'].text().strip()
                image_name_filter = search_fields['image_name'].text().strip()
                
                # Construct the search query
                query = "SELECT * FROM patients WHERE 1=1"
                params = []
                
                if id_filter:
                    query += " AND id = ?"
                    params.append(id_filter)
                
                if image_name_filter:
                    query += " AND image_name LIKE ?"
                    params.append(f"%{image_name_filter}%")
                
                # Execute the search query
                self.db.cursor.execute(query, params)
                data = self.db.cursor.fetchall()
                
                if not data:
                    QMessageBox.information(self, "Info", "No matching records found.")
                    return
                
                # Display matching records to confirm
                record_info = "\n".join([", ".join(map(str, row)) for row in data])
                confirm = QMessageBox.question(
                    self,
                    "Confirm Deletion",
                    f"The following records will be deleted:\n\n{record_info}\n\nAre you sure?",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                )
                
                if confirm == QMessageBox.StandardButton.Yes:
                    # Construct the delete query
                    delete_query = "DELETE FROM patients WHERE 1=1"
                    delete_params = []
                    
                    if id_filter:
                        delete_query += " AND id = ?"
                        delete_params.append(id_filter)
                    
                    if image_name_filter:
                        delete_query += " AND image_name LIKE ?"
                        delete_params.append(f"%{image_name_filter}%")
                    
                    # Execute the delete query
                    self.db.cursor.execute(delete_query, delete_params)
                    self.db.connection.commit()
                    
                    QMessageBox.information(self, "Success", "Data deleted successfully!")
                    # self.retrieve_data()  # Refresh the table view
                else:
                    QMessageBox.information(self, "Info", "Deletion canceled.")
            else:
                QMessageBox.information(self, "Info", "Search canceled.")
        
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Error", f"Failed to delete data: {str(e)}")
