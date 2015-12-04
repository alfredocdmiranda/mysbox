import os
import configparser


default_config = "[default]\n" \
                 "arduino_path=[]\n"


def create_config_file():
    with open(os.path.expanduser("~/.mysboxrc"), 'w') as f:
        f.write(default_config)

    return True


def load_config():
    if not _check_exist_config_file():
        create_config_file()
    config = configparser.ConfigParser()
    config.read(os.path.expanduser("~/.mysboxrc"))

    return config


def _check_exist_config_file():
    return os.path.exists(os.path.expanduser("~/.mysboxrc"))
