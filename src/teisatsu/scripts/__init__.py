import logging as lg
import pkgutil
import importlib


_TSS_REQUIRED_ATTRS= [
    'TSS_NAME',
    'TSS_TAGS',
    'TSS_REQUIREMENTS',
    'TSS_CLASS'
]

logger = lg.getLogger('teisatsu.scripts.init')

scripts_list = []

for loader, module_name, is_pkg in pkgutil.iter_modules(__path__):
    if not is_pkg:
        module = importlib.import_module(f'.{module_name}', __package__)
        logger.debug(f'Processing module: {module.__name__}')
        
        passed = True
        for attr in _TSS_REQUIRED_ATTRS:
            if not hasattr(module, attr):
                logger.error(f'Script {module.__name__} hasn\'t attr {attr}')
                passed = False
        
        if passed:
            scripts_list.append(module)
            globals()[module_name] = module
            