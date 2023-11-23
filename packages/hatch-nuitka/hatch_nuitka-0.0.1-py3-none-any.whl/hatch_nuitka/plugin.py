from typing import Any
from hatchling.builders.hooks.plugin.interface import BuildHookInterface
import platform

class NuitkaBuildHook(BuildHookInterface):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__config_nuitka_args = None
        self.__config_options = None
        self.__config_separation = None
        self.__config_build_dir = None
        self.__config_include = None
        self.__config_exclude = None
        self.__package_source = None
        self.__include_spec = None
        self.__exclude_spec = None
        self.__included_files = None
        self.__normalized_included_files = None
        self.__artifact_globs = None
        self.__normalized_artifact_globs = None
        self.__artifact_patterns = None
        self._on_windows = platform.system() == 'Windows'
        self.__compiled_extension = '.pyd' if self._on_windows else '.so'
        
    @property
    def config_nuitka(self):
        if self.__config_nuitka_args is None:
            nuitka_args = self.config.get('nuitka-args', {})
            if isinstance(self.__config_nuitka_args, list):
                for i, argument in enumerate(nuitka_args, 1):
                    if not isinstance(argument, str):
                        raise ValueError(f"nuitka-args[{i}] is not a string")
                    elif not argument:
                        raise ValueError(f"nuitka-args[{i}] is empty")
            else:
                raise ValueError("nuitka-args is not a list")
            self.__config_nuitka_args = nuitka_args
        return self.__config_nuitka_args
    
    @property
    def config_options(self):
        if self.__config_options is None:
            options = self.config.get('options', {})
            if not isinstance(options, dict):
                raise ValueError("options is not a dict")
            self.__config_options = options
        return self.__config_options
    
    @property
    def config_separation(self):
        if self.__config_separation is None:
            self.__config_separation = self.config.get('separation', False) == True
        return self.__config_separation
    
    
    def initialize(self, version: str, build_data: dict[str, Any]) -> None:
        if self.target_name != "wheel":
            return
        