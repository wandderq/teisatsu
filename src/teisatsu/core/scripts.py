from abc import ABC, abstractmethod
from typing import Any

import logging as lg



class TeisatsuScript(ABC):
    def __init__(self, name: str, tags: list[str], requirements: list[str]) -> None:
        self.name = name
        self.tags = tags
        self.requirements = requirements
        
        self.name = str(self.name).strip().replace(' ', '-').replace('_', '-')
        self.logger = lg.getLogger(f'teisatsu.scripts.{self.name.lower()}')
    
    
    @abstractmethod
    def run(self, thing: Any) -> dict[str, Any]:
        ...