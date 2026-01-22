"""src/less_list/core/view_manager.py

The Core Framework. Defines Lifecycle Nodes, Views, Components, and the Manager.
"""

from typing import Optional, TypeVar, Generic, Type, List, Any
from abc import abstractmethod
from PySide6.QtWidgets import QWidget, QVBoxLayout, QStackedWidget
from PySide6.QtCore import Signal
from less_list.core.binding import Binder

M = TypeVar("M")

# --- 1. Lifecycle Node (Tree Logic) ---


class LifeCycleNode(Generic[M]):
    """Mixin handles recursive activation of child components."""

    def __init__(self):
        self._children: List["ManagedComponent"] = []
        self._model: Optional[M] = None

    def register_child(self, component: "ManagedComponent"):
        self._children.append(component)
        # If parent is currently active, activate child immediately
        if self._model:
            component.activate(self._model)

    def activate_children(self, model: M):
        for child in self._children:
            child.activate(model)

    def deactivate_children(self):
        for child in self._children:
            child.deactivate()


# --- 2. Base View Classes ---


class ManagedView(QWidget, LifeCycleNode[M]):
    """Top-Level Page in the Stack."""

    data_requested = Signal()

    def __init__(self, parent: Optional[QWidget] = None):
        QWidget.__init__(self, parent)
        LifeCycleNode.__init__(self)
        self._setup_ui()

    @abstractmethod
    def _setup_ui(self):
        """Build widgets here."""
        pass

    def activate(self, model: Optional[M] = None):
        """Called when navigating TO this view."""
        self._model = model
        if model:
            self._bind_model(model)
            self.activate_children(model)
        elif self._model is None:
            self.data_requested.emit()

    def deactivate(self):
        """Called when navigating AWAY."""
        if self._model:
            self._unbind_model()
            self.deactivate_children()
            self._model = None

    def _bind_model(self, model: M):
        pass

    def _unbind_model(self):
        pass


class ManagedComponent(ManagedView[M]):
    """Nested component inside a View (e.g. Tab, Card)."""

    def __init__(
        self, parent_view: ManagedView, parent_widget: Optional[QWidget] = None
    ):
        super().__init__(parent_widget)
        # Auto-registration with parent
        parent_view.register_child(self)

    def map_data(self, root_model: M) -> Any:
        """Override to select a specific sub-object of the model."""
        return root_model

    def activate(self, model: M):
        # Component activation includes mapping logic
        target_data = self.map_data(model)
        if target_data is not None:
            super().activate(target_data)
        else:
            # If mapping fails (e.g. data is None), treat as valid but empty
            self._model = None


class DeclarativeView(ManagedView[M]):
    """View that uses the Binder."""

    def __init__(self, parent=None):
        self._binder = Binder()
        super().__init__(parent)

    def _bind_model(self, model: M):
        self._binder.apply(model)

    def _unbind_model(self):
        self._binder.unapply()

    def bind(self, widget, widget_prop, model_prop, signal_map=None):
        if signal_map is None:
            # Auto-guess conventions: model.prop_changed / widget.textChanged
            m_sig = f"{model_prop.split('.')[-1]}_changed"
            w_sig = "textChanged"  # Default guess
            signal_map = (w_sig, m_sig)
        self._binder.add_rule(widget, widget_prop, model_prop, signal_map)


class DeclarativeComponent(ManagedComponent[M]):
    """Component that uses the Binder."""

    def __init__(self, parent_view, parent_widget=None):
        self._binder = Binder()
        super().__init__(parent_view, parent_widget)

    def _bind_model(self, model: M):
        self._binder.apply(model)

    def _unbind_model(self):
        self._binder.unapply()

    def bind(self, widget, widget_prop, model_prop, signal_map=None):
        if signal_map is None:
            m_sig = f"{model_prop.split('.')[-1]}_changed"
            w_sig = "textChanged"
            signal_map = (w_sig, m_sig)
        self._binder.add_rule(widget, widget_prop, model_prop, signal_map)


# --- 3. The Manager ---


class ViewManager(QWidget):
    """Manages the QStackedWidget and Lazy Instantiation."""

    view_changed = Signal(str)

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self._stack = QStackedWidget()
        self._registry: dict[str, Type[ManagedView]] = {}
        self._active_views: dict[str, ManagedView] = {}
        self._current_key: Optional[str] = None

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self._stack)

    def register(self, key: str, view_cls: Type[ManagedView]):
        self._registry[key] = view_cls

    def navigate(self, key: str, model=None):
        if key not in self._registry and key not in self._active_views:
            raise KeyError(f"View '{key}' not registered")

        # 1. Teardown old
        if self._current_key and self._current_key in self._active_views:
            self._active_views[self._current_key].deactivate()

        # 2. Lazy Load new
        if key not in self._active_views:
            view_cls = self._registry[key]
            instance = view_cls()
            self._active_views[key] = instance
            self._stack.addWidget(instance)

        # 3. Setup new
        current_view = self._active_views[key]
        self._stack.setCurrentWidget(current_view)
        current_view.activate(model)

        self._current_key = key
        self.view_changed.emit(key)

    def current_view(self) -> Optional[ManagedView]:
        if self._current_key:
            return self._active_views.get(self._current_key)
        return None
