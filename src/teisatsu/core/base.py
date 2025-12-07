from abc import ABC, abstractmethod
from typing import Any

import logging as lg
import importlib


class TScriptError(Exception):
    pass


class TScriptBase(ABC):
    @abstractmethod
    def __init__(self, script_config: dict) -> None:
        
        self.name = script_config['name']
        self.tags = script_config['tags']
        self.version = script_config['version']
        self.desc = script_config['desc'].strip()
        self.requirements = script_config['requirements']
        
        self.name = str(self.name).strip().replace(' ', '-').replace('_', '-')
        self.logger = lg.getLogger(f'teisatsu.script.{self.name.lower()}')
        
        self.data = {}
        self._imported_modules = {}
        
        
    def __getattr__(self, name: str) -> Any:
        if name in self.requirements:
            return self._imported_modules.get(name)
        
        raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")
    
    
    def import_requirements(self) -> None:
        failed = []
        for lib_name in self.requirements:
            try:
                module = importlib.import_module(lib_name)
                self._imported_modules[lib_name] = module
            
            except ImportError as e:
                self.logger.exception(f'Failed to load required lib: {lib_name}')
                failed.append(lib_name)
        
        if failed:
            raise ImportError(f'Failed to load required libraries: {",".join(failed)}')
    
    
    @abstractmethod
    def run(self, thing: Any) -> dict[str, Any]:
        ...