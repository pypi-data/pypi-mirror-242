from dataclasses import dataclass, field
from dotenv import dotenv_values
from typing import *

@dataclass
class SystemSettings:
    openai_api_key: str

    def __post_init__(self):
        self.openai_api_key = str(self.openai_api_key)


def load_env_vars() -> SystemSettings:
    env_vars = dict(dotenv_values())
    new = {}
    for index, (key, value) in enumerate(env_vars.items()):
        new[key.lower()] = value
    lower_case_settings = dict(map(lambda x: (x[0].lower(), x[1]), env_vars.items()))
    return SystemSettings(**lower_case_settings)