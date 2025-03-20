import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout

class MaterialCalculator(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Material Calculator")
        self.setGeometry(100, 100, 300, 200)


        layout = QVBoxLayout()


        self.label_thickness = QLabel('Thickness:')
        self.input_thickness = QLineEdit()

        self.label_density = QLabel('Density:')
        self.input_density = QLineEdit()

        self.label_young_modulus = QLabel("Young's Modulus:")
        self.input_young_modulus = QLineEdit()


        self.calculate_btn = QPushButton('Calculate')
        self.calculate_btn.clicked.connect(self.print_values)


        layout.addWidget(self.label_thickness)
        layout.addWidget(self.input_thickness)
        layout.addWidget(self.label_density)
        layout.addWidget(self.input_density)
        layout.addWidget(self.label_young_modulus)
        layout.addWidget(self.input_young_modulus)
        layout.addWidget(self.calculate_btn)

        self.setLayout(layout)

    def print_values(self):

        print("Thickness:", self.input_thickness.text())
        print("Density:", self.input_density.text())
        print("Young's Modulus:", self.input_young_modulus.text())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MaterialCalculator()
    window.show()
    sys.exit(app.exec())
