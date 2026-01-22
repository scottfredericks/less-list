from PySide6.QtWidgets import QLabel, QVBoxLayout, QPushButton
from PySide6.QtCore import Qt
from less_list.core.view_manager import DeclarativeView

# Type hinting imports
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass  # Only for type checking to avoid circular imports


class OnboardingView(DeclarativeView):
    """First screen seen by the user."""

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        title = QLabel("Welcome to LessList")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")

        desc = QLabel("The generic list management tool.")

        self.btn_start = QPushButton("Get Started")

        # Connect UI event to Logic Handler
        self.btn_start.clicked.connect(self._complete_onboarding)

        layout.addWidget(title)
        layout.addWidget(desc)
        layout.addWidget(self.btn_start)

    def _bind_model(self, model):
        # We explicitly call super to enable the declarative binder
        super()._bind_model(model)

        # We also store a direct reference purely for the logic method below
        # (ManagedView already stores self._model, but type inference helps)
        self._model = model

    def _complete_onboarding(self):
        """Updates the model to reflect completion."""
        if self._model:
            # This setter triggers the 'onboarding_complete_changed' Signal
            # which main.py is listening to.
            self._model.onboarding_complete = True
