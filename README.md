# WebSiteScanner
Scanner di siti web alla ricerca di un determinato pattern.
-----------------------------------------------------------

Scansione sito web basandosi sulla prima parte dell' url che verrà concatenato ad un pezzo finale di una lunghezza specificata dall' utente, al fine di trovare una pagina funzionante nella quale cercare un determinato elemento basandoci su un pattern.
La stringa generata ha un suo alfabeto che l'utente deve specificare ed esse consiste nell'insieme di tutti i caratteri che può assumere.
E' inoltre possibile settare la stringa di partenza, nel caso in cui non venga specificata verrà settata randomicamente
Infine è possibile impostare il tempo tra una chiamata e l'altra al sito web per evitare di essere bloccati, non e' necessario in molti siti, 
infatti di default e' nullo.

-----------------------------------------------------------
E' infine possibile chiamare ogni scansione facendola partire su un thread a parte, cosi da poter fare più scansioni contemporanemanete.

