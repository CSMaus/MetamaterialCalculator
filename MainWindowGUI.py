# here is the GUI for the app: version 0
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QScrollArea, QLineEdit, \
    QComboBox
from PyQt6.QtWidgets import QLabel, QSizePolicy, QGridLayout
from PyQt6.QtCore import Qt, QSize
from torch.utils.data.datapipes.gen_pyi import materialize_lines
from GUI_elements import CustomButton, CustomButton2
from structures.MaterialType import PorousMaterial, SolidMaterial
from kseni.backend.crud import insert_material, get_materials, user_name
from kseni.backend.database import initialize_database

layers = {}
selected_layer = "0"

# TODO: load from database:
# new window where we will make a search of materials in DB by their names and produser names
# also, need to implement search, so in list there would be only ones,
# which combined name "{material_name} {producer_name}" contains search phrase in any part
# todo: do not forget to match the material type
# todo: also maybe we can make sort by material type before printing list of materials for search


class MainWindow(QWidget):
    global layers
    def __init__(self):
        super().__init__()

        self.material_gui = MaterialPropertiesGUI(layers[selected_layer]["material_params"])
        self.layers_gui = LayersStructureGUI(self)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.material_gui)

        self.add_material_lo = QHBoxLayout()
        self.add_material_lo.setSpacing(5)

        self.material_text = QLabel("Material name: ")
        self.material_name = QLineEdit()
        self.add_material_inDB = QPushButton("➕", self)
        self.add_material_inDB.clicked.connect(self.add_material_toDB)
        self.add_material_lo.addWidget(self.material_text)
        self.add_material_lo.addWidget(self.material_name)
        self.add_material_lo.addWidget(self.add_material_inDB)


        self.see_db = QPushButton("Print DB", self)
        self.see_db.clicked.connect(self.print_db)

        layout = QVBoxLayout()
        layout.addWidget(self.layers_gui)
        layout.addWidget(self.scroll_area)
        # layout.addWidget(self.add_material_inDB)
        layout.addLayout(self.add_material_lo)
        layout.addWidget(self.see_db)
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

    def add_material_toDB(self):
        property_dict = layers[selected_layer]["material_params"]._properties
        material_dict = {}
        for mkey in property_dict.keys():
            try:
                material_dict[mkey] = float(property_dict[mkey])
            except Exception as ex:
                print("All properties should be defined as numbers (float)")
                print(ex)
                material_dict[mkey] = 0

        material_name = self.material_name.text()
        material_type = "Porous" if "viscous_cl" in material_dict else "Solid"
        user_added = user_name # "admin"  # Later, replace with actual logged-in user
        producer = "Unknown Producer"  # Later, replace with user input

        insert_material(material_name, material_type, user_added, producer, material_dict)

        # some_interaction_with_db_script.add("material_name", material_dict)
    def print_db(self):
        df = get_materials()
        for index, row in df.iterrows():
            print(f"ID: {row['id']}, Name: {row['name']}, Properties: {row['properties']}")
        # print(df)

    def update_material_panel(self, material):
        self.material_gui.set_material(material)

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
        # self.scroll_widget.setMinimumHeight(130)
        self.scroll_area.setMinimumHeight(130)
        # self.layers_layout.setContentsMargins(0, 0, 0, 0)
        # self.layers_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.scroll_widget.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        # self.scroll_area.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        # self.layers_layout = QGridLayout(self.scroll_widget) #  QHBoxLayout QGridLayout

        self.scroll_widget.setLayout(self.layers_layout)
        self.scroll_area.setWidget(self.scroll_widget)
        self.scroll_area.setWidgetResizable(True)
        main_layout.addWidget(self.scroll_area)

        self.solid_image = "solid.jpg"
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
        while self.layers_layout.count():
            item = self.layers_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                self.clear_layout(item.layout())

        sorted_keys = sorted(layers.keys(), key=lambda x: int(x))
        for col_index, layer_key in enumerate(sorted_keys):
            thickness_val = layers[layer_key]["thickness"]
            layer_container_width = float(thickness_val) + 22
            # layer_container_width = layer_container_width if layer_container_width > 25 else layer_container_width + 25

            material_type = layers[layer_key]["material_type"]
            image_path = self.porous_image if material_type == "Porous" else self.solid_image
            new_layer_btn = CustomButton2(int(layer_key), image_path, self.layers_layout, self.change_selected_layer)
            new_layer_btn.resize_btn(layer_container_width, new_layer_btn.button.sizeHint().height())
            layer_container = QVBoxLayout()
            # layer_container_width = new_layer_btn.button.sizeHint().width()

            thickness_input = QLineEdit(str(thickness_val))
            thickness_input.editingFinished.connect(self.create_thickness_update_callback(layer_key, thickness_input))

            thickness_input.setFixedWidth(layer_container_width)
            thickness_input.setAlignment(Qt.AlignmentFlag.AlignLeft)
            thickness_input.setStyleSheet("padding: 0px; border: 1px solid gray;")
            layer_container.addWidget(thickness_input)
            layer_container.addWidget(new_layer_btn.button, alignment=Qt.AlignmentFlag.AlignLeft)

            dot_label = QLabel("●")  # dot
            dot_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            dot_label.setStyleSheet("font-size: 10px; color: black;")

            if layer_key == selected_layer:
                dot_label.setStyleSheet("font-size: 10px; color: lightgreen;")  # Light green if selected

            layer_container.addWidget(dot_label, alignment=Qt.AlignmentFlag.AlignCenter)
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
        def callback():
            self.update_thickness(layer_key, thickness_input.text())
        return callback

    def update_thickness(self, layer_key, value):
        try:
            # new_width = int(float(value))
            # new_width = new_width if new_width > 15 else new_width + 15

            layers[layer_key]["thickness"] = float(value)
            self.update_layers_gui()
            # print(layers[layer_key]["thickness"])
            '''for i in range(self.layers_layout.count()):
                item = self.layers_layout.itemAt(i)
                if isinstance(item, QVBoxLayout):
                    thickness_input = item.itemAt(0).widget() # QLineEdit
                    layer_button = item.itemAt(1).widget()  # CustomButton

                    if thickness_input and layer_button:
                        thickness_input.setFixedWidth(new_width)
                        height = layer_button.sizeHint().height()
                        layer_button.setFixedWidth(new_width)
                        layer_button.setStyleSheet(f"""
                        QPushButton {{
                            border: none;
                            padding: 0px;
                            width: {new_width}px;
                            height: {height}px;
                        }}""")
                        layer_button.setIconSize(QSize(new_width, height))  # Ensure image stretches'''

            # modify the properties of each element of this layers_layout item to the new width:
            # i e the width of the layers_layout_item.thickness_input and layers_layout_item.new_layer_btn.resize_btn(...)
        except ValueError:
            pass  # Ignore invalid inputs (e.g., empty field)

    def change_selected_layer(self, dynamic_layer):
        global selected_layer

        # if isinstance(dynamic_layer, CustomButton):
        layer_index = str(dynamic_layer.index)
        selected_layer = f'{layer_index}'
        self.main_window.update_material_panel(layers[selected_layer]["material_params"])
        self.update_dot_colors()

    def update_dot_colors(self):
        """Updates dot colors to reflect the currently selected layer."""
        for i in range(self.layers_layout.count()):
            item = self.layers_layout.itemAt(i)
            if isinstance(item, QVBoxLayout):
                dot_label = item.itemAt(2).widget()  # Third widget in the container (dot label)
                layer_index = str(i)  # Assuming layers are stored in order

                if dot_label and isinstance(dot_label, QLabel):
                    if layer_index == selected_layer:
                        dot_label.setStyleSheet("font-size: 10px; color: lightgreen;")
                    else:
                        dot_label.setStyleSheet("font-size: 10px; color: black;")

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
        self.params_layout.setSpacing(5)
        self.params_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
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

    initialize_database()

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())