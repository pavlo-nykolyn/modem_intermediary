# REST API

la REST API esposta, per il momento, è molto semplice. Non sono previsti meccanismi di autenticazione quindi,
se si desidera utilizzarla, è preferibile farlo in un'infrastruttura isolata oppure, in cui la comunicazione
via TCP/IP è opportunamente mediata da un firewall. Inoltre, l'accesso all' host che espone l'API dovrebbe
essere limitato ai soli client che ne fanno uso (quando l'host non è sottoposto a sessioni di manutenzione);

la root degli end-point è **/modem**. Allo stato attuale, una singola chiamata è resa disponibile:

- /modem/retrieve\_all\_sms

tale chiamata è l'equivalente di:

> python3 modem\_communication.py modules/requirements.txt read-all-sms --read-timeout 2000

non è possibile impostare nè l'intervallo inter-byte nè il time-out di lettura. Il primo non viene
utilizzato mentre, il secondo è cablato su 2000 millisecondi. Le impostazioni della porta seriale
vengono prelevate dal file .yaml contenuto nella directory _configuration_

in caso di errori durante l'elaborazione dell'operazione, il server restituirà il codice 500 unito
ad una stringa che indicherà la motivazione dell'errore;

in caso di successo, il valore restituito sarà un oggetto JSON contenente i seguenti campi:

(il numero di slot è da considerare come numero di SM)

- _filled-slots_ : il numero di slot del dispositivo di archiviazione attualmente in uso. Se il valore è 0, il client non DEVE analizzare gli altri campi dell'oggetto;
- _maximum-slots_ : il numero massimo di slot supportato dal dispositivo di archiviazione del transmission equipment;
- _responses_ : un vettore JSON i cui elementi sono degli oggetti JSON. Ciascuno di essi contiene informazioni relative ad un SM memorizzato. Si veda la sezione [Risposta](../README.md) per maggiori informazioni sul formato dell'oggetto;

gli elementi del vettore identificato da _responses_ sono ordinati in ordine crescente rispetto al campo **Service-center-timestamp**

il deploy dell'API è reso possibile con la creazione di un'immagine Docker tramite il Dockerfile integrato nel repository. Il server
utilizzato è uwsgi.

## Container Docker

Dato che il programma doveva essere esposto su una raspberry, ho optato per una configurazione che si basa su variabili d'ambiente.
Solitamente, uso un here-doc per generare un file di configurazione con dei parametri definiti durante il build. Le versioni
Docker basate su arm potrebbero non supportare la sintassi here-doc in un Dockerfile.

le variabili che possono essere configurate solo durante il build dell'immagine sono:

- image\_version : specifica la versione dell'immagine base di python;
- image\_type : se impostata su use\_slim, verrà utilizzata un'immagine con un footprint di memoria più leggero;

le seguenti variabili, invece, possono essere configurate anche durante l'inizializzazione di un container:

- MODEM\_API\_LISTENING\_PORT : porta esposta dal container;
- MODEM\_API\_WSGI\_FILE: file che contiene le definizioni delle chiamate REST. Allo stato attuale è **modem_communication_api.py**;
- MODEM\_API\_APPLICATION\_INSTANCE: nome dell'istanza di Flask utilizzata per definire le chiamate REST. Attualmente deve essere impostato **modem_intermediary**;
- MODEM\_API\_NUM\_THREADS: numero di thread resi disponibili da uwsgi (il valore di default è pari a uno);
- MODEM\_API\_NUM\_PROCESSES: numero di processi resi disponibili da uwsgi (il valore di default è pari a uno);

### Esempi di utilizzo del Dockerfile

(utilizzo BuildKit per generare l'immagine. Non è detto che sulle raspberry sia supportato. Se non lo è, l'invocazione di un docker build è sufficiente per generare l'immagine)

```bash
docker buildx build --file Dockerfile --build-arg 'MODEM_API_LISTENING_PORT=9500' --build-arg 'MODEM_API_WSGI_FILE=modem_communication_api.py' --build-arg 'MODEM_API_APPLICATION_INSTANCE=modem_intermediary' --output 'type=image,name=modem_intermediary,push=false' .
```

avvio del container (per l'opzione _--publish_ è fortemente consigliata l'aggiunta dell'indirizzo IPv4 dell'interfaccia sulla quale sarà possibile contattare il servizio)

```bash
docker run --detach --name 'modem_intermediary' --publish '9500:9500' modem_intermediary
```
