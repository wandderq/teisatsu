from ...core.base import TScriptBase
from ...core.tags import Tag
from typing import Any

import socket


class GetIPScript(TScriptBase):
    def __init__(self) -> None:
        super().__init__(globals())
        self.data = {}
            
    def run(self, thing: Any) -> dict[str, Any]:
        try:
            addr = socket.gethostbyname(thing)
            self.data['ip'] = addr
            
        except Exception as e:
            self.logger.error(f'Error: {str(e)}')
        
        return self.data



# TSS - TeiSatsu Script
TSS_NAME = 'get-ip-by-name'
TSS_TAGS = [Tag.DOMAIN, Tag.HOSTNAME]
TSS_VERSION = '0.1.0'
TSS_REQUIREMENTS = []
TSS_CLASS = GetIPScript

TSS_DESCRIPTION = """
First teisatsu script
Finds domain or hostname's IP and returns it
Uses socket.gethostbyname

Should be used as an example script
"""