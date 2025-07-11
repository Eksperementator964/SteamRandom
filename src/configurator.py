import platform
import configparser
import getpass
import json
from os import path

from searching import find_games


def get_os_name() -> str:
    result = platform.system().lower()
    if result == 'darwin':
        return 'macos'
    return result

def set_os(new_os:str):
        parser = configparser.ConfigParser()
        parser.read('config.cfg')
        parser['SYSTEM']['os'] = new_os
        with open('config.cfg', 'w') as cfgfile:
            parser.write(cfgfile)

def get_default_steamapps_path():
    with open('defaults.json', mode='r') as dftfile:
        dft_data = json.load(dftfile)

    os_name = get_os_name()
    res_path = dft_data['steampath'][os_name]
    if os_name == 'macos':
        res_path = f'/Users/{getpass.getuser()}/' + res_path

    if path.exists(res_path):
        return res_path
    return None


def global_cofiguration():
    data = {}
    data['os'] = get_os_name()
    data['default_path'] = get_default_steamapps_path()
    with open('defaults.json', mode='r') as dftfile:
        dft_data = json.load(dftfile)
    data['launch'] = dft_data['launch'][data['os']]
    data['apps'] = {}

    with open('config.json', mode='w') as configfile:
        json.dump(data, configfile)

if __name__ == "__main__":
    global_cofiguration()