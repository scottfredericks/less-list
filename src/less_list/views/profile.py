"""Profile view for managing user information."""

from PySide6.QtWidgets import QLabel, QVBoxLayout, QLineEdit, QCheckBox
from less_list.core.view_manager import DeclarativeView


class ProfileView(DeclarativeView):
    """View for displaying and editing user profile information."""

    def _setup_ui(self):
        layout = QVBoxLayout(self)

        self.user_input = QLineEdit()
        self.email_input = QLineEdit()
        self.notify_chk = QCheckBox("Enable Notifications")

        layout.addWidget(QLabel("Username"))
        layout.addWidget(self.user_input)

        layout.addWidget(QLabel("Email"))
        layout.addWidget(self.email_input)

        layout.addWidget(self.notify_chk)
        layout.addStretch()

        # Bindings
        self.bind(self.user_input, "text", "username")
        self.bind(self.email_input, "text", "email")
        self.bind(
            self.notify_chk,
            "checked",
            "notifications",
            signal_map=("toggled", "notifications_changed"),
        )
