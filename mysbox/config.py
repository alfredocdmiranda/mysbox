import os
import configparser


def create_config_file():
    config_filename = ".mysboxrc"
    skel_dir = _get_skeleton_dir()

    with open(os.path.join(skel_dir, config_filename+".skeleton")) as f:
        default_config = f.read()

    with open(os.path.expanduser("~/"+config_filename), 'w') as f:
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


def _get_skeleton_dir():
    package_dir, filename = os.path.split(__file__)
    skel_dir = os.path.join(package_dir, 'skeletons')

    return skel_dir
