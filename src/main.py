import os
import random
from searching import find_executable, get_executable_paths



def start_game():   #Запуск случайной игры
    directory_C = "C:\\Program Files (x86)\\Steam\\steamapps\\common"
    directory_D = 'D:\\SteamLibrary\\steamapps\\common'
    directory_E = "E:\\SteamLibrary\\steamapps\\common"
    path = ' '
    x = True
    if os.path.exists(directory_C):
        folders_C = [entry.name for entry in os.scandir(directory_C) if entry.is_dir()]
    else:
        folders_C =[]

    if os.path.exists(directory_D):
        folders_D = [entry.name for entry in os.scandir(directory_D) if entry.is_dir()]
    else:
        folders_D =[]
    if os.path.exists(directory_E):
        folders_E = [entry.name for entry in os.scandir(directory_E) if entry.is_dir()]
    else:
        folders_E =[]

    folders_All = folders_C + folders_D + folders_E

    while x:
        random_game_number = random.randint(0, len(folders_All) - 1)
        if random_game_number < len(folders_C):
            x = start_game(folders_C[random_game_number],directory_C)

        elif random_game_number - len(folders_C) < len(folders_D):
            x = start_game(folders_D[random_game_number - len(folders_C)], directory_D)

        else:
            x = start_game(folders_E[random_game_number - len(folders_C) - len(folders_D)], directory_E)

def init_procedure(): #Процедура инициализации программы
    pass
    


if __name__ == '__main__':
    init_procedure()
