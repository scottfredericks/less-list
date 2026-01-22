from PySide6.QtWidgets import QLabel, QVBoxLayout

from ..core.view_manager import DeclarativeView


class NewJobsView(DeclarativeView):
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        label = QLabel("New Jobs (TODO)")
        layout.addWidget(label)
