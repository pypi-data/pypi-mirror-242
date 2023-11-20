import os
from configparser import ConfigParser
from pathlib import Path
from typing import TypedDict

BASE_URL = "https://pflops-proxy-1234.fly.dev"


class FileInfo(TypedDict):
    name: str
    size: int


def is_logged_in() -> bool:
    config_path = os.path.join(Path.home(), ".pflops.config")
    config = ConfigParser()
    config.read(config_path)
    return "Authentication" in config
