from ..core.base import TScriptError, TScriptBase
from datetime import datetime

import logging as lg
import importlib
import pkgutil
import copy


class TDataProcessor:
    def __init__(self) -> None:
        pass
    
    
    def _process_list(self, data: list) -> list:
        for i, obj in enumerate(data):
            if isinstance(obj, dict):
                data[i] = self._process_dict(obj)
                continue
    
            if isinstance(obj, list):
                data[i] = self._process_list(obj)
                continue
            
            # processiong here
            if isinstance(obj, datetime):
                data[i] = obj.strftime("%d/%m/%Y, %H:%M:%S")
        
        return data
    
    
    def _process_dict(self, data: dict) -> dict:
        for key, value in data.items():
            if isinstance(value, dict):
                data[key] = self._process_dict(value)
                continue
            
            if isinstance(value, list):
                data[key] = self._process_list(value)
                continue
            
            # processing here
            if isinstance(value, datetime):
                data[key] = value.strftime("%d/%m/%Y, %H:%M:%S")
        
        return data
    
    
    def process(self, raw_data: dict):
        raw_data_copy = copy.deepcopy(raw_data)
        return self._process_dict(raw_data_copy)



class TScriptManager:
    def __init__(self) -> None:
        self.logger = lg.getLogger('teisatsu.plugins.script-manager')
        self.package_path = 'teisatsu.plugins.scripts'
        self.scripts: list = []
        self.data_processor = TDataProcessor()
    
    
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
    
    
    def run_scripts(self, thing: str, tags: list[int]):
        sent_results = {}
        
        for script in self.scripts:
            self.logger.debug(f'Checking script: {script["name"]}')
            
            if 'exclude_tags' in script and any([tag in script['exclude_tags'] for tag in tags]):
                continue
            
            if any([tag in script['tags'] for tag in tags]):
                
                self.logger.debug(f'Launching script: {script["name"]}')
                script_object: TScriptBase = script['class']()
                raw_results = script_object.run(thing)
                results = self.data_processor.process(raw_results)
                
                for key, val in list(results.items()):
                    if key in sent_results and sent_results[key] == val:
                        del results[key]
                
                sent_results.update(results)
                
                yield script['name'], results