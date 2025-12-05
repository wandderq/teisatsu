from abc import ABC, abstractmethod
from typing import Any

import logging as lg


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
    
    @abstractmethod
    def run(self, thing: Any) -> dict[str, Any]:
        ...