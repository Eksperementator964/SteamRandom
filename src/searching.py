import os
import getpass
from steam.client import SteamClient 
from steam.enums import EResult
import json
import vdf

from additionals import break_into_words

def find_games() -> str:
    apps_to_add = []
    apps = get_apps_info()
    with open('config.json', mode='r') as cfgfile:
        config_data = json.load(cfgfile)
    
    for app_id in apps:
        if app_id in config_data['apps']:
            if os.path.exists(config_data['apps'][app_id]['installdir']):
                continue
            config_data['apps'].pop(app_id)
        apps_to_add.append(int(app_id))
    if not apps_to_add:
        return "No need to add/modify games' paths"
    

    exe_paths = get_steam_executables(apps_to_add)
    for app_id in exe_paths:
        apps[str(app_id)]['installdir'] = apps[str(app_id)]['installdir'] + '/' + exe_paths[app_id]
        apps[str(app_id)]['installdir'] = apps[str(app_id)]['installdir'].replace('\\', '/')
        config_data['apps'][str(app_id)] = apps[str(app_id)]
    
    with open('config.json', mode='w') as cfgfile:
        json.dump(config_data, cfgfile)
    return "Successfully added/modified games' paths"


def find_executable(filename, directory): #Поиск исполняемого файла
    for dirpath, _, filenames in os.walk(directory + "\\" + filename):
        for filename in filenames:
            if filename.endswith('.exe'):
                if check_for_words(filename):
                    os.startfile(os.path.join(dirpath, filename))
                    print(os.path.join(dirpath, filename))
                    return False
    return True

def check_for_words(filename): 
    with open("ignor_list.txt") as f:
        ignor_list = [i.strip() for i in f]
    for i in range(len(ignor_list)):
        if filename.lower().find(ignor_list[i]) != -1:
                return False
    return True

def request_steam_data(app_ids: list) -> dict: #Получение конфигурационных данных игр по их ID в Steam
    client = SteamClient()

    login_result = client.anonymous_login()
    if login_result == EResult.OK:
        result = client.get_product_info(apps=app_ids)
        client.logout()
        # if not result:
        #     print("No game data!") #исправить!
        #     return None
        return result['apps']
    else:
        print('ERROR!')
        return None

def get_steam_executables(app_ids: list) -> dict: # Получение пути до исполняемого файла
    with open('config.json', mode='r') as cfgfile:
        data = json.load(cfgfile)

    apps = request_steam_data(app_ids)
    paths = {}
    if apps == None:
        return None
    for id in app_ids:
        for launch_option in apps[id]['config']['launch']:
            os = apps[id]['config']['launch'][launch_option]['config']['oslist']
            if os == data['os']:
                paths[id] = apps[id]['config']['launch'][launch_option]['executable']
                break
        else:
            paths[id] = 'None'
    return paths

def get_lib_folders() -> list: 
    if not os.path.exists('config.json'):
        return 'Config file was not found!'
    
    with open('config.json', mode='r') as cfgfile:
        data = json.load(cfgfile)
        path_start = data['default_path']
    
    if not os.path.exists(path_start + 'steamapps/libraryfolders.vdf'):
        return 'libraryfolders.vdf was not found!'
    
    paths = []
    with open(path_start + 'steamapps/libraryfolders.vdf', mode='r') as vdfile:
        data = vdfile.readlines()
        for row in data:
            if 'path' in row:
                result = break_into_words(row)
                paths.append((result[1] + '/steamapps/'))
    return paths

def get_apps_info() -> dict:
    lib_folders_paths = get_lib_folders()
    apps = {}

    for lib_path in lib_folders_paths:
        if os.path.exists(lib_path):
            dir_data = os.scandir(lib_path)
            for file in dir_data:
                filename = file.name
                if filename.endswith('.acf'):
                    id = filename[filename.find('_') + 1:filename.find('.acf')]
                    apps[id] = read_acf_file(lib_path + file.name)
                    apps[id]['installdir'] = lib_path + 'common/' + apps[id]['installdir']
    return apps

def read_acf_file(filename: str) -> dict:
    app_data = {}

    with open(filename, mode='r') as acf_file:
        data = vdf.load(acf_file)['AppState']
    app_data['appid'] = data['appid']
    app_data['name'] = data['name']
    app_data['installdir'] = data['installdir']
    return app_data

def build_path() -> dict:
    pass

if __name__ == '__main__':
    find_games()