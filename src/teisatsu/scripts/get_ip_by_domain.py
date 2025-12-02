from typing import Any
from ..core.script import TeisatsuScript

import socket


class GetDomainScript(TeisatsuScript):
    def __init__(self) -> None:
        super().__init__(TSS_NAME, TSS_TAGS, TSS_REQUIREMENTS)
    
    
    def run(self, thing: Any) -> dict[str, Any]:
        addr = socket.gethostbyname(thing)
        return {'thing': thing, 'ipv4-addr': addr}


# Teisatsu Script Configuration
TSS_NAME = 'get-ip-by-domain'
TSS_TAGS = ['domain']
TSS_REQUIREMENTS = []
TSS_CLASS = GetDomainScript
