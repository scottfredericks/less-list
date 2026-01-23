"""Handles the Declarative Binding logic (The 'Binder')."""

from typing import Any, List
from PySide6.QtCore import QObject


class BindingRule:
    """Stores the definition of a link between a Widget and a Model Property."""

    def __init__(
        self,
        widget: QObject,
        widget_prop: str,
        widget_signal: str,
        model_prop: str,
        model_signal: str,
    ):
        """Initialize a binding rule with widget and model property mappings."""
        self.widget = widget
        self.widget_prop = widget_prop
        self.widget_signal = widget_signal
        self.model_prop = model_prop
        self.model_signal = model_signal


class Binder:
    """Manage active signal connections.

    Apply rules when a model is provided, disconnect them when removed.
    """

    def __init__(self):
        """Initialize the binder with empty rules and connections lists."""
        self._rules: List[BindingRule] = []
        # We store connection objects to keep references alive or allows introspection
        self._connections: List[Any] = []

    def add_rule(
        self,
        widget: QObject,
        widget_prop: str,
        model_prop: str,
        signal_map: tuple[str, str],
    ):
        """Add a binding rule to connect a widget property to a model property."""
        rule = BindingRule(
            widget, widget_prop, signal_map[0], model_prop, signal_map[1]
        )
        self._rules.append(rule)

    def apply(self, model: Any):
        """Connect all registered rules to the specific model instance."""
        if not model:
            return

        for rule in self._rules:
            # 1. Resolve Nested Properties (e.g., 'settings.theme')
            target_model = model
            target_prop_name = rule.model_prop

            if "." in rule.model_prop:
                parts = rule.model_prop.split(".")
                target_prop_name = parts[-1]
                for part in parts[:-1]:
                    if hasattr(target_model, part):
                        target_model = getattr(target_model, part)
                    else:
                        # Path broken (e.g. settings is None), skip binding
                        target_model = None
                        break

            if target_model is None:
                continue

            # 2. Initial Data Push (Model -> Widget)
            if hasattr(target_model, target_prop_name):
                val = getattr(target_model, target_prop_name)
                self._set_widget_prop(rule.widget, rule.widget_prop, val)

            # 3. Widget -> Model Binding (Two-way)
            if hasattr(rule.widget, rule.widget_signal):
                w_sig = getattr(rule.widget, rule.widget_signal)
                # Lambda captures rule/target to ensure correct update
                # We use defaults in lambda to capture current loop variables
                conn = w_sig.connect(
                    lambda v, tm=target_model, tp=target_prop_name: setattr(tm, tp, v)
                )
                self._connections.append(conn)

            # 4. Model -> Widget Binding
            if hasattr(target_model, rule.model_signal):
                m_sig = getattr(target_model, rule.model_signal)
                conn = m_sig.connect(
                    lambda v, w=rule.widget, wp=rule.widget_prop: self._set_widget_prop(
                        w, wp, v
                    )
                )
                self._connections.append(conn)

    def unapply(self):
        """Disconnect all signals.

        In PySide6, creating new connection objects in apply() allows the old ones
        to be garbage collected if we clear the list, or we can explicit disconnect.
        """
        for conn in self._connections:
            # Explicit disconnect is safer to ensure no zombie signals
            try:
                conn.disconnect()
            except Exception:
                pass  # Already disconnected or object dead
        self._connections.clear()

    def _set_widget_prop(self, widget, prop, value):
        """Call setText, setValue, setChecked dynamically based on property name."""
        # Standard Qt Setters are usually setProperty -> setProp
        # Check for standard setter: 'text' -> 'setText'
        setter_name = f"set{prop[0].upper()}{prop[1:]}"

        if hasattr(widget, setter_name):
            getattr(widget, setter_name)(value)
        else:
            # Fallback (mostly for custom properties)
            setattr(widget, prop, value)
