from ..core.groups import TAGS
from typing import Any

import logging as lg


class ClassifierError(Exception):
    pass

class TeisatsuClassifier:
    def __init__(self, thing: Any) -> None:
        self.logger = lg.getLogger('teisatsu.classifier')
        self.thing = thing
    
    
    def classify(self) -> list[str]:
        thing_tags = []
        
        for tag in TAGS:
            if tag['func'](self.thing):
                thing_tags.append(tag['name'])
        
        if not thing_tags:
            self.logger.error(f'Failed to classificate: {self.thing}')
        
        return thing_tags