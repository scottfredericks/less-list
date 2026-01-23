"""Wrapper class to automate signal generation for model properties."""

from typing import cast, get_type_hints, Any, Type
from dataclasses import is_dataclass
from PySide6.QtCore import QObject, Signal


def reactive_model(cls: Type[Any]) -> Type[QObject]:
    """Transform a class into a reactive QObject.

    Support standard classes AND @dataclasses.
    """
    annotations = get_type_hints(cls)

    # 1. Generate Signals and Properties
    # (Same logic as before to create _field, property, and field_changed signal)
    for field_name, field_type in annotations.items():
        signal_name = f"{field_name}_changed"
        private_name = f"_{field_name}"

        if not hasattr(cls, signal_name):
            setattr(cls, signal_name, Signal(field_type))

        def make_getter(p_name):
            return lambda self: getattr(self, p_name)

        def make_setter(p_name, s_name):
            def setter(self, value):
                # Handle AttributeError during init (if private var doesn't exist yet)
                try:
                    old_val = getattr(self, p_name)
                    if old_val != value:
                        setattr(self, p_name, value)
                        getattr(self, s_name).emit(value)
                except AttributeError:
                    setattr(self, p_name, value)

            return setter

        setattr(
            cls,
            field_name,
            property(make_getter(private_name), make_setter(private_name, signal_name)),
        )

    # 2. Handle Initialization Logic

    if is_dataclass(cls):
        # STRATEGY 3 FIX: Wrap the dataclass-generated __init__
        # We capture the __init__ created by @dataclass
        original_dataclass_init = cls.__init__

        def wrapped_init(self, *args, **kwargs):
            # A. Initialize QObject FIRST (Crucial Step)
            # This allocates the C++ memory
            super(cls, self).__init__()

            # B. Call the dataclass init to populate fields
            # Since properties are already active, settng self.name = "Bob"
            # calls our reactive setter -> sets _name -> emits Signal.
            original_dataclass_init(self, *args, **kwargs)

        cls.__init__ = wrapped_init

    else:
        # STRATEGY 1/2 Logic: Standard class handling
        user_defined_init = cls.__dict__.get("__init__")

        def new_init(self, **kwargs):
            if user_defined_init:
                user_defined_init(self, **kwargs)
            else:
                safe_cls = cast(Type[QObject], cls)
                super(safe_cls, self).__init__()

            # Initialize defaults and apply kwargs
            for name in annotations:
                p_name = f"_{name}"
                if not hasattr(self, p_name):
                    setattr(self, p_name, None)

            for k, v in kwargs.items():
                if k in annotations:
                    setattr(self, k, v)

        cls.__init__ = new_init

    return cls
