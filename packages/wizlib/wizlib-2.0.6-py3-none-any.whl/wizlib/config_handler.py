from argparse import Namespace
from pathlib import Path
import os
from dataclasses import dataclass
from unittest.mock import patch

from yaml import load
from yaml import Loader

from .app import WizApp


class ConfigHandler:
    """
    Handle app-level configuration, where settings could come from specific
    settings (such as from argparse), environment variables, or a YAML file.
    """

    name = 'config'

    def __init__(self, value=None):
        self.cache = {}
        self.file = value

    @property
    def yaml(self):
        if hasattr(self, '_yaml'):
            return self._yaml
        if self.file:
            path = Path(self.file)
        elif (envvar := self.env(self.appname + '-config')):
            path = Path(envvar)
        elif ((localpath := Path.cwd() / f".{self.appname}.yml").is_file()):
            path = localpath
        elif ((homepath := Path.home() / f".{self.appname}.yml").is_file()):
            path = homepath
        else:
            path = None
        if path:
            with open(path) as file:
                self._yaml = load(file, Loader=Loader)
                return self._yaml

    @staticmethod
    def env(name):
        if (envvar := name.upper().replace('-', '_')) in os.environ:
            return os.environ[envvar]

    def get(self, key: str):
        """Return the value for the requested config entry"""

        # If we already found the value, return it
        if key in self.cache:
            return self.cache[key]

        # Environment variables take precedence
        if (result := self.env(key)):
            self.cache[key] = result
            return result

        # Otherwise look at the YAML
        if (yaml := self.yaml):
            split = key.split('-')
            while (val := split.pop(0)) and (val in yaml):
                yaml = yaml[val] if val in yaml else None
                if not split:
                    self.cache[key] = yaml
                    return yaml

    @classmethod
    def fake(cls, **vals):
        """Return a fake ConfigHandler with forced values, for testing"""
        handler = cls()

        def fake_env(name):
            if name in vals:
                return vals[name]
        handler.env = fake_env
        return handler
