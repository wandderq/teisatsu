from .groups import TAGS
from typing import Any


class ClassifierError(Exception):
    ...

class TeisatsuClassifier:
    def __init__(self, thing: Any) -> None:
        self.thing = thing
    
    
    def classify(self, raise_exception = False) -> list[str]:
        thing_tags = []
        
        for tag in TAGS:
            if tag['func'](self.thing):
                thing_tags.append(tag['name'])
        
        if raise_exception and not thing_tags:
            raise ClassifierError(f'Failed to classificate: {self.thing}')
        
        return thing_tags