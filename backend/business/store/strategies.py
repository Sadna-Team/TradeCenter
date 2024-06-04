from abc import ABC, abstractmethod
from typing import List

class Composite(ABC):
    @abstractmethod
    def pass_filter(self):
        pass



class AndFilter(Composite):
    def __init__(self, filters: List[Composite]):
        self.filters: Composite = filters

    def pass_filter(self):
        for filter in self.filters:
            if not filter.pass_filter():
                return False
        return True
    
