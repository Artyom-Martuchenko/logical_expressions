from src.minimization import *
from src.PCNF import PCNF, numbers_PCNF
from src.PDNF import PDNF, numbers_PDNF
from src.operations import operations


variable_dict = {}
alphabet = []

def index_find(result):
    out = 0
    for i in range(len(variable_dict[result])):
        if variable_dict[result][i] == 1:
            out += 2**(len(variable_dict[result])-i-1)
    print(f"Index form: {out}")
    return out

def checks(string, alphabet):
    output = 0
    function = 0
    using_letters = set()
    for i in range(len(string)):
        if string[i] is "(":
            j = i
            while j < len(string):
                if string[j] is ")":
                    output += 1
                    j = len(string) - 1
                j += 1
        elif string[i] in alphabet:
            using_letters.add(string[i])
            function += 1
    def convert_set_to_list(value):
        out = []
        for element in value:
            out.append(element)
        out.sort()
        return out
    using_letters = convert_set_to_list(using_letters)
    using_letters.sort()
    return [using_letters, output]

def truth_table(using_letters):
    global variable_dict
    size = 2**len(using_letters)
    table = [[0] * size for i in range(len(using_letters)+1)]
    for i in range(len(table) - 1):
        size /= 2
        size1 = size
        value = True
        for j in range(len(table[i])):
            if size1 == 0:
                value = not value
                size1 = size
            if value:
                table[i][j] = 0
                size1 -= 1
            else:
                table[i][j] = 1
                size1 -= 1
    using_letters = list(using_letters)
    using_letters.sort()
    for i in range(len(using_letters)):
        variable_dict[using_letters[i]] = table[i]
    return table

def print_truth_table(alphabet, result):
    for letter in variable_dict.keys():
        if letter.find('|') == -1 and letter.find('&') == -1:
            print(letter, end='')
    print('Result')
    for j in range(len(variable_dict['A'])):
        for i in variable_dict.keys():
            if i in alphabet or i is result:
                print(variable_dict[i][j], end='')
        print('')

def define_function(string):
    small_task = []
    for i in range(len(string)):
        if string[i] is '(':
            check = True
            j = i + 1
            fragment = ""
            while string[j] is not ')' or check is not True:
                fragment += string[j]
                if string[j] is ')' and check is False:
                    check = True
                elif string[j] is '(' and j is not i:
                    check = False
                j += 1
            variable_dict[fragment] = []
            small_task.append(fragment)
    return small_task

if __name__ == '__main__':
    print('-' * 25, end='')
    print('2LR', end='')
    print('-' * 25)

    formula = "A&(B|C)"

    alphabet = list(map(chr, range(97, 123)))
    def up(literal):
       return literal.upper()
    alphabet = map(up, alphabet)
    alphabet = list(alphabet)

    out = checks(formula, alphabet)
    truth_table(out[0])
    spisok = define_function(formula)
    spisok.insert(0, formula)
    variable_dict[formula] = []
    for i in range(2**len(out[0])):
        operations(spisok, i, variable_dict)
    result = ''
    for key in variable_dict.keys():
        if len(key) > len(result):
            result = key
    print_truth_table(alphabet, result)
    index_find(result)
    print(f'PCNF: {PCNF(result, variable_dict)}')
    print(f'PDNF: {PDNF(result, variable_dict)}')
    print(f'numbers PCNF: {numbers_PCNF(result, variable_dict)}')
    print(f'numbers PDNF: {numbers_PDNF(result, variable_dict)}')
    print('-' * 25, end='')
    print('3LR', end='')
    print('-' * 25)
    mac_claski(PCNF(result, variable_dict), 'PCNF', alphabet)
    mac_claski(PDNF(result, variable_dict), 'PDNF', alphabet)
    title = get_T_NF(PCNF(result, variable_dict), 'PCNF', alphabet)
    print(f'calculated {title}')
    title = get_T_NF(PDNF(result, variable_dict), 'PDNF', alphabet)
    print(f'calculated {title}')
    karno_card(result, out[0], variable_dict, alphabet)
    title = get_T_NF(PCNF(result, variable_dict), 'PCNF', alphabet)
    print(f'table {title}')
    title = get_T_NF(PDNF(result, variable_dict), 'PDNF', alphabet)
    print(f'table {title}')