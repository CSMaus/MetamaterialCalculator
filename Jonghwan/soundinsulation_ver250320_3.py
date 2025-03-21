from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QGroupBox, QLabel, QLineEdit, QPushButton, QSpacerItem, QSizePolicy
)
import sys


class SoundInsulationUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sound Insulation Performance")  # Set window title
        self.setGeometry(100, 100, 1050, 500)  # Set window size (x, y, width, height)

        central_widget = QWidget()  # Create the main central widget
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout()  # Use a horizontal layout for main content
        central_widget.setLayout(main_layout)

        # Create the left panel for material property inputs
        self.property_panel = QGroupBox("Material Properties")  # Group box for material properties
        self.property_panel.setFixedSize(800, 500)  # Set fixed size for the panel (width, height)
        property_layout = QGridLayout()  # Use a grid layout for the input fields
        self.property_panel.setLayout(property_layout)
        main_layout.addWidget(self.property_panel)  # Add panel to the main layout

        # Define labels for material properties (first 9 entries)
        labels_foam_9 = [
            "Thickness", "VCL", "TCL", "TOR",
            "Phi", "Rho", "Sigma",
            "Eta", "Nu"
        ]
        # Define labels for material properties (last 5 entries)
        labels_foam_5 = [
            "Etast", "E0st", "Vst",
            "Rost", "Hp"
        ]

        self.fields = []  # List to store field widgets

        # Add first 9 fields in columns 0 and 1
        for i, label_text in enumerate(labels_foam_9):
            label = QLabel(label_text)  # Create label
            field = QLineEdit()  # Create input field
            self.fields.append((label, field))
            property_layout.addWidget(label, i, 0)  # Place label at row i, column 0
            property_layout.addWidget(field, i, 1)  # Place input field at row i, column 1

        # Add remaining 5 fields in columns 2 and 3
        for i, label_text in enumerate(labels_foam_5):
            label = QLabel(label_text)  # Create label
            field = QLineEdit()  # Create input field
            self.fields.append((label, field))
            property_layout.addWidget(label, i, 2)  # Place label at row i, column 2
            property_layout.addWidget(field, i, 3)  # Place input field at row i, column 3

        # Create right panel for actions (buttons, etc.)
        self.button_panel = QGroupBox("Actions")  # Group box for actions
        self.button_panel.setFixedSize(200, 500)  # Set fixed size for button panel (width, height)
        button_layout = QVBoxLayout()  # Use a vertical layout for buttons
        self.button_panel.setLayout(button_layout)
        main_layout.addWidget(self.button_panel)  # Add button panel to main layout

        # Add 'Calculate' button
        self.calculate_button = QPushButton("Calculate")  # Create button
        self.calculate_button.clicked.connect(self.perform_calculation)  # Connect button click event
        button_layout.addWidget(self.calculate_button)  # Add button to the panel

        # Add extra space below button for future additions
        button_layout.addItem(
            QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))  # Add vertical spacer

    def perform_calculation(self):
        print("Performing calculation...")  # Print message when 'Calculate' button is clicked


if __name__ == "__main__":
    app = QApplication(sys.argv)  # Create application instance
    window = SoundInsulationUI()  # Create main window
    window.show()  # Show window
    sys.exit(app.exec())  # Execute application event loop
 