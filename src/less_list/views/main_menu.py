"""Main menu view with tabs for different sections of the app."""

from PySide6.QtWidgets import QTabWidget, QVBoxLayout
from less_list.core.view_manager import DeclarativeView
from less_list.views.new_jobs import NewJobsView
from less_list.views.active_jobs import ActiveJobsView
from less_list.views.profile import ProfileView
from less_list.views.settings import SettingsView


class MainMenuView(DeclarativeView):
    """The main app screen containing tabs.

    This view acts as a lifecycle orchestrator for the tabs.
    """

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)

        # We use a list to track child views so we can activate them
        self.tab_views = []

        # Helper to Add Tabs
        self._add_tab(NewJobsView, "New Jobs")
        self._add_tab(ActiveJobsView, "Active Jobs")
        self._add_tab(ProfileView, "Profile")
        self._add_tab(SettingsView, "Settings")

        # Handle Tab Switching: Activate only the visible tab logic?
        # Option A: Activate ALL tabs (Simple).
        # Option B: Activate only current (Lazy).
        # Implementing Option A (Simple) for this example as per "Strategy 2" logic

        # NOTE: Even though NewJobsView is a 'ManagedView', here we treat it
        # as a Child Component because it lives inside MainMenu.
        # We manually register it if it doesn't auto-register.
        # Since 'ManagedView' logic is strictly for top-level stack, we
        # need to ensure the LIFECYCLE signals propagate.

    def _add_tab(self, view_cls, title):
        # Instantiate the view
        # We treat these as "Components" of the MainMenu
        view = view_cls()
        self.tabs.addTab(view, title)

        # Important: By default, ManagedView doesn't auto-register as a child
        # of another ManagedView unless we use the Component wrapper.
        # So we manually register it to receive Update/Bind events.
        self.register_child(view)

    # Note: No custom _bind_model needed here.
    # The base class 'activate' will automatically call 'activate' on all
    # registered children (the tabs), passing the model down.
