def formato_number(number):
    resultado = []
    tmp_txt = ''

    for x in number:
        if x == ',':
            if '-' in tmp_txt:
                a = tmp_txt.replace('-',',')
                resultado.append([a])
                tmp_txt = ''
            elif '+' in tmp_txt:
                b = tmp_txt.replace('+',',')
                resultado.append((b,))
                tmp_txt = ''
            else:
                resultado.append(tmp_txt)
                tmp_txt = ''
        else:
            tmp_txt += x

    return resultado

def examinar_texto(let_txt):
    let = formato_number(let_txt)
    t_int = []

    for x in let:
        if isinstance(x, str):
            t_int.append(int(x))
        
        elif isinstance(x, tuple):
            xx = x[0].split(',')
            tupla = tuple(int(valor) for valor in xx)
            t_int.append(tupla)

        elif isinstance(x, list):
            xx = x[0].split(',')
            box_list = []
            for m in xx:
                box_list.append(int(m))
            t_int.append(box_list)

        else:
            pass
    print(t_int)

    return t_int

