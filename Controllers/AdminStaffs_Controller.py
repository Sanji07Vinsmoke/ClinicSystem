from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QMessageBox
from Views.Admin_Staffs import Ui_MainWindow as AdminStaffsUI
from PyQt5 import QtCore
from Controllers.AdminAddUser_Controller import AdminAddUserController
from Models.Staff import Staff
from Models.Doctor import Doctor

class AdminStaffsController(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = AdminStaffsUI()
        self.ui.setupUi(self)

        print("Admin Staffs UI initialized!")

        # Connect buttons
        if hasattr(self.ui, 'AddUserButton'):
            print("AddUserButton exists")
            self.ui.AddUserButton.clicked.connect(self.open_add_user_form)
            print("AddUserButton connected to open_add_user_form!")
        else:
            print("AddUserButton is missing!")

        if hasattr(self.ui, 'DashboardButton'):
            print("DashboardButton exists")
            self.ui.DashboardButton.clicked.connect(self.ViewDashboard)
        else:
            print('DashboardButton is missing')

        if hasattr(self.ui, 'ChargesButton'):
            print("ChargesButton exists")
            self.ui.ChargesButton.clicked.connect(self.ViewCharges)
        else:
            print('ChargesButton is missing')

        # Apply styles to the tables
        self.apply_table_styles()
        self.refresh_tables()

    def ViewDashboard(self):
        print("DashboardButton clicked!")
        try:
            from Controllers.AdminDashboard_Controller import AdminDashboardController
            self.admin_dashboard_controller = AdminDashboardController()
            self.admin_dashboard_controller.show()
            self.hide()
        except Exception as e:
            print(f"Error loading tables: {e}")
            QMessageBox.critical(self, "Error", f"Failed to load tables: {e}")

    def ViewCharges(self):
        print("ChargesButton clicked!")
        try:
            from Controllers.AdminCharges_Controller import AdminChargesController
            self.admin_charges_controller = AdminChargesController()
            self.admin_charges_controller.show()
            self.hide()
        except Exception as e:
            print(f"Error loading tables: {e}")
            QMessageBox.critical(self, "Error", f"Failed to load tables: {e}")

    def refresh_tables(self):
        """Reload data into the tables"""
        try:
            self.load_doctor_table()
            self.load_staff_table()
            print("Tables refreshed successfully!")
        except Exception as e:
            print(f"Error refreshing tables: {e}")
            QMessageBox.critical(self, "Error", f"Failed to refresh tables: {e}")

    def apply_table_styles(self):
        """Apply custom styles to the tables"""
        # Style for StaffTable
        self.ui.StaffTable.setStyleSheet("""
                       QTableWidget {
            background-color: #F4F7ED;
            gridline-color: transparent;
            border-radius: 10px;
        }
        QTableWidget::item {
            border: none;
            font: 16pt "Lexend";
        }
        QTableWidget::item:selected {
            background-color: rgba(46, 110, 101, 0.3);
        }
        QTableWidget QHeaderView::section {
            background-color: #2E6E65;
            color: white;
            padding: 5px;
            font: 18px "Lexend Medium";
            border: 2px solid #2E6E65;
        }
        
        Scroll Area CSS
        QScrollBar:vertical {
             background: transparent;
             width: 10px;
            border-radius: 5px;
        }
        QScrollBar::handle:vertical {
                background: #C0C0C0;
                border-radius: 5px;
        }
        QScrollBar::handle:vertical:hover {
                background: #A0A0A0;
        }
        QScrollBar::add-line:vertical,
        QScrollBar::sub-line:vertical{
                background: none;
                border: none;
        }
           """)
        self.ui.StaffTable.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)

        # Style for DoctorTable
        self.ui.DoctorTable.setStyleSheet("""
               QTableWidget {
                background-color: #F4F7ED;
                gridline-color: transparent;
                border-radius: 10px;
            }
            QTableWidget::item {
                border: none;
                font: 16pt "Lexend";
            }
            QTableWidget::item:selected {
                background-color: rgba(46, 110, 101, 0.3);
            }
            QTableWidget QHeaderView::section {
                background-color: #2E6E65;
                color: white;
                padding: 5px;
                font: 18px "Lexend Medium";
                border: 2px solid #2E6E65;
            }
            
            Scroll Area CSS
            QScrollBar:vertical {
                 background: transparent;
                 width: 10px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                    background: #C0C0C0;
                    border-radius: 5px;
            }
            QScrollBar::handle:vertical:hover {
                    background: #A0A0A0;
            }
            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical{
                    background: none;
                    border: none;
            }
           """)
        self.ui.DoctorTable.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)

    def load_doctor_table(self):
        """Load doctor data into the DoctorTable"""
        doctors = Doctor.get_all_doctors_()
        self.ui.DoctorTable.setRowCount(len(doctors))

        # Remove row numbering
        self.ui.DoctorTable.verticalHeader().setVisible(False)

        # Set font color for header
        self.ui.DoctorTable.horizontalHeader().setDefaultAlignment(QtCore.Qt.AlignLeft)
        self.ui.DoctorTable.horizontalHeader().setStyleSheet(
            """
            QHeaderView::section {
                background-color: #2E6E65;
                color: white;
                padding: 5px;
                font: 14px "Lexend Medium";
                border: 2px solid #2E6E65;
            }
            """
        )

        # Populate the table
        for row, doctor in enumerate(doctors):
            # Insert ID
            self.ui.DoctorTable.setItem(row, 0, QTableWidgetItem(str(doctor["id"])))
            # Insert Name
            self.ui.DoctorTable.setItem(row, 1, QTableWidgetItem(doctor["name"]))
            # Insert Specialty
            self.ui.DoctorTable.setItem(row, 2, QTableWidgetItem(doctor["specialty"]))

    def load_staff_table(self):
        """Load staff data into the StaffTable"""
        staff_list = Staff.get_all_staff()
        self.ui.StaffTable.setRowCount(len(staff_list))

        # Remove row numbering
        self.ui.StaffTable.verticalHeader().setVisible(False)

        # Set font color for header
        self.ui.StaffTable.horizontalHeader().setDefaultAlignment(QtCore.Qt.AlignLeft)
        self.ui.StaffTable.horizontalHeader().setStyleSheet(
            """
            QHeaderView::section {
                background-color: #2E6E65;
                color: white;
                padding: 5px;
                font: 14px "Lexend Medium";
                border: 2px solid #2E6E65;
            }
            """
        )

        # Populate the table
        for row, staff in enumerate(staff_list):
            # Insert ID
            self.ui.StaffTable.setItem(row, 0, QTableWidgetItem(str(staff["id"])))
            # Insert Name
            self.ui.StaffTable.setItem(row, 1, QTableWidgetItem(staff["name"]))

    def open_add_user_form(self):
        print("Opening Add User Form...")
        try:
            self.add_user_window = AdminAddUserController(parent=self)
            self.add_user_window.show()
            print("Add User Form shown successfully!")
        except Exception as e:
            print(f"Error opening Add User Form: {e}")