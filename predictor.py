import pygtrie
import pickle
import pyttsx3

## Orden para predecir palabra. Iniciar un diccionario con cargar_por_lista o
## cargar por archivo con cargar_diccionario.
## Lo que hacemos es gesto_a_letra y se va añadiendo a la palabra interna.
## Si quires predecir llamas a predecir_palabra con un diccionario. Te devuelve
## una lista si es de longitud 1 es que solo hay una palabra. Si devuelve False
## es que no esta la clave.
## devuelve False es que hay mas de un match. Si te devuelve una palabra
## es esa.
## Si no quires predecir llamas a get_palabra_actual.
## De cualquiera de las dos llamas a escuchar_palabra y luego a
## reset_palabra_actual.
## Si quieres usar las 200 mas usas palabras_mas_usadas -> cargar_por_lista
## y luego pasarias ese diccionario a predecir.
## Si quieres guardar y cargar las palabras mas usadas usas guardar y cargar.
class Principal():
    engine = pyttsx3.init()
    rate = engine.getProperty('rate')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', 'spanish')
    engine.setProperty('rate', rate-100)
    freq = {}
    freq_pickle = "./freq.pickle"
    palabra_actual = ""
    letra = [
             ["a", "b", "c", "d"],
             ["e", "f", "g", "h"],
             ["i", "j", "k", "l"],
             ["m", "n", "o", "p"],
             ["q", "r", "s", "t"],
             ["u", "v", "y", "z"]
            ]


    def anadir_palabra(self, palabra):
        if palabra in self.freq:
            self.freq[palabra] += 1
        else:
            self.freq[palabra] = 1

    def palabra_a_prefijo(self, palabra):
        lst = []
        for i in range(len(palabra)-1):
            lst.append(palabra[:i+1])
        lst.append(palabra)
        t = '/'.join(lst)
        return t

    def cargar_por_lista(self, palabras):
        diccionario = pygtrie.StringTrie()
        for palabra in palabras:
            t = self.palabra_a_prefijo(palabra)
            diccionario[t] = palabra
        return diccionario

    def cargar_diccionario(self, archivo):
        fp = open(archivo, "r")
        palabras = fp.read().splitlines()
        fp.close()
        return self.cargar_por_lista(palabras)

    def palabras_mas_usadas(self, n=200):
        return sorted(self.freq, key=self.freq.get, reverse=True)

    def predecir_palabra(self, dic):
        candidate = []
        try:
            for i in range(len(self.palabra_actual)):
                t = self.palabra_a_prefijo(self.palabra_actual)
                candidate = list(dic.items(prefix=t));
            return list(map(lambda x: x[1], candidate))
        except KeyError:
            return False
    def escuchar_palabra(self, palabra):
        self.anadir_palabra(palabra)
        self.engine = pyttsx3.init()

        self.engine.say(palabra)
        self.engine.runAndWait()
    def guardar(self):
        f = open(self.freq_pickle, "wb")
        p = pickle.Pickler(f)
        p.dump(self.freq)
        f.close()
    def cargar(self):
        f = open(self.freq_pickle, "rb")
        u = pickle.Unpickler(f)
        self.freq = u.load()
        f.close()
    def resetear(self):
        self.freq = {}
    def gesto_a_letra(self, gesto , estado):
        self.palabra_actual += self.letra[estado][gesto]
        return self.letra[estado][gesto]
    def get_palabra_actual(self):
        return self.palabra_actual
    def clear_palabra_actual(self):
        self.palabra_actual = ""

if __name__ == "__main__":
    main = Principal()
    #dic = main.cargar_diccionario("palabras_faciles.txt")
    #main.gesto_a_letra(0, 0)
    # print(main.get_palabra_actual())
    #print(main.predecir_palabra(dic))
    engine = pyttsx3.init()
    rate = engine.getProperty('rate')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', 'spanish')
    engine.setProperty('rate', rate-100)
    engine.say("hola")
    engine.runAndWait()
    engine.say("hola")
    engine.runAndWait()
    # print(main.palabras_mas_usadas(dic))
    # main.cargar()
    # main.escuchar_palabra()
    # main.guardar()
    # print(main.freq)
    # Base 0, libre 1
    # estado = 0
    # if estado == 0:
    #     entrada = ""
    #     while False == predecir_palabra(dic, entrada):
    #         pass
    #     audio
    # elif estado == 1:
