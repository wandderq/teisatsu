from datetime import datetime

import copy

class TDataProcessor:
    def __init__(self) -> None:
        pass
    
    
    def _process_list(self, data: list) -> list:
        for i, obj in enumerate(data):
            if isinstance(obj, dict):
                data[i] = self._process_dict(obj)
                continue
    
            if isinstance(obj, list):
                data[i] = self._process_list(obj)
                continue
            
            # processiong here
            if isinstance(obj, datetime):
                data[i] = obj.strftime("%d/%m/%Y, %H:%M:%S")
            
            # if obj is None:
            #     del data[i]
        
        return data
    
    
    def _process_dict(self, data: dict) -> dict:
        # none_data = []
        for key, value in data.items():
            if isinstance(value, dict):
                data[key] = self._process_dict(value)
                # if none: none_data.extend(none)
                continue
            
            if isinstance(value, list):
                data[key] = self._process_list(value)
                continue
            
            # processing here
            if isinstance(value, datetime):
                data[key] = value.strftime("%d/%m/%Y, %H:%M:%S")
            
            # if value is None:
            #     none_data.append(key)
            #     del data[key]
        
        return data #, none_data
    
    
    def process(self, raw_data: dict):
        raw_data_copy = copy.deepcopy(raw_data)
        return self._process_dict(raw_data_copy)
