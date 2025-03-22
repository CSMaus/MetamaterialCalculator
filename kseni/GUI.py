# here is my GUI for the calculator with material structure, etc
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
from backend.crud import get_materials, insert_material

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Metamaterial Properties Calculator")
        self.initUI()

    def initUI(self):
        self.button = QPushButton("Fetch Materials")
        self.button.clicked.connect(self.fetch_data)

        layout = QVBoxLayout()
        layout.addWidget(self.button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def fetch_data(self):
        df = get_materials()
        print(df)  # for now just print in console

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()

