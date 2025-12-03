from ..core.base import TScriptError

import logging as lg
import importlib
import pkgutil
import inspect


class TPluginManager:
    def __init__(self) -> None:
        self.classifiers_package_path = 'teisatsu.core.plugins.classifiers'
        self.scripts_package_path = 'teisatsu.core.plugins.scripts'
        
        self._discovered_plugins: dict[str, list] = {
            'classifiers': [],
            'scripts': []
        }
        
        self.logger = lg.getLogger('teisatsu.plugin-manager')
        
        self._script_required_constants = [
            '_TSS_NAME',
            '_TSS_TAGS',
            '_TSS_VERSION',
            '_TSS_DESCRIPTION',
            '_TSS_REQUIREMENTS',
            '_TSS_CLASS',
        ]
    
    
    def discover_plugins(self) -> dict[str, list] | None:
        try:
            classifiers_package = importlib.import_module(self.classifiers_package_path)
            scripts_package = importlib.import_module(self.scripts_package_path)
            
            
            # classifiers discovering
            for _, module_name, is_package in pkgutil.iter_modules(classifiers_package.__path__):
                if not is_package:
                    full_module_name = f"{self.classifiers_package_path}.{module_name}"
                    classifiers = self._load_classifiers(full_module_name)
                    if classifiers:
                        self._discovered_plugins['classifiers'].extend(classifiers)
            
            
            # scripts discovering
            for _, module_name, is_package in pkgutil.iter_modules(scripts_package.__path__):
                if not is_package:
                    full_module_name = f"{self.scripts_package_path}.{module_name}"
                    script = self._load_script(full_module_name)
                    if script:
                        self._discovered_plugins['scripts'].append(script)
            
            
            return self._discovered_plugins
        
        except Exception as e:
            self.logger.error(f'Failed to discover plugins due to error: {str(e)}')
    
    
    def _load_classifiers(self, full_module_name: str) -> list[function]  | None:
        try:
            classifiers = []
            module = importlib.import_module(full_module_name)
            for name, obj in inspect.getmembers(module):
                if name.startswith('is_') and callable(obj):
                    classifiers.append(obj)
            
            return classifiers
        
        except Exception as e:
            self.logger.error(f'Failed to load classifiers due to error: {str(e)}')

    
    
    def _load_script(self, full_module_name: str) -> dict[str, str | function] | None:
        try:
            module = importlib.import_module(full_module_name)
            for constant in self._script_required_constants:
                if not hasattr(module, constant):
                    raise TScriptError(f'Script {full_module_name} must contain attribute \'{constant}\'')
            
            return {
                'name': module._TSS_NAME,
                'tags': module._TSS_TAGS,
                'version': module._TSS_VERSION,
                'description': module._TSS_DESCRIPTION,
                'requirements': module._TSS_REQUIREMENTS,
                'class': module._TSS_CLASS
                
            }
        
        except Exception as e:
            self.logger.error(f'Failed to load script due to error: {str(e)}')
            