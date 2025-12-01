from typing import Any
from ..core.scripts import TeisatsuScript


class GetDomainScript(TeisatsuScript):
    def __init__(self) -> None:
        super().__init__(TSS_NAME, TSS_TAGS, TSS_REQUIREMENTS)
    
    
    def run(self, thing: Any) -> dict[str, Any]:
        return {'thing': thing}


# Teisatsu Script Configuration
TSS_NAME = 'get-ip-by-domain'
TSS_TAGS = ['domain']
TSS_REQUIREMENTS = []
TSS_OBJECT = GetDomainScript()
