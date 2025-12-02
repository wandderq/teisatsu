from ..core.groups import SCRIPTS
from typing import Any
from collections import defaultdict

import logging as lg
import time

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
    
    
    def run_scripts(self, thing: Any, scripts: list[dict[str, Any]]) -> dict[str, Any]:
        info = defaultdict(dict)
        
        for script in scripts:
            name = script['name']
            tags = script['tags']
            cls = script['class']
            requirements = script['requirements']
            
            # launching & timeit
            self.logger.info(f'Launching script: {name}')
            start = time.time()
            data = cls().run(thing)
            elapsed = time.time() - start
            self.logger.debug(f'Script {name} took {elapsed:.4f}s')
            
            info[name].update(data)
        
        return info