
def PCNF(result, variable_dict, check = False):
    out = ''
    variable = set()
    for i in range(len(variable_dict[result])):
        if variable_dict[result][i] == 0:
            out += '('
            for key in variable_dict.keys():
                if key.find('|') == -1 and key.find('&') == -1:
                    if variable_dict[key][i] is 1:
                        variable.add(i)
                        out += f'~{key}|'
                    else:
                        variable.add(i)
                        out += f'{key}|'
            out = list(out)
            out[len(out)-1] = ''
            out = "".join(out)
            out += ')&'
    out = list(out)
    out[len(out) - 1] = ''
    out = "".join(out)
    if check:
        return variable
    else:
        return out

def numbers_PCNF(result, variable_dict):
    out = ''
    for i in range(len(variable_dict[result])):
        if variable_dict[result][i] == 0:
            for key in variable_dict.keys():
                if key.find('|') == -1 and key.find('&') == -1:
                    out += str(variable_dict[key][i])
            out += '&'
    out = list(out)
    out[len(out) - 1] = ''
    out = "".join(out)
    return out