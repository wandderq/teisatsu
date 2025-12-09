from ..core.base import TScriptError, TScriptBase
from typing import Generator
from .data import TDataProcessor

import logging as lg
import importlib
import pkgutil


class TScriptManager:
    def __init__(self) -> None:
        self.logger = lg.getLogger('teisatsu.plugins.script-manager')
        self.package_path = 'teisatsu.plugins.scripts'
        self.scripts: list = []
    
    
    def load_scripts(self) -> None:
        try:
            package = importlib.import_module(self.package_path)
            
            # getting all of teisatsu.plugins.scripts.* modules
            for _, module_name, is_pkg in pkgutil.iter_modules(package.__path__):
                if not is_pkg:
                    
                    # loading script from teisatsu.plugins.scripts.module
                    try:
                        full_name = f"{self.package_path}.{module_name}"
                        module = importlib.import_module(full_name)
                        
                        if not hasattr(module, 'TSS_SCRIPT'):
                            raise TScriptError(f'Module {module.__name__} hasn\'t the TSS_SCRIPT attribute')
                        
                        self.scripts.append(module.TSS_SCRIPT)
                        
                    
                    except Exception as e:
                        self.logger.warning(f'Failed to load script: {module_name} due to error: {str(e)}')
                        
        
        except Exception as e:
            self.logger.error(f'Failed to load scripts due to error: {str(e)}')
    
    
    def run_scripts(self, thing: str, tags: list[int]) -> Generator[tuple[str, dict, list], None, None]:
        data_processor = TDataProcessor()
        sent_results = {}
        
        
        scripts = [
            script for script in self.scripts
            if any(tag in script['tags'] for tag in tags)
            and not (
                ('exclude_tags' in script and script['exclude_tags'])
                and
                (not any(tag in script['exclude_tags'] for tag in tags))
            )
        ]
        
        # if 'exclude_tags' in script and script['exclude_tags']:
        #     if any([tag in script['exclude_tags'] for tag in tags]):
        #         continue
        
        # for script in scripts:
            # if any([tag in script['tags'] for tag in tags]):
        
        
        for script in scripts:
            none_data = []
            script_obj: TScriptBase = script['class']()
            raw_results = script_obj.run(thing)
            results = data_processor.process(raw_results)
            
            
            for key, val in list(results.items()):
                if val is None:
                    none_data.append(key)
                    del results[key]
                    continue
                
                if key in sent_results and sent_results[key] == val:
                    del results[key]
                    continue
            
            sent_results.update(results)
            yield (script['name'], results, none_data)