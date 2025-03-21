import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QGridLayout,
    QPushButton, QComboBox, QLabel, QLineEdit
)

class MetamaterialCalculator(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Metamaterial Calculator")
        self.setGeometry(100, 100, 800, 500)


        widget = QWidget()
        self.setCentralWidget(widget)
        main_layout = QVBoxLayout()
        grid_layout = QGridLayout()


        material_label = QLabel("Select Materials")
        self.material_combo = QComboBox()
        self.material_combo.addItems(["Foam-Aluminum", "22", "33", "44"])
        grid_layout.addWidget(material_label, 0, 0)
        grid_layout.addWidget(self.material_combo, 0, 1, 1, 3)


        self.thickness_input = QLineEdit()
        self.loss_factor_input = QLineEdit()
        self.vcl_input = QLineEdit()
        self.static_young_input = QLineEdit()
        self.tcl_input = QLineEdit()
        self.poisson_input = QLineEdit()
        self.tor_input = QLineEdit()
        self.density_input = QLineEdit()
        self.phi_input = QLineEdit()
        self.rho1_input = QLineEdit()
        self.sigma_input = QLineEdit()
        self.eta_input = QLineEdit()
        self.nu_input = QLineEdit()

        grid_layout.addWidget(QLabel("Thickness"), 1, 0)
        grid_layout.addWidget(self.thickness_input, 1, 1)
        grid_layout.addWidget(QLabel("Loss Factor"), 1, 2)
        grid_layout.addWidget(self.loss_factor_input, 1, 3)

        grid_layout.addWidget(QLabel("VCL"), 2, 0)
        grid_layout.addWidget(self.vcl_input, 2, 1)
        grid_layout.addWidget(QLabel("Static Young's Modulus"), 2, 2)
        grid_layout.addWidget(self.static_young_input, 2, 3)

        grid_layout.addWidget(QLabel("TCL"), 3, 0)
        grid_layout.addWidget(self.tcl_input, 3, 1)
        grid_layout.addWidget(QLabel("Poisson's Ratio"), 3, 2)
        grid_layout.addWidget(self.poisson_input, 3, 3)

        grid_layout.addWidget(QLabel("TOR"), 4, 0)
        grid_layout.addWidget(self.tor_input, 4, 1)
        grid_layout.addWidget(QLabel("Density"), 4, 2)
        grid_layout.addWidget(self.density_input, 4, 3)

        grid_layout.addWidget(QLabel("Phi"), 5, 0)
        grid_layout.addWidget(self.phi_input, 5, 1)
        grid_layout.addWidget(QLabel("Rho1"), 5, 2)
        grid_layout.addWidget(self.rho1_input, 5, 3)

        grid_layout.addWidget(QLabel("Sigma"), 6, 0)
        grid_layout.addWidget(self.sigma_input, 6, 1)
        grid_layout.addWidget(QLabel("Eta"), 6, 2)
        grid_layout.addWidget(self.eta_input, 6, 3)

        grid_layout.addWidget(QLabel("Nu"), 7, 0)
        grid_layout.addWidget(self.nu_input, 7, 1)


        self.calculate_btn = QPushButton("Calculate")
        self.calculate_btn.clicked.connect(self.calculate)
        main_layout.addLayout(grid_layout)
        main_layout.addWidget(self.calculate_btn)
        widget.setLayout(main_layout)

    def calculate(self):
        print("Calculation done!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MetamaterialCalculator()
    window.show()
    app.exec()
