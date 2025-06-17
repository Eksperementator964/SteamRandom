import os
import random

def find_executable(filenam, directory): #Поиск исполняемого файла
    for dirpath, _, filenames in os.walk(directory + "\\" + filename):
        for filename in filenames:
            if filename.endswith('.exe'):
                if check_for_words(filename):
                    os.startfile(os.path.join(dirpath, filename))
                    print(os.path.join(dirpath, filename))
                    return False
    return True

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

def check_for_words(filename): 
    with open("ignor_list.txt") as f:
        ignor_list = [i.strip() for i in f]
    for i in range(len(ignor_list)):
        if filename.lower().find(ignor_list[i]) != -1:
                return False
    return True

def init_procedure(): #Процедура инициализации программы
    pass


if __name__ == '__main__':
    pass
