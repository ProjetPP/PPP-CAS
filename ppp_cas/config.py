"""Configuration module."""
import os
import json
import logging
from ppp_libmodule.config import Config as BaseConfig
from ppp_libmodule.exceptions import InvalidConfig

class Config(BaseConfig):
    __slots__ = ('max_heap', 'timeout')
    config_path_variable = 'PPP_CAS_CONFIG'
    
    def parse_config(self, data):
        self.max_heap = data['max_heap']
        self.timeout = data['timeout']
