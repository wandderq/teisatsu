from ..core.groups import SCRIPTS
from typing import Any

import logging as lg


class TeisatsuScriptManager:
    def __init__(self) -> None:
        self.scripts = SCRIPTS
        self.logger = lg.getLogger('teisatsu.manager')
    
    
    
    def get_scripts(self, tags: list[str]) -> list[dict[str,Any]]:
        matches = []
        for script in self.scripts:
            for tag in tags:
                if tag in script['tags']:
                    matches.append(script)
                    break # breaking 'tag in tags' loop
        
        if not matches:
            self.logger.error(f'No matches found for \'{", ".join(tags)}\' tags')
        
        return matches