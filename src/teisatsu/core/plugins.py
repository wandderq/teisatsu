from .base import TScriptError
from .tags import TAG2STR
from collections import defaultdict

import logging as lg
import importlib
import pkgutil
import inspect
import sys


class TPluginManager:
    def __init__(self) -> None:
        self.classifiers_package_path = 'teisatsu.plugins.classifiers'
        self.scripts_package_path = 'teisatsu.plugins.scripts'
        
        self._discovered_plugins: dict[str, list] = {
            'classifiers': [],
            'scripts': []
        }
        
        self.logger = lg.getLogger('teisatsu.plugins.manager')
        
        self._script_required_constants = [
            'TSS_NAME',
            'TSS_TAGS',
            'TSS_VERSION',
            'TSS_DESCRIPTION',
            'TSS_REQUIREMENTS',
            'TSS_CLASS',
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
    
    
    def _load_classifiers(self, full_module_name: str) -> list  | None:
        try:
            classifiers = []
            module = importlib.import_module(full_module_name)
            for name, obj in inspect.getmembers(module):
                if name.startswith('is_') and callable(obj):
                    classifiers.append(obj)
            
            return classifiers
        
        except Exception as e:
            self.logger.warning(f'Failed to load classifiers due to error: {str(e)}')

    
    
    def _load_script(self, full_module_name: str) -> dict | None:
        try:
            module = importlib.import_module(full_module_name)
            for constant in self._script_required_constants:
                if not hasattr(module, constant):
                    raise TScriptError(f'Script {full_module_name} must contain attribute \'{constant}\'')
            
            return {
                'name': module.TSS_NAME,
                'tags': module.TSS_TAGS,
                'version': module.TSS_VERSION,
                'description': module.TSS_DESCRIPTION,
                'requirements': module.TSS_REQUIREMENTS,
                'class': module.TSS_CLASS
                
            }
        
        except Exception as e:
            self.logger.warning(f'Failed to load script due to error: {str(e)}')



class TClassifierManager:
    def __init__(self, classifiers: list) -> None:
        self.logger = lg.getLogger('teisatsu.plugins.classifier-manager')
        self.classifiers = classifiers
    
    
    def classify(self, thing: str) -> list[int] | None:
        self.logger.info(f'Classifying: {thing}')
        
        tags = []
        for classifier in self.classifiers:
            tag = classifier(thing)
            if tag:
                self.logger.debug(f'Classified tag {TAG2STR[tag]}')
                tags.append(tag)
        
        return tags if tags else None


class TScriptManager:
    def __init__(self, scripts: list) -> None:
        self.logger = lg.getLogger('teisatsu.plugins.script-manager')
        self.scripts = scripts
    
    
    def run_script(self, script, thing: str):
        self.logger.debug(f'Running script: {script["name"]}')
        s = script['class']()
        return s.run(thing)
    
    
    def iter_scripts(self, tags: list[int]):
        for script in self.scripts:
            self.logger.debug(f'Checking if script {script["name"]} contains any of the tags: {tags}')
            if any([tag in script['tags'] for tag in tags]):
                self.logger.debug(f'Script {script["name"]} match')
                yield script