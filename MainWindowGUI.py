# here is the GUI for the app: version 0
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QScrollArea, QLineEdit, \
    QComboBox
from PyQt6.QtWidgets import QLabel, QSizePolicy, QGridLayout
from PyQt6.QtCore import Qt
from torch.utils.data.datapipes.gen_pyi import materialize_lines

from GUI_elements import CustomButton, CustomButton2
from structures.MaterialType import PorousMaterial, SolidMaterial

# later need to implement read from database
# at least one material in layers
# later to replace it to dictionary with calculation results
# layers would be dictionary to interactive any position change of layer
layers = {}
selected_layer = "0"


class MainWindow(QWidget):
    global layers
    def __init__(self):
        super().__init__()

        # self.porous_material = PorousMaterial()
        # self.solid_material = SolidMaterial()
        # self.material_gui = MaterialPropertiesGUI(self.porous_material)
        # self.material_gui.set_material(self.solid_material)
        self.material_gui = MaterialPropertiesGUI(layers[selected_layer]["material_params"])

        self.layers_gui = LayersStructureGUI(self)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.material_gui)

        layout = QVBoxLayout()
        layout.addWidget(self.layers_gui)
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

# TODO: todo: fix the layers to be aligned to each other wihtout spacing
class LayersStructureGUI(QWidget):
    global layers
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
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

        self.scroll_area = QScrollArea(self)
        self.scroll_widget = QWidget()
        self.layers_layout = QHBoxLayout(self.scroll_widget)
        self.layers_layout.setSpacing(0)
        self.layers_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        # self.layers_layout = QGridLayout(self.scroll_widget) #  QHBoxLayout QGridLayout

        self.scroll_widget.setLayout(self.layers_layout)
        self.scroll_area.setWidget(self.scroll_widget)
        self.scroll_area.setWidgetResizable(True)
        main_layout.addWidget(self.scroll_area)

        self.solid_image = "solid.png"
        self.porous_image = "porous.png"
        self.layers_buttons = []  # this is Buttons that looks like images

        self.update_layers_gui()

    def add_dynamic_layer(self):
        global selected_layer

        index = len(layers.keys())
        layer_key = str(index)
        material_type = self.material_types.currentText()

        if material_type == "Porous":
            layer_material = PorousMaterial()
            # image_path = self.porous_image
        else:
            layer_material = SolidMaterial()
            # image_path = self.solid_image

        layers[layer_key] = {"material_type": material_type,
                             "thickness": self.thickness.text(),
                             "material_params": layer_material}
        selected_layer = layer_key
        self.update_layers_gui()
        self.main_window.update_material_panel(layers[selected_layer]["material_params"])


    def update_layers_gui(self):
        # TODO: sort keys by increasing index number

        # for ease remake all gui for layers
        # remove existing buttons before updating
        '''for i in reversed(range(self.layers_layout.count())):
            self.layers_layout.itemAt(i).widget().deleteLater()
        self.layers_buttons.clear()'''

        while self.layers_layout.count():
            item = self.layers_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                self.clear_layout(item.layout())

        sorted_keys = sorted(layers.keys(), key=lambda x: int(x))
        for col_index, layer_key in enumerate(sorted_keys):
            thickness_val = layers[layer_key]["thickness"]

            material_type = layers[layer_key]["material_type"]
            image_path = self.porous_image if material_type == "Porous" else self.solid_image
            new_layer_btn = CustomButton2(int(layer_key), image_path, self.layers_layout, self.change_selected_layer)

            layer_container = QVBoxLayout()
            layer_container_width = new_layer_btn.button.sizeHint().width()

            thickness_input = QLineEdit(str(thickness_val))
            thickness_input.textChanged.connect(self.create_thickness_update_callback(layer_key, thickness_input))
            thickness_unit_label = QLabel("mm")
            thickness_unit_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

            label_width = thickness_unit_label.sizeHint().width()

            thickness_input.setFixedWidth(layer_container_width - label_width)
            thickness_input.setAlignment(Qt.AlignmentFlag.AlignLeft)
            thickness_input.setStyleSheet("padding: 0px; border: 1px solid gray;")

            thickness_layout = QHBoxLayout()
            thickness_layout.setSpacing(0)
            thickness_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
            thickness_layout.addWidget(thickness_input)
            thickness_layout.addWidget(thickness_unit_label)
            layer_container.addLayout(thickness_layout)

            layer_container.addWidget(new_layer_btn.button, alignment=Qt.AlignmentFlag.AlignLeft)

            self.layers_layout.addLayout(layer_container)
            self.layers_buttons.append(new_layer_btn)

    def clear_layout(self, layout):
        """Recursively removes all widgets and layouts inside a layout."""
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                self.clear_layout(item.layout())

    def create_thickness_update_callback(self, layer_key, thickness_input):
        """Fixes lambda scope issue and properly updates thickness."""
        def callback():
            self.update_thickness(layer_key, thickness_input.text())
        return callback

    def update_thickness(self, layer_key, value):
        try:
            layers[layer_key]["thickness"] = float(value)
        except ValueError:
            pass  # Ignore invalid inputs (e.g., empty field)

    def change_selected_layer(self, dynamic_layer):
        global selected_layer

        # if isinstance(dynamic_layer, CustomButton):
        layer_index = str(dynamic_layer.index)
        selected_layer = f'{layer_index}'
        self.main_window.update_material_panel(layers[selected_layer]["material_params"])

    def load_layers_structure(self, layers_structure_DB):
        # TODO: here will code implementation to read the structure as dict
        # TODO: which will store thickness and material properties for each layer
        layers.clear()
        for layer_key in layers_structure_DB.keys():
            # load layers structure from DataBase and fill this variable
            # layers.append(layer_item)
            layers[layer_key] = layers_structure_DB[layer_key]

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
    layers["0"] = {"material_type": "Porous",
                         "thickness": "10",
                         "material_params": PorousMaterial()}
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())