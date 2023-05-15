import copy

def get_T_NF(string, kind, alphabet):
    check = True
    i = 0
    out = []
    while i in range(len(string)):
        if string[i] == '(':
            check = True
            out.append('')
            i += 1
        elif string[i] == ')':
            check = False

        if check:
            if string[i] in alphabet:
                out[-1] += string[i]
            elif string[i] == '~':
                out[-1] += string[i] + string[i+1]
                i += 1
        i += 1
    string = copy.deepcopy(out)

    def get_short_form(value):
        using_variable = set()
        out = set()
        for i in range(len(value)):
            for k in range(len(value)):

                if k == i:
                    continue

                size = len(value[i])
                check = size
                j = 0
                while j < size:
                        if value[i][j] != '~':
                            if value[k].count(value[i][j]) <= 0:
                                if value[k].count(f'~{value[i][j]}') > 0:
                                    check -= 1
                                else:
                                    check -= 2
                            else:
                                if value[k].count(f'~{value[i][j]}') > 0:
                                    check -= 1
                        else:
                            if value[k].count(value[i][j] + value[i][j+1]) <= 0:
                                if value[k].count(value[i][j+1]) > 0:
                                    check -= 1
                                else:
                                    check -= 2
                            j += 1
                        j += 1

                if check == size - 1:
                    timing = ''
                    j = 0
                    while j < size:
                        if value[i][j] != '~':
                            if value[i][j] in value[k] and value[k].count(f'~{value[i][j]}') <= 0:
                                timing += str(value[i][j])
                        else:
                            if (value[i][j] + value[i][j + 1]) in value[k]:
                                timing += str(value[i][j] + value[i][j + 1])
                            j += 1
                        j += 1
                    using_variable.add(value[i])
                    using_variable.add(value[k])
                    out.add(timing)

        for i in range(len(value)):
            if value[i] in using_variable:
                pass
            else:
                out.add(value[i])

        if len(list(out)) == 0:
            out = set(value)
        return out

    def print_T_NF(value, kind):
        out = ''
        if kind == 'PCNF':
            symbol1 = '|'
            symbol2 = '&'
        else:
            symbol1 = '&'
            symbol2 = '|'
        for elements in range(len(value)):
            out += '('
            i = 0
            while i in range(len(value[elements])):
                if value[elements][i] is '~':
                    out += f'{value[elements][i]+value[elements][i+1]+symbol1}'
                    i += 1
                elif value[elements][i] is '+':
                    out = list(out)
                    out[len(out) - 1] = ''
                    out = "".join(out)
                    out += f'){symbol2}('
                else:
                    out += f'{value[elements][i]+symbol1}'
                i += 1
            out = list(out)
            out[len(out) - 1] = ''
            out = "".join(out)
            out += ')' + symbol2
        out = list(out)
        out[-1] = ''
        out = "".join(out)
        return f'{kind}: {out}'

    while True:
        if out == list(get_short_form(out)):
            break
        else:
            out = list(get_short_form(out))

    spisok = copy.deepcopy(out)
    for i in range(len(out)):
        if type(out[i]) is str:
            out.append([])
            value = ''
            for j in range(len(out[i])):
                if out[i][j] in alphabet:
                    value += out[i][j]
                    out[-1].append(value)
                    value = ''
                else:
                    value += out[i][j]
        else:
            break
    while True:
        if type(out[0]) is str:
            del out[0]
        else:
            break

    def prototype(value):
        out = []

        for i in range(3):
            if value.count(alphabet[i]) <= 0:
                out.append('o')
            else:
                out.append('x')

        return out

    def compare(value_list):
        out = set()
        for element_1 in value_list.keys():
            for element_2 in value_list.keys():
                if element_1 == element_2:
                    continue
                check = True
                for i in range(len(value_list[element_1])):
                    if value_list[element_1][i] == 'o' and value_list[element_2][i] == 'o':
                        check = False
                if check:
                    timing = ''
                    timing += element_1 + '+' + element_2
                    out.add(timing)
                    value_list[element_1] = ['o'] * len(value_list[element_2])
                    value_list[element_2] = ['o'] * len(value_list[element_1])
        return out

    spisok2 = copy.deepcopy(out)

    out = dict()
    for i in range(len(spisok)):
        out[spisok[i]] = prototype(spisok[i])
    out = compare(out)
    return print_T_NF(list(out), kind)

def mac_claski(string, kind, alphabet):
    title = get_T_NF(string, kind, alphabet)
    print(f'table-calculated {title}')

def truth_table(using_letters, variable_dict):
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

def karno_card(result, using_letters, variable_dict, alphabet):
    out = []
    using_variable = {}

    for value in variable_dict.keys():
        if value in alphabet or value is result:
            using_variable[value] = variable_dict[value]

    size = int((len(using_variable.keys())-1)/2)
    out.append([''])

    for letter in range(len(using_variable.keys())-1):
        if letter < size:
            out[-1][-1] += alphabet[letter]
        elif letter == size:
            out[-1][-1] += '/'
            out[-1][-1] += alphabet[letter]
        else:
            out[-1][-1] += alphabet[letter]

    table = truth_table(using_letters, variable_dict)
    cases_y = set()
    cases_x = set()
    for i in range(len(table[0])):
        string = ''
        for j in range(size):
            string += str(table[j][i])
        cases_y.add(string)
        string = ''
        for j in range(len(out[-1][-1]) - size - 1):
            string += str(table[j][i])
        cases_x.add(string)
    cases_x = sorted(cases_x, key=lambda value: int(value))
    cases_y = sorted(cases_y, key=lambda value: int(value))

    for l in cases_y:
        out[0].append(l)
    for l in cases_x:
        out.append([l])
    x=y=1
    z = 0

    while y < len(out[0]):
        while x < len(out):
            out[x].append(using_variable[result][z])
            x += 1
            z += 1
        y += 1
        x = 1

    def print_karno_card():
        print('Karno card:')
        for i in range(len(out[0])):
            if i > 0:
                for j in range(len(out)):
                    print(f'  {out[j][i]}', end='')
            else:
                for j in range(len(out)):
                    print(f'{out[j][i]}', end=' ')
            print('')

    print_karno_card()