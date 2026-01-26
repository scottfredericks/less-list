"""Main window containing the main menu and other global views."""

from PySide6.QtWidgets import QMainWindow, QLabel

from less_list.strings import STRINGS


class MainWindow(QMainWindow):
    """Class for the main application window."""

    def __init__(self):
        """Manage child view navigation and model initiation."""
        super().__init__()

        self.setWindowTitle(STRINGS["main"]["app_name"])

        button = QLabel("TODO")

        self.setCentralWidget(button)
