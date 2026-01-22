from PySide6.QtWidgets import QLabel, QVBoxLayout
from less_list.core.view_manager import DeclarativeView


class SettingsView(DeclarativeView):
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        label = QLabel("Settings (TODO)")
        layout.addWidget(label)
