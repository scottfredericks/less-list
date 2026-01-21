from PySide6.QtWidgets import QApplication, QWidget

import sys

app = QApplication(sys.argv)

window = QWidget()


def main():
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
