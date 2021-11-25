"""Settings loader module."""
import importlib
import os
from typing import Any

from onapsdk.exceptions import ModuleError, SettingsError

from . import global_settings


SETTINGS_ENV = "ORAN_PYTHON_SDK_SETTINGS"


class SettingsLoader:
    """Settings loader class.

    Load global settings and optionally load
        custom settings by importing the module
        stored in ORAN_PYTHON_SDK_SETTINGS environment
        variable.
        The module has to be uder PYTHONPATH.
    """

    def __init__(self) -> None:
        """Load settings.

        Load global settings and optionally load custom one.

        Raises:
            ModuleError: If ORAN_PYTHON_SDK_SETTINGS environment variable
                is set and module can't be imported.

        """
        self._settings = {}

        # Load values from global_settings (only uppercase)
        self.filter_and_set(global_settings)

        settings_env_value: str = os.environ.get(SETTINGS_ENV)
        if settings_env_value:
            # Load values from custom settings
            try:
                module = importlib.import_module(settings_env_value)
            except ModuleNotFoundError:
                msg = "Can't import custom settings. Is it under PYTHONPATH?"
                raise ModuleError(msg)
            self.filter_and_set(module)

    def __getattribute__(self, name: str) -> Any:
        """Return stored attributes.

        If attribute name is uppercase return it from
            _settings dictionary.
            Look for attribute in __dict__ otherwise.

        Args:
            name (str): Attribute's name

        Raises:
            SettingsError: a setting is not found by the key.

        Returns:
            Any: Attribute's value

        """
        if name.isupper():
            try:
                return self._settings[name]
            except KeyError as exc:
                msg = f"Requested setting {exc.args[0]} does not exist."
                raise SettingsError(msg) from exc
        return super().__getattribute__(name)

    def __setattr__(self, name: str, value: Any) -> None:
        """Save attribute.

        If attribute name is uppercase save the value
            in _settings dictionary.
            Use Object class __setattr__ implementation
            otherwise.

        Args:
            name (str): Attribute's name
            value (Any): Attribute's value

        """
        if name.isupper():
            self._settings[name] = value
        super().__setattr__(name, value)

    def filter_and_set(self, module: "module") -> None:
        """Filter module attributes and save the uppercased.

        Iterate through module's attribures and save the value
            of them which name is uppercase.

        Args:
            module (module): Module to get attributes from

        """
        for key in filter(lambda x: x.isupper(), dir(module)):
            self._settings[key] = getattr(module, key)
