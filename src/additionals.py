import json

def break_into_words(string: str, symbol: chr = '"') -> list:
    result = []
    word = ''
    word_flag = True
    for c in string:
        if c == symbol and word_flag:
            word = ''
            word_flag = False
        elif c == symbol and not word_flag:
            result.append(word[1:])
            word_flag = True
        word = word + c
    return result
    
if __name__ == '__main__':
    data = {}
    steampath = {'macos': 'Library/Application Support/Steam/',
                 'windows': 'C:/Program Files (x86)/Steam/',
                 'linux': 'null'}
    data['steampath'] = steampath
    launch_options = {'macos': ['open', '-a'],
                      'windows': [],
                      'linux': []}
    data['launch'] = launch_options
    with open('defaults.json', mode='w') as dftfile:
        json.dump(data, dftfile)