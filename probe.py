max_page = 9

txt = '8'

a = txt.replace('+',',')
b = a.replace('-',',')
c = b.split(',')

for x in c:
    if int(x) > max_page:
        print('STOP')