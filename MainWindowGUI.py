# here is the GUI for the app: version 0
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QScrollArea, QLineEdit
from PyQt6.QtWidgets import QLabel

from GUI_elements import CustomButton
from structures.MaterialType import PorousMaterial, SolidMaterial


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        porous_material = PorousMaterial()
        solid_material = SolidMaterial()
        material_gui = MaterialPropertiesGUI(porous_material)
        material_gui.set_material(solid_material)

        # self.material = PorousMaterial(update_callback=update_material_ui)
        # here need to add only gui element with material parameters

        # material layers would be stored as list ? or dictionary ?
        # at least 2 materials in the list
        # del list[index] or list.pop(index) to remove
        # but need to think about Exceptions for correct length of the list




class MaterialPropertiesGUI(QWidget):
    def __init__(self, material_instance):
        super().__init__()

        self.material = material_instance
        self.material.update_callback = self.update_material_ui

        self.textboxes = {}
        self.params_layout = QVBoxLayout()
        self.setup_ui()
        self.setLayout(self.params_layout)

    def setup_ui(self):
        for prop in self.material._properties.keys():
            label = QLabel(prop.replace("_", " ").capitalize())  # Label for readability
            textbox = QLineEdit()

            self.textboxes[prop] = textbox
            textbox.textChanged.connect(lambda _, key=prop: self.update_material_from_ui(key))

            self.params_layout.addWidget(label)
            self.params_layout.addWidget(textbox)

    def update_material_ui(self, property_name, value):
        if property_name in self.textboxes:
            self.textboxes[property_name].setText(str(value))  # Auto-update the text field

    def update_material_from_ui(self, property_name):
        try:
            self.material.set_property(property_name, float(self.textboxes[property_name].text()))
        except ValueError:
            pass

    def set_material(self, new_material):
        """To easily change material type for the layer"""
        self.material = new_material
        self.material.update_callback = self.update_material_ui  # rebind callback

        for i in reversed(range(self.params_layout.count())):
            self.params_layout.itemAt(i).widget().deleteLater()

        self.textboxes.clear()
        self.setup_ui()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())