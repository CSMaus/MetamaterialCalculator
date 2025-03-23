# here there will be classes for creating complex interactive elements
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import QSize


class CustomButton:
    def __init__(self, index, image_path, parent_layout, on_click_callback=None):
        """
        :param index: Unique index of the button
        :param image_path: Path to the button image
        :param parent_layout: Layout where the button will be added
        :param on_click_callback: Function to call when the button is clicked
        """
        self.index = index
        self.image_path = image_path
        self.button = QPushButton("")

        icon = QIcon(QPixmap(image_path))
        self.button.setIcon(icon)
        self.button.setIconSize(QSize(40, 80))

        self.button.setStyleSheet("""
            QPushButton {
                border: none;
                padding: 0px;
                width: 40px;
                height: 80px;
            }
        """)

        self.button.clicked.connect(self.on_click)
        parent_layout.addWidget(self.button)  # Add button to layout

        self.on_click_callback = on_click_callback  # Store callback function

    def on_click(self):
        # TODO: we will change the panel where we set
        # layer and material properties
        print(f"Button {self.index} clicked!")
        if self.on_click_callback:
            self.on_click_callback(self)  # Call external callback if provided

    def update_image(self, new_image_path):
        self.image_path = new_image_path
        icon = QIcon(QPixmap(new_image_path))
        self.button.setIcon(icon)

    def remove(self, parent_layout):
        parent_layout.removeWidget(self.button)
        self.button.deleteLater()

class CustomButton2:
    def __init__(self, index, image_path, parent_layout, on_click_callback=None):
        """
        :param index: Unique index of the button
        :param image_path: Path to the button image
        :param parent_layout: Layout where the button will be added
        :param on_click_callback: Function to call when the button is clicked
        """
        self.index = index
        self.image_path = image_path
        self.button = QPushButton("")



        self.button.setStyleSheet("""
            QPushButton {
                border: none;
                padding: 0px;
                width: 40px;
                height: 80px;
                }""")
        self.update_image(image_path)
        '''icon = QIcon(QPixmap(image_path))
        self.button.setIcon(icon)
        self.button.setIconSize(QSize(70, 80))'''

        # self.resize_btn(40, 80)
        self.button.clicked.connect(self.on_click)
        parent_layout.addWidget(self.button)

        self.on_click_callback = on_click_callback

    def resize_btn(self, new_width, new_height):
        self.button.resize(QSize(new_width, new_height))
        self.update_image(self.image_path)

    def update_image(self, new_image_path):
        self.image_path = new_image_path
        width = self.button.sizeHint().width()
        height = self.button.sizeHint().height()
        pixmap = QPixmap(new_image_path).scaled(QSize(width, height))
        icon = QIcon(pixmap)
        self.button.setIcon(icon)
        self.button.setIconSize(QSize(width, height))

    def on_click(self):
        # TODO: we will change the panel where we set
        # layer and material properties
        print(f"Button {self.index} clicked!")
        if self.on_click_callback:
            self.on_click_callback(self)  # Call external callback if provided

    def remove(self, parent_layout):
        """Removes the button from the layout."""
        parent_layout.removeWidget(self.button)
        self.button.deleteLater()