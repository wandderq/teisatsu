from ...core.base import TScriptBase
from ...core.tags import Tag
from typing import Any

import socket


class GetIPScript(TScriptBase):
    def __init__(self) -> None:
        super().__init__(TSS_SCRIPT)
        
            
    def run(self, thing: Any) -> dict[str, Any]:
        try:
            addr = socket.gethostbyname(thing)
            self.data['ip'] = addr
            
        except Exception as e:
            self.logger.error(f'Error: {str(e)}')
        
        return self.data



TSS_SCRIPT = {
    'name': 'get-ip-by-name',
    'tags': [Tag.DOMAIN, Tag.HOSTNAME],
    'version': '0.2.0',
    'requirements': None,
    'class': GetIPScript,
    'desc': "Uses socket.gethostbyname to find domain/hostname's IP"
}