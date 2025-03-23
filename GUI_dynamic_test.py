import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QScrollArea
from GUI_elements import CustomButton

class DynamicButtonsApp(QWidget):
    def __init__(self):
        super().__init__()

        main_layout = QHBoxLayout(self)

        # only function to add more buttons
        self.control_panel = QWidget(self)
        control_layout = QVBoxLayout(self.control_panel)
        self.add_button = QPushButton("Add Button", self)
        self.add_button.clicked.connect(self.add_dynamic_button)
        control_layout.addWidget(self.add_button)
        main_layout.addWidget(self.control_panel)

        # Buttons Container with Scroll Area - add them into rightz
        self.scroll_area = QScrollArea(self)
        self.scroll_widget = QWidget()
        self.buttons_layout = QVBoxLayout(self.scroll_widget)
        self.scroll_widget.setLayout(self.buttons_layout)

        self.scroll_area.setWidget(self.scroll_widget)
        self.scroll_area.setWidgetResizable(True)
        main_layout.addWidget(self.scroll_area)

        self.setLayout(main_layout)
        # this will be material layers in future
        self.dynamic_buttons = []

        self.image_paths = ["solid.png", "porous.png"]

    def add_dynamic_button(self):
        index = len(self.dynamic_buttons) + 1

        if index % 2 == 1:  # Odd index → Standard QPushButton
            new_button = QPushButton(f"Button {index}", self)
            new_button.clicked.connect(lambda _, btn=new_button: self.remove_dynamic_button(btn))
        else:  # Even index → CustomButton with alternating images
            image_path = self.image_paths[(index // 2) % 2]  # Alternate images
            new_button = CustomButton(index, image_path, self.buttons_layout, self.remove_dynamic_button)

        self.buttons_layout.addWidget(new_button.button if isinstance(new_button, CustomButton) else new_button)
        self.dynamic_buttons.append(new_button)

    def remove_dynamic_button(self, button):
        """now removes a button when clicked"""
        # TODO: replace it with the code to:
        # selected_layer_index = this
        #
        if isinstance(button, CustomButton):
            button.remove(self.buttons_layout)
        else:
            self.buttons_layout.removeWidget(button)
            button.deleteLater()

        self.dynamic_buttons.remove(button)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DynamicButtonsApp()
    window.show()
    sys.exit(app.exec())