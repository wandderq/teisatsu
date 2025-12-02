from typing import Any
from ..core.script import TeisatsuScript



class GetWhoisScript(TeisatsuScript):
    def __init__(self) -> None:
        super().__init__(TSS_NAME, TSS_TAGS, TSS_REQUIREMENTS)
    
    
    def run(self, thing: Any) -> dict[str, Any]:
        import whois
        
        return whois.whois(thing)


# Teisatsu Script Configuration
TSS_NAME = 'get-whois-info'
TSS_TAGS = ['domain', 'ipv4', 'url']
TSS_REQUIREMENTS = ['python-whois']
TSS_CLASS = GetWhoisScript
