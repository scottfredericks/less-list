"""Starts and runs the main application and window."""

from PySide6.QtWidgets import QApplication

from less_list.views.main_menu import MainWindow

import sys


def main():
    """Instantiate and start the global objects."""
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
