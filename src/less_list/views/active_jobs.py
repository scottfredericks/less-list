from PySide6.QtWidgets import QLabel, QVBoxLayout
from less_list.core.view_manager import DeclarativeView


class ActiveJobsView(DeclarativeView):
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        label = QLabel("Active Jobs (TODO)")
        layout.addWidget(label)
