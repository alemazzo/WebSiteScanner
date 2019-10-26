import re, time, threading, requests, os, string
from SiteScanner.StringGenerator import StringGenerator

class SiteScanner:
    """
    Scansione sito web basandosi sulla prima parte dell' url
    [base_url] che verrà concatenato ad un pezzo finale di una 
    lunghezza[str_length] nella speranza di trovare una pagina
    funzionante nella quale cercare un determinato elemento
    [pattern]
    la stringa ha un suo alfabeto[alphabeth], ovvero l'insieme di
    tutti i caratteri che può assumere.
    [str_start] e' la stringa di partenza, se non specificata sara'
    poi settata randomicamente
    [delay] è il tempo tra una chiamata e l'altra al sito web per
    evitare di essere bloccati, non e' necessario in molti siti e
    infatti di default e' nullo
    [name] e' il nome del sito che andiamo a scansionare, sul quale si
    baserà il file di output che si chiamera' '[name].html'
    [rand] la stringa viene generata random ogni volta
    """
    def __init__(self, base_url, pattern, name, str_length = 4, str_start = None, alphabeth = None, delay = None, before = '', after='', rand = False, log = False):
        self.base_url = base_url
        self.pattern = pattern
        self.name = name
        self.delay = delay
        self.contents = list() #lista di contenuti gia salvati 
        self.output = None #connessione al file di output
        self.end = False
        self.log = log #Se True stampa il new_end che sta provando


        """
        Da stampare prima e dopo l'elemento trovato nella risposta
        che viene stampato nel file html
        """
        self.before = before
        self.after = after

        """
        Generatore di stringhe
        """
        self.generator = StringGenerator(
            length = str_length, 
            alphabeth = alphabeth, 
            start = str_start,
            rand = rand
            )
    
    def Terminate(self):
        self.end = True

    def _extract_results(self, response):
        """
        Analizza la risposta dell'url chiamato
        Cerca il pattern e nel caso trovi uno o
        piu' risultati li ritorna.
        """
        res = re.compile(self.pattern, re.DOTALL).findall(response)
        results = list()
        for r in res:
            results.append(r)
        return results
    
    def _get_response(self, new_end):
        """
        Effettua la chiamata al sito web, concatenando
        l'url base con la stringa passatagli come
        parametro [new_end]
        Infinde da questa risposta estrae solamente il testo
        e lo inserisce nella variabile self.response
        """
        res = requests.get(self.base_url + new_end)
        if self.log:
            print(res.status_code)
        if res.status_code != 404:
            return res.text
        else:
            return None

    def _save_result(self, result):
        """
        Salva il risultato accodandolo ai precendenti
        Il tutto va dentro un div con una separazione
        dal precedente.
        Inoltre aggiunge il contenuto di [self.before]
        prima del testo trovato e [self.after] dopo, cosi 
        da permetter una personalizzazione della visualizzazione
        del contenuto una volta scoperto cosa ritorna il contenuto.
        """
        self.output.write('<div id="mydiv" style="width: 700px; height:700px; margin-bottom: 50px; margin-left: 30px; margin-right: 30px; border-style: solid">')
        try:
            self.output.write(self.before)
            self.output.write(result)
            self.output.write(self.after)
        except:
            pass
        self.output.write('</div>')

    def _open_file(self):
        #Crea il file .html se non è presente e lo apre
        output_dir = 'output/'
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)
        self.output = open(output_dir + self.name + '.html', 'w+')
        #Stile del file
        self.output.write('<style>#mydiv img {max-width: 100%; max-height: 100%;}</style>')

    def _close_file(self):
        self.output.close()

    def StartScan(self, thread = False):
        """
        Fa partire la scansione del sito web in base
        ai parametri specificati.
        Nel caso in cui la variabile [thread] sia True allora
        fa partire la scansione su un Thread a parte quindi la 
        funzione ritorna subito ed è possibile eseguire altri
        comandi o fare partire altre scansioni contemporaneamente.
        """
        if thread == True:
            t = threading.Thread(target = self._scan_forever)
            t.start()
        else:
            self._scan_forever()

    def _scan_forever(self):
        """
        Crea il file .html
        Inizia il loop che termina solo quando l'utente
        preme ctrl+c se non siamo in multithreading.
        Altrimenti terminera' solo quando il programma verrà killato oppure
        se si verra' chiamata anche la funzione SiteScanner.handle_termination(args)
        terminera' sempre con il ctrl+c dell'utente.
        Partendo dalla stringa base effettua la chiamata al server,
        poi elabora la risposta e nel caso di risultati
        li scrive sul file.
        Il tutto tenendo memoria dei contenuti cosi da non avere 
        doppioni.
        Nel caso il parametro [delay] sia stato specificato
        tra un ciclo e l'altro verrà aspettato del tempo.
        Alla fine dell'esecuzione verra' stampato il numero di risultati
        che sono stati trovati.
        """
        try:
            self._open_file()
            while True:
                try:
                    new_end = self.generator.get()
                    if self.log:
                        print(f'Trying {new_end}')
                    response = self._get_response(new_end)
                    if response:
                        results = self._extract_results(response)
                        for result in results:
                            if(result not in self.contents):
                                self.contents.append(result)
                                self._save_result(result)
                                print(f'{self.name} - {len(self.contents)} trovati - link = {new_end}')
                    if(self.delay):
                        time.sleep(self.delay)
                    if(self.end):
                        raise KeyboardInterrupt()
                except KeyboardInterrupt:
                    self._close_file()
                    break
                except:
                    pass
        except KeyboardInterrupt:
            self.output.close()
        """
        Aspetto un po di tempo prima di stampare 
        i risultati per dare tempo agli altri thread di finire
        """
        time.sleep(5)
        print(f'{self.name} - {len(self.contents)} risultati')

    @staticmethod
    def handle_termination(threads):
        """
        Funzione da usare nel caso di multithreading
        dello Site Scanner.
        Rimane nel loop fino a che non viene premuto ctrl-c,
        in quel momento andra' a settare la variabile [end] dei
        vari thread a True in modo da fare terminare i thread
        al prossimo controllo della variabile
        """
        while True:
            try:
                time.sleep(.1)
            except KeyboardInterrupt:
                for thread in threads:
                    thread.Terminate()
                print('\n\n Terminating threads\n\n')
                return

