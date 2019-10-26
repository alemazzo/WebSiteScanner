import string, random

class StringGenerator:
    """
    Generatore di stringhe di una lunghezza specificata[length]
    la stringa viene incrementato basandosi su un alfabeto
    [alphabeth] ad ogni chiamata della funzione get
    la stringa di partenza [start] viene creata in modo randomico
    se non viene passato il parametro
    [rand] la stringa viene generata random ogni chiamata di get()
    """
    def __init__(self, length, alphabeth, start = None, rand = False, max_length = 20):
        self.length = length
        self.alphabeth = alphabeth
        self.indici = list()
        self.stringa = ''
        self.rand = rand
        self.max_length = max_length
        if start:
            for letter in start:
                self.indici.append(self.alphabeth.index(letter))
        else:
            for _ in range(self.length):
                self.indici.append(random.randint(0,len(self.alphabeth)))

    def get(self):
        if not self.rand:
            self.stringa = ''
            for i in range(self.length):
                self.stringa += self.alphabeth[self.indici[i]]
            self.indici[self.length - 1] += 1
            self._check(self.length - 1)
            return self.stringa
        else:
            return ''.join(random.choice(self.alphabeth) for i in range(self.length))
    
    def _check(self, index):
        #Controllo raggiungimento limite alfabeto e aggiornamento
        #della stringa incrementando la lettera precedente
        #Attenzione: No controllo del ragimento limite della prima lettera da sinistra
        if self.indici[index] == len(self.alphabeth):
            self.indici[index] = 0
            self.indici[index - 1] += 1
            self._check(index - 1)
