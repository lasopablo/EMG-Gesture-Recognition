fp = open("./palabras.txt", "r")
words = list(fp)
fp.close()
vocales = ["a", "e", "i", "o", "u", "á", "é", "í", "ó", "ú"]
diccionario = {}
for w in words:
    w = w[:-1]
    p = ''.join(list(filter(lambda x: not x in vocales, w)))
    if p in diccionario:
        if w not in diccionario[p]:
            diccionario[p].append(w)
    else:
        diccionario[p] = [w]
# print(diccionario)
# ls = []
# for clave in diccionario:
#     ls.append((clave, len(diccionario[clave])))
# ls.sort(reverse=True, key=lambda x: x[1])
# print(ls)
ls = []
for clave in diccionario:
    ls.append((clave, len(diccionario[clave]), diccionario[clave]))
ls.sort(reverse=True, key=lambda x: x[1])
for l in ls:
    print("------------------------------------")
    print(l[0])
    print(l[1])
    print(l[2])
