def examinar_texto(texto):
    resultado = []
    temp = []
    i = 0

    while i < len(texto):
        char = texto[i]

        if char.isdigit():
            temp.append(char)
        elif char == ',':
            if temp:
                resultado.append(temp)
                temp = []
        i += 1

texto = '2 , 8 , 9, 5-6, , 8, 9+3, 16'
resultado = examinar_texto(texto)
print(resultado)