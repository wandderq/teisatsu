from abc import ABC, abstractmethod
from typing import Any

import logging as lg


class TScriptError(Exception):
    pass


class TScriptBase(ABC):
    @abstractmethod
    def __init__(self, script_globals: dict) -> None:
        
        self.name = script_globals['TSS_NAME']
        self.tags = script_globals['TSS_TAGS']
        self.version = script_globals['TSS_VERSION']
        self.description = script_globals['TSS_DESCRIPTION']
        self.requirements = script_globals['TSS_REQUIREMENTS']
        
        self.name = str(self.name).strip().replace(' ', '-').replace('_', '-')
        self.logger = lg.getLogger(f'teisatsu.script.{self.name.lower()}')
    
    @abstractmethod
    def run(self, thing: Any) -> dict[str, Any]:
        ...