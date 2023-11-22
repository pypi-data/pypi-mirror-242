from guerrilla.device.router.config import BaseConfig
from dataclasses import dataclass
from .top import MainConfig

@dataclass
class Config(BaseConfig, MainConfig):
    """
    A class representing the configuration of a router device.
    """
    pass
    
    

