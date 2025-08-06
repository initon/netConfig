import json
import sys


class Settings:

    def __init__(self, path):
        self.config_devices = None
        self.path = path

    def load_config(self):
        try:
            with open(self.path, encoding='utf-8-sig') as f:
                self.config_devices = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as error:
            sys.exit(1)