"""
Configurazione di scansioni a siti web gia configurate.
Sara' comunque possibile modificarne i parametri settando
i membri della classe una volta instanziata
"""
websites = {
    'ibb' : SiteScanner(
        base_url = 'https://ibb.co/',
        pattern = '<div id="image-viewer-container" class="image-viewer-main image-viewer-container">(.*?)</div>',
        name = 'ibb',
        str_length = 3,
        rand = True,
        alphabeth = string.ascii_letters + string.digits,
        #log = True
        ),
    'justpaste' : SiteScanner(
        base_url = 'https://justpaste.it/', 
        pattern = '<div id="articleContent"(.*?)</div>',
        name = 'justpaste',
        str_length = 4,
        rand = True,
        alphabeth = string.ascii_letters + string.digits,
        delay = 0.2
        ),
    'heypasteit' : SiteScanner(
        base_url = 'https://www.heypasteit.com/clip/',
        pattern = '<td colspan="2">(.*?)</td>',
        name = 'heypasteit',
        str_length = 3,
        alphabeth = string.ascii_uppercase + string.digits
        ),
    
    'instagram' : SiteScanner(
        name = 'instagram',
        base_url = 'https://www.instagram.com/p/',
        pattern = '<meta property="og:image" content="(.*?)" />',
        str_length = 5,
        rand = True,
        alphabeth = string.ascii_letters + string.digits,
        before = '<img src="',
        after = '">',
        #log = True
        ),
    
    'facebook' : SiteScanner(
        
        name = 'facebook',
        base_url = 'https://www.facebook.com/photo.php?fbid=',
        pattern = 'data-ploi="(.*?)" href',
        str_length = 17,
        #rand = True,
        str_start = '10102210419817761', #immagine che sono sicuro esista
        alphabeth = string.digits,
        before = '<img src="',
        after = '">',
        #log = True
        ),
}