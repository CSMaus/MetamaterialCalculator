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
        self.button = QPushButton("")  # No text, image only

        # Load image and set full button size
        icon = QIcon(QPixmap(image_path))
        self.button.setIcon(icon)
        self.button.setIconSize(QSize(80, 80))  # Ensures icon fills the button

        # Remove padding, margin, and background for a clean look
        self.button.setStyleSheet("""
            QPushButton {
                border: none;
                padding: 0px;
                width: 80px;
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
        """Updates the button image."""
        self.image_path = new_image_path
        icon = QIcon(QPixmap(new_image_path))
        self.button.setIcon(icon)

    def remove(self, parent_layout):
        """Removes the button from the layout."""
        parent_layout.removeWidget(self.button)
        self.button.deleteLater()