

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
    
        
