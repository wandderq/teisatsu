from ...core.base import TScriptBase
from ...core.tags import Tag
from typing import Any


class WhoisLookupScript(TScriptBase):
    def __init__(self) -> None:
        super().__init__(TSS_SCRIPT)
        
            
    def run(self, thing: Any) -> dict[str, Any]:
        import whois
        
        try:
            whois_data = whois.whois(thing)
            self.data.update(whois_data)
        
        except whois.parser.WhoisDomainNotFoundError as e:
            self.logger.error(f'Whois error: domain not found: {str(e)}')
        
        except Exception as e:
            self.logger.error(f'Error: {str(e)}')
        
        return self.data



TSS_SCRIPT = {
    'name': 'whois-lookup',
    'tags': [Tag.DOMAIN, Tag.IPV4, Tag.URL],
    'version': '0.1.0',
    'requirements': ['python-whois'],
    'class': WhoisLookupScript,
    'desc': "Uses python-whois lib to find info about domain/ip/url"
}