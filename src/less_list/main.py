"""Define data models and orchestrate the app startup."""

from dataclasses import dataclass
import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QObject

from less_list.core.view_manager import ViewManager
from less_list.core.reactive_model import reactive_model

from less_list.views.onboarding import OnboardingView
from less_list.views.main_menu import MainMenuView


# --- Data Models ---


@reactive_model
@dataclass
class AppState(QObject):
    """Root State Object passed to views."""

    username: str
    email: str
    notifications: bool
    onboarding_complete: bool


# --- Application Controller ---


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("LessList")
        self.resize(800, 600)

        # 1. Initialize State
        # In a real app, you would load 'onboarding_complete' from disk (Settings/JSON) here.
        self.state = AppState(
            username="NewUser",
            email="",
            notifications=False,
            onboarding_complete=False,  # Default for new session
        )

        # 2. Setup View Manager
        self.vm = ViewManager()
        self.setCentralWidget(self.vm)

        # 3. Register Views
        self.vm.register("onboarding", OnboardingView)
        self.vm.register("main_menu", MainMenuView)

        # 4. Wire up Global Logic (Model-Driven Navigation)
        # When the flag changes in the model, we switch views automatically.
        self.state.onboarding_complete_changed.connect(self._check_onboarding_status)

        # 5. Initial Navigation based on State
        self._check_onboarding_status(self.state.onboarding_complete)

    def _check_onboarding_status(self, is_complete):
        """Routing Logic: Decides which screen to show based on state."""
        if is_complete:
            # If we are already elsewhere, navigate to menu
            if self.vm._current_key != "main_menu":
                self.vm.navigate("main_menu", model=self.state)
        else:
            if self.vm._current_key != "onboarding":
                self.vm.navigate("onboarding", model=self.state)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
