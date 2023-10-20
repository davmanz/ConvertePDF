def proc_text(txt):
    txt2 = txt.split(',')
    ar = []
    ar_format = []

    for i in range(len(txt2)):
        if len(txt2[i].split("-")) > 1:
            ar_format.append("range")
            ar.append([int(s) for s in txt2[i].split("-")])
        elif len(txt2[i].split("+")) > 1:
            ar_format.append("join")
            ar.append(tuple([int(s) for s in txt2[i].split("+")]))
        else:
            ar_format.append("numeric")
            ar.append(int(txt2[i]))

    return ar