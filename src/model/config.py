"""Writer: Jinchan Hwang <ghkdwlscks@gmail.com>
"""


import configparser


class Config(configparser.ConfigParser):
    """Configuration object.

    Args:
        config_path (str, optional): Configuration file path. Defaults to "config/config.ini".
    """

    def __init__(self, config_path="config/config.ini"):
        super().__init__()

        self.config_path = config_path
        self.read(self.config_path, encoding="utf-8")
