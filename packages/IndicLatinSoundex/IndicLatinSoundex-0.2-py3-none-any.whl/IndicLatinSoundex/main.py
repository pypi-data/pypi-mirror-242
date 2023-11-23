import re

class IndicLatinSoundex:
    def __init__(self) -> None:
        vowels = {
            '1':['a','aa'],
            '2':['i','ee'],
            '3':['u','oo'],
            '4':['e','ai'],
            '5':['o','au','ou'],
            '6':['ae','aae','aaee']
        }
        consonants = {
            'K':['k','kh','kk','q'],
            'G':['g','gh','gg'],
            'C':['ch','chh','chch'],
            'J':['j','jj','jh','z','zh'],
            'T':['t','th','tt'],
            'D':['d','dh','dd','ddh'],
            'N':['n','nn'],
            'P':['p','ph','f','pp','ff'],
            'B':['b','bh','bb'],
            'M':['m','mm'],
            'R':['r','rr'],
            'L':['l','ll'],
            'V':['v','w'],
            'S':['s','sh','ss','c'],
            'H':['h','hh'],
            'X':['ks','ksh','kshh','x'],
            'Z':['dn']
        }

        self.char_mapping = {}
        for key in vowels:
            for new_key in vowels[key]:
                self.char_mapping[new_key] = key
        for key in consonants:
            for new_key in consonants[key]:
                self.char_mapping[new_key] = key

    def __group_chars(self, input_str: str) -> list:
        pattern = re.compile(r'(?<=[^aeiouy])y(?=[^aeiouy])|[^aeiou]+y$')
        if re.search(pattern, input_str):
            groups = re.findall(r'([aeiouy]+|[bcdfghjklmnpqrstvwxz]+)', input_str)
            self.char_mapping['y'] = '2'
        else:
            groups = re.findall(r'([aeiou]+|[bcdfghjklmnpqrstvwxyz]+)', input_str)
            self.char_mapping['y'] = 'Y'
        return groups
    
    def __get_all_slices_recursive(self, word, start=0):
        if start == len(word):
            return [[]]

        result = []
        for end in range(len(word),start,-1):
            slice_combination = word[start:end]
            rest_combinations = self.__get_all_slices_recursive(word, end)
            
            for rest_combination in rest_combinations:
                result.append([slice_combination] + rest_combination)

        return result

    def get_soundex(self, word: str) -> str:
        '''
        accepts a string which can contains multiple words with spaces between them.
        outputs a string of soundex code of input
        '''
        all_words = word.split(' ')
        soundex_list = []

        for one_word in all_words:
            one_word = one_word.lower()
            tokens = self.__group_chars(one_word)
            soundex = ''

            for token in tokens:
                if token in self.char_mapping:
                    soundex += self.char_mapping[token]
                elif len(token)<7:
                    result = self.__get_all_slices_recursive(token)
                    result.remove([token])
                    result = sorted(result, key=len)
                    
                    for combination in result:
                        if all(item in self.char_mapping for item in combination):
                            for subtoken in combination:
                                soundex += self.char_mapping[subtoken]
                            break
              
                else:
                    soundex = 'error'
                    break
            soundex_list.append(soundex)
        return ' '.join(soundex_list)
    
    def compare(self, string1: str, string2: str) -> bool:
        '''
        accepts two words and it will return True if they are same otherwise False.
        '''
        code1 = self.get_soundex(string1)
        code2 = self.get_soundex(string2)
        if code1 == code2:
            return True
        else:
            return False