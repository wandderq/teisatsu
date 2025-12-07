from ...core.base import TScriptBase
from ...core.tags import Tag
from typing import Any



class IPAPIsLookupScript(TScriptBase):
    def __init__(self) -> None:
        super().__init__(TSS_SCRIPT)
        self.api_list = [
            'http://ip-api.com/json/{}',
            'https://ipinfo.io/{}/json',
            'https://freegeoip.app/json/{}',
            
        ]
        
            
    def run(self, thing: Any) -> dict[str, Any]:
        try:
            import cloudscraper
            import fake_useragent
            
            scraper = cloudscraper.create_scraper()
            user_agent = fake_useragent.UserAgent()
             
            for api_url in self.api_list:
                try:
                    url = api_url.format(thing)
                    headers = {'User-Agent': user_agent.random}
                    
                    self.logger.debug(f'Sending GET request to {url} with headers {headers}')                    
                    responce = scraper.get(url=url, headers=headers,timeout=3)
                    
                    self.data.update(responce.json())
                
                
                except Exception as e:
                    self.logger.error(f'Failed to GET: {api_url.format(thing)} due to error: {str(e)}')
                    continue
            
            
        except Exception as e:
            self.logger.error(f'Error: {str(e)}')
        
        return self.data



TSS_SCRIPT = {
    'name': 'ip-apis-lokup',
    'tags': [Tag.IPV4, Tag.IPV6],
    'version': '0.1.0',
    'requirements': ['requests', 'cloudscraper', 'fake-useragent'],
    'class': IPAPIsLookupScript,
    'desc': "Uses public APIs to find some info about IP"
}