import os
from steam.client import SteamClient 
from steam.enums import EResult
import configparser 

def find_executable(filenam, directory): #Поиск исполняемого файла
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
        return result['apps']
    else:
        print('ERROR!')
        return None

def get_executable_paths(app_ids: list) -> dict: # Получение пути до исполняемого файла
    config = configparser.ConfigParser()
    config.read('config.cfg')

    apps = request_steam_data(app_ids)
    paths = {}
    if apps == None:
        return None
    for id in app_ids:
        for launch_option in apps[id]['config']['launch']:
            os = apps[id]['config']['launch'][launch_option]['config']['oslist']
            if os == config['SYSTEM']['os']:
                paths[id] = apps[id]['config']['launch'][launch_option]['executable']
                break
        else:
            paths[id] = 'None'
    print(paths)
    return paths

if __name__ == '__main__':
    get_executable_paths([413150, 310360, 1286710])
