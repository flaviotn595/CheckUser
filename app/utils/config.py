import typing as t
import os
import json

from ..utils.logger import logger


class Config:
    CONFIG_FILE = 'config.json'
    PATH_CONFIG = '/etc/checker/'
    PATH_CONFIG_OPTIONAL = os.path.join(os.path.expanduser('~'), 'checker')

    @property
    def path_config(self) -> str:
        path = os.path.join(self.PATH_CONFIG, self.CONFIG_FILE)

        try:
            if not os.path.exists(path):
                os.makedirs(self.PATH_CONFIG, exist_ok=True)
        except PermissionError:
            path = os.path.join(self.PATH_CONFIG_OPTIONAL, self.CONFIG_FILE)

            if not os.path.exists(path):
                os.makedirs(self.PATH_CONFIG_OPTIONAL, exist_ok=True)

        return path

    @property
    def exclude(self) -> t.List[str]:
        return self.config.get('exclude', [])

    @exclude.setter
    def exclude(self, value: t.List[str]):
        self.config['exclude'] = value
        self.save_config()

    def include(self, name: str) -> bool:
        if name in self.exclude:
            self.exclude.remove(name)
            self.save_config()
            return True

        return False

    @property
    def port(self) -> int:
        return self.config.get('port', 5000)

    @port.setter
    def port(self, value: int):
        self.config['port'] = value
        self.save_config()

    @property
    def config(self) -> dict:
        default_config = {
            'exclude': [],
            'port': 5000,
        }

        if os.path.exists(self.path_config):
            with open(self.path_config, 'r') as f:
                data = json.load(f)
                return data if isinstance(data, dict) else default_config

        return default_config

    def save_config(self, config: dict = None) -> bool:
        config = config or self.config

        with open(self.path_config, 'w') as f:
            f.write(json.dumps(config, indent=4))

    @staticmethod
    def remove_config() -> None:
        if os.path.exists(Config.PATH_CONFIG):
            os.system('rm -rf %s' % Config.PATH_CONFIG)
