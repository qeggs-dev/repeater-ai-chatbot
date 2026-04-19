from types import ModuleType
from dataclasses import dataclass

@dataclass
class ModuleUnit:
    module: ModuleType
    expected_version: str = ""

    def check_version(self):
        self.version == self.expected_version
    
    @property
    def name(self):
        return self.module.__name__
    
    @property
    def version(self):
        return self.module.__version__