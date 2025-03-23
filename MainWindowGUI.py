# here is the GUI for the app: version 0
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QScrollArea, QLineEdit, \
    QComboBox
from PyQt6.QtWidgets import QLabel
from torch.utils.data.datapipes.gen_pyi import materialize_lines

from GUI_elements import CustomButton
from structures.MaterialType import PorousMaterial, SolidMaterial

# later need to implement read from database
# at least one material in layers
# later to replace it to dictionary with calculation results
# layers would be dictionary to interactive any position change of layer
layers = {}
selected_layer = ""


class MainWindow(QWidget):
    global layers
    def __init__(self):
        super().__init__()

        self.porous_material = PorousMaterial()
        self.solid_material = SolidMaterial()
        self.material_gui = MaterialPropertiesGUI(self.porous_material)
        # self.material_gui.set_material(self.solid_material)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.material_gui)

        layout = QVBoxLayout()
        layout.addWidget(self.scroll_area)
        self.setLayout(layout)

        # self.material = PorousMaterial(update_callback=update_material_ui)
        # here need to add only gui element with material parameters

        # material layers would be stored as list ? or dictionary ?
        # at least 2 materials in the list
        # del list[index] or list.pop(index) to remove
        # but need to think about Exceptions for correct length of the list

        # TODO: need to implement event catch when we select some layer
        # from layers global variable
        # and based on this layer material we have to update material
        # where material is layers[selected_layer_key]

    def update_material_panel(self, material):
        self.material_gui.set_material(material)


class LayersStructureGUI(QWidget):
    global layers
    def __init__(self):
        super().__init__()
        main_layout = QVBoxLayout(self)
        self.control_panel = QWidget(self)
        control_layout = QHBoxLayout(self.control_panel)

        self.material_types = QComboBox()
        self.material_types.addItems(["Porous", "Solid"])
        control_layout.addWidget(self.material_types)

        self.thickness = QLineEdit()
        self.thickness.setText("10")
        control_layout.addWidget(self.thickness)
        self.thickness_unit = QLabel()
        self.thickness_unit.setText("mm")
        control_layout.addWidget(self.thickness_unit)

        self.add_layer = QPushButton("Add Layer", self)
        self.add_layer.clicked.connect(self.add_dynamic_layer)
        control_layout.addWidget(self.add_layer)

        main_layout.addWidget(self.control_panel)
        main_layout.setAlignment(control_layout)  # add here right alignment

        self.solid_image = "solid.png"
        self.porous_image = "porous.png"

        self.scroll_area = QScrollArea(self)
        self.scroll_widget = QWidget()
        self.layers_layout = QHBoxLayout(self.scroll_widget)
        self.scroll_widget.setLayout(self.layers_layout)
        self.scroll_area.setWidget(self.scroll_widget)
        self.scroll_area.setWidgetResizable(True)

        self.layers_buttons = []  # this is Buttons looks like images
        # self.update_layers_gui()

    def add_dynamic_layer(self):
        index = len(layers.keys())
        layer_key = f'{index}'
        material_type = self.material_types.currentText()

        if material_type == "Porous":
            layer_material = PorousMaterial()
            layers[layer_key] = {"material_type": material_type,
                                 "thickness": self.thickness,
                                 "material_params": layer_material}
        else:
            layer_material = SolidMaterial
            layers[layer_key] = {"material_type": material_type,
                                 "thickness": self.thickness,
                                 "material_params": layer_material}

        self.update_layers_gui()

    def update_layers_gui(self):
        # TODO: sort keys by increasing index number
        for layer_key in layers.keys():
            material_type = layers[layer_key]["material_type"]
            index = int(float(layer_key))
            image_path = self.porous_image if material_type == "Porous" else self.solid_image
            new_layer_btn = CustomButton(index, image_path, self.layers_layout, None)
            self.layers_layout.addWidget(new_layer_btn.button if isinstance(new_layer_btn, CustomButton) else new_layer_btn)
            self.layers_buttons.append(new_layer_btn)

    def load_layers_structure(self, layers_structure_DB):
        # TODO: here will code implementation to read the structure as dict
        # TODO: which will store thickness and material properties for each layer
        layers.clear()
        for layer_key in layers_structure_DB.keys():
            # load layers structure from DataBase and fill this variable
            layers[layer_key] = layers_structure_DB[layer_key]
            # layers.append(layer_item)



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
        self.setup_ui() # rebuild gui for new mat

        #  set properties values for text boxes corresponding material
        for prop, value in self.material._properties.items():
            if prop in self.textboxes:
                self.textboxes[prop].setText(str(value) if value is not None else "")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())