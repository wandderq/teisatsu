# from collections import defaultdict
from typing import Any


class TeisatsuInfoProcessor:
    def __init__(self, raw_info: dict) -> None:
        self.raw_info = raw_info
    
    
    def summary(self) -> dict[str, Any]:
        all_pairs = []
        for script_name, script_results in self.raw_info.items():
            for key, val in script_results.items():
                if not (key, val) in all_pairs:
                    all_pairs.append((key, val))
        
        
        return {k: v for k, v in all_pairs}