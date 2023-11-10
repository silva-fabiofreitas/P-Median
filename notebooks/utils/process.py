import re

   
def stander_text(text):
    '''
        Converte e padroniza string de tempos (1h 6min, 1h, 6min) para minutos
    '''
    if text.find('h') >= 0:
        return convert_compound_text_to_minutes(text)
    return convert_text_to_number(text)
        

def convert_compound_text_to_minutes(text):
    H_TO_MIN = 60 
    # get number with space, ex.: '1 6'
    string = re.sub(string=text, repl=' ', pattern='\D').strip()
    times = [int(time) for time in string.split()]
    if len(times) == 2:
        return times[0] * H_TO_MIN + times[1] 
    return times[0]*H_TO_MIN

def convert_text_to_number(text):
    return int(re.sub(string=text, repl='', pattern='\D'))