from abc import ABC, abstractmethod
from typing import Any

import logging as lg


class TeisatsuScript(ABC):
    def __init__(self, name: str, tags: list[str], requirements: list[str]) -> None:
        self.name = name
        self.tags = tags
        self.requirements = requirements
        
        self.name = str(self.name).strip().replace(' ', '-').replace('_', '-')
        self.logger = lg.getLogger(f'teisatsu.script.{self.name.lower()}')
    
    @abstractmethod
    def run(self, thing: Any) -> dict[str, Any]:
        ...

# from functools import wraps
# import time

# def _timeit(func):
#     logger = lg.getLogger('teisatsu.script-debug.timeit')
#     @wraps(func)
#     def wrapper(*args, **kwargs):
#         start = time.time()
#         result = func(*args, **kwargs)
#         elapsed = time.time() - start
        
#         logger.debug(f'Func {func.__name__} took {elapsed/60:.4f}s to execute')
        
#         return result
#     return wrapper


# class TeisatsuMeta(type):
#     def __new__(mcs, name, bases, namespace, **kwargs):
#         if 'run' in namespace and not name == 'TeisatsuScript':
#             namespace['run'] = _timeit(namespace['run'])
#         return super().__new__(mcs, name, bases, namespace, **kwargs)

# class TeisatsuScript(ABC, metaclass=TeisatsuMeta):
#     def __init__(self, name: str, tags: list[str], requirements: list[str]) -> None:
#         self.name = name
#         self.tags = tags
#         self.requirements = requirements
        
#         self.name = str(self.name).strip().replace(' ', '-').replace('_', '-')
#         self.logger = lg.getLogger(f'teisatsu.script.{self.name.lower()}')
    
    
    # @abstractmethod
    # def run(self, thing: Any) -> dict[zstr, Any]:
    #     ...