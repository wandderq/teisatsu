from typing import Any
from validators import ValidationError

import logging as lg
import validators


class BunrukiClassifierError(Exception):
    pass


class BunrukiClassifier:
    def __init__(self, thing: Any) -> None:
        self.logger = lg.getLogger('teisatsu.bunruki')
        self.thing = thing
        
        
        self.tags_lv1 = {name.replace('is_', ''): getattr(self, name) for name in BunrukiClassifier.__dict__.keys() if name.startswith('is_')}
        
        self.tags_lv2 = {}
    
    
    def classify(self, raise_exception=False) -> list[str] | bool:
        tags = []
        
        # Level 1 processing
        for tag, method in self.tags_lv1.items():
            if method(self.thing):
                self.logger.debug(f'{self.thing} got tag {tag} on lv1')
                tags.append(tag)
        
        # Level 2 processing
        for tag, method in self.tags_lv2.items():
            if method(self.thing):
                self.logger.debug(f'{self.thing} got tag {tag} on lv2')
                tags.append(tag)
        
        
        if not tags and raise_exception:
            self.logger.critical(f"Failed to classificate: {self.thing}")
            # raise BunrukiClassifierError(f"Failed to classificate: {self.thing}")
            return False
        
        self.logger.info(f'Classified as: {", ".join(tags)}')
        return tags
    
    
    
    # begin of classification methods
    # must be a lot of them
    
    # PARSED FROM validators LIB
    @staticmethod
    def is_ipv4(thing: Any) -> bool:
        if type(validators.ipv4(thing)) == ValidationError:
            return False
        return True
    
    
    @staticmethod
    def is_ipv6(thing: Any) -> bool:
        if type(validators.ipv6(thing)) == ValidationError:
            return False
        return True
    
    
    @staticmethod
    def is_domain(thing: Any) -> bool:
        if type(validators.domain(thing)) == ValidationError:
            return False
        return True
    
    
    @staticmethod
    def is_url(thing: Any) -> bool:
        if type(validators.url(thing)) == ValidationError:
            return False
        return True
    
    
    @staticmethod
    def is_email(thing: Any) -> bool:
        if type(validators.email(thing)) == ValidationError:
            return False
        return True
    
    
    @staticmethod
    def is_credit_card(thing: Any) -> bool:
        if type(validators.card_number(thing)) == ValidationError:
            return False
        return True
    
    
    @staticmethod
    def is_iban(thing: Any) -> bool:
        if type(validators.iban(thing)) == ValidationError:
            return False
        return True