from ..core.tags import TAG2STR

import logging as lg
import importlib
import pkgutil
import inspect


class TClassifierManager:
    def __init__(self) -> None:
        self.logger = lg.getLogger('teisatsu.plugins.classifier-manager')
        self.package_path = 'teisatsu.plugins.classifiers'
        self.classifiers: list = []
    
    
    def load_classifiers(self) -> None:
        try:
            package = importlib.import_module(self.package_path)
            
            # getting all of teisatsu.plugins.classifiers.* modules
            for _, module_name, is_pkg in pkgutil.iter_modules(package.__path__):
                if not is_pkg:
                    
                    # getting all of 'is_' functions from teisatsu.plugins.classifiers.module
                    full_name = f"{self.package_path}.{module_name}"
                    module = importlib.import_module(full_name)
                    
                    for name, obj in inspect.getmembers(module):
                        if name.startswith('is_') and callable(obj):
                            self.classifiers.append(obj)
        
        except Exception as e:
            self.logger.error(f'Failed to load classifiers due to error: {str(e)}')
            
    
    
    def classify(self, thing: str) -> list[int] | None:
        self.logger.info(f'Classificating: {thing}')
        tags = []
        
        for classifier in self.classifiers:
            self.logger.debug(f'Running {classifier.__name__}')
            tag = classifier(thing)
            
            if tag:
                self.logger.debug(f'Classified tag {TAG2STR[tag]}')
                tags.append(tag)
        
        return tags if tags else None
