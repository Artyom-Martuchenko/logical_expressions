# from main import variable_dict
import copy

def operations(small_task, ordine, variable_dict, check = False):
    def inversion(string, variables, check = False):
        symbol = string.find('~')
        if variables[string[symbol+1]] is 0:
            variables[string[symbol+1]] = 1
        else:
            variables[string[symbol+1]] = 0
        string = list(string)
        string[symbol] = ''
        string = "".join(string)
        symbol = string[symbol]
        if check:
            return variables[symbol]
        else:
            return [string, variables]

    def conjunction(string, variables):
        while string.find('~') != -1:
            out = inversion(string, variables)
            string = out[0]
            variables = out[1]
        symbol = string.find('&')
        if variables[string[symbol + 1]] is 1 and variables[string[symbol - 1]] is 1:
            return 1
        else:
            return 0


    def disgiunzione(string, variables):
        while string.find('~') != -1:
            out = inversion(string, variables)
            string = out[0]
            variables = out[1]
        symbol = string.find('|')
        if variables[string[symbol + 1]] is 0 and variables[string[symbol - 1]] is 0:
            return 0
        else:
            return 1

    def big_function(string):
        i = 0
        lst = {}
        alphabet = list(map(chr, range(97, 123)))
        while i < len(small_task):
            if small_task[i] in string and small_task[i] is not string:
                string = string.replace(f"({small_task[i]})", f"{alphabet[len(alphabet) - 1]}", 8)
                lst[alphabet[len(alphabet) - 1]] = variable_dict[small_task[i]][ordine]
                del alphabet[len(alphabet) - 1]
            i += 1

        for j in range(len(alphabet)):
            if alphabet[j].upper() in string:
                lst[alphabet[j].upper()] = variable_dict[alphabet[j].upper()][ordine]

        if '|' in string:
            return disgiunzione(string, lst)
        elif '&' in string:
            return conjunction(string, lst)
        elif '~' in string:
            return inversion(string, lst, True)
        print(string)

    variable = {}
    for key in variable_dict.keys():
        if key.find('|') == -1 and key.find('&') == -1:
            variable[key] = variable_dict[key][ordine]
    i = len(small_task) - 1
    while(i > -1):
        if '(' in small_task[i]:
            variable_dict[small_task[i]].append(big_function(small_task[i]))
            i -= 1
        elif '&' in small_task[i]:
            variable_dict[small_task[i]].append(conjunction(small_task[i], copy.deepcopy(variable)))
            i -= 1
        elif '|' in small_task[i]:
            variable_dict[small_task[i]].append(disgiunzione(small_task[i], copy.deepcopy(variable)))
            i -= 1