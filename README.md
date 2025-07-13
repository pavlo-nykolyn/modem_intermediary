# modem_intermediary

questo programma interroga un modem che supporta i comandi AT definiti dallo standard 3GPP 27.007;
lo scambio di dati, mediato da una porta seriale, viene gesito mediante una politica di polling. In particolare,
l'utente è in grado di configurare il time-out totale durante il quale il programma resta in attesa della
ricezione di almeno un byte oppure del sopraggiungere di un evento particolare che comporta il fallimento
del tentativo di lettura.
L'utente è in grado di configurare:

- il nome della porta seriale (sui sistemi UNIX, è necessaria la path assoluta al device);
- il baud rate;
- il framing (la lunghezza del frame e la semantica del bit di parità);

la configurazione è gestita tramite un file .yaml;

si rimanda al seguente documento per informazioni aggiuntive sui valori da assegnare ai diversi parametri:

[Configurazione seriale](docs/SERIAL_CONFIGURATION.md)

## Requisiti

al fine di utilizzare il programma, sono necessari i seguenti package:

- pyserial
- pyyaml

in **modules** è disponibile il file requirements.txt che può essere utilizzato con pip per scaricare i
package aggiuntivi:

```bash
pip install --requirement modules/requirements.txt
```

## Sinossi

per ottenere una sinossi da riga di comando, è sufficiente invocare:

> python3 modem_communication.py --help

> python3 modem_communication.py \<file-path\> \<behaviour\> \[--command \<command\>\] \[--message-index \<index\>\] \[--read-timeout \<read-timeout\>\] \[--inter-byte-timeout \<inter-byte-timeout\>\]

| parametro | descrizione |
| --- | --- |
| \<file-path\> | path (può essere assoluta oppure relativa) del file di configurazione di una porta seriale |
| \<behaviour\> | la dinamica del programma : read-all-sms tenta la lettura di tutti gli SM archiviati nell'unità di memoria del dispositivo mentre, command indica l'invio di un comando |
| --command | specifica il singolo comando da inviare al modem |
| --message-index | indica l'indice, rispetto all'unità di memoria, di un SM (tale opzione è utilizzata per selezionare il messaggio da leggere o eliminare quando \<behaviour\> è impostato su command) |
| --read-timeout | time-out di lettura totale (valido per una singola operazione di lettura) |
| --inter-byte-timeout | time-out massimo che può intercorrere tra la ricezione di due byte consecutivi |

[!IMPORTANT]
> i time-out sono espressi in millisecondi

### Risposta

nel caso in cui venga richiesta la lettura degli SM memorizzati, verranno stampati a video
tante mappe (opportunamente formattate) quanti sono gli SM letti.
Le chiavi definite in ciascuna mappa sono:

- **SMS-sender** : l'entità (solitamente un service center) che ha eseguito il dispacciamento del messaggio;
- **SMS-status** : lo stato dell'SM (rispetto al transmission equipment). Può assumere quattro valori:

  * read : ricevuto e letto;
  * not_read : ricevuto ma non ancora letto;
  * not_dispatched : memorizzato ma non ancora inviato;
  * dispatched : memorizzato e inviato;

- **Service-center-timestamp** : istante temporale del service center che ha eseguito l'invio del messaggio;
- **SMS** : corpo del messaggio;

il formato della stringa identificata da **Service-center-timestamp** è _yy/MM/dd,hh:mm:ss±zz_

- yy indica l'anno dell'istante riferito al secolo corrente (\[0, 99\]);
- MM indica il mese dell'istante (\[1, 12\]);
- dd indica il giorno mensile dell'istante (\[1, 31\]);
- hh indica l'ora dell'istante (\[0, 23\]);
- mm indica i minuti dell'istante (\[0, 59\]);
- ss indica i secondi dell'istante (\[0, 59\]);
- zz indica il numero di quarti d'ora che separano l'istante locale da quello UTC;

le mappe stampate sono ordinate rispetto al valore dell'istante temporale (ordine crescente). Nell'elaborare il valore,
ho preferito omettere l'indicazione del time zone dai confronti necessari per l'ordinamento in quanto, ho ipotizzato
che i service center siano dislocati in Italia. Mi rendo conto che si tratta di un'ipotesi conservativa ma, è sufficiente
per le mie esigenze attuali. Detto ciò, ho provveduto a definire l'interfaccia della funzione create\_instance\_scts\_aware
(la si può trovare nel modulo ts\_instance) per un'eventuale estensione futura;

[!WARNING]
> è possibile che il numero di messaggi stampati sia superiore a quello estratto dalla risposta del comando +CPMS?. In tal caso\
  sono stati ricevuti dei messaggi dopo l'invio del comando stesso. Dato che read-all-sms presuppone l'interrogazione di tutti\
  gli slot resi disponibili dal dispositivo di archiviazione configurato, tale comportamento è inevitabile

per altri comandi, la mappa, allo stato attuale, contiene una singola chiave *data* che definisce una sequenza
di elementi. La loro natura dipende dal comando inviato;

per i comandi di scrittura, allo stato attuale, non è stata implementata una risposta;

### Comandi singoli

| comando | descrizione |
| --- | --- |
| read-SMS | esegue la lettura di un SM (il parametro --message-index è obbligatorio) |
| delete-SMS | esegue l'eliminazione di un SM (il parametro --message-index è obbligatorio) |
| delete-all-SMS | simile a delete-SMS ma agisce su tutti gli slot di memoria |
| get-maximum-record-index | ottiene lo stato dell'unità di memoria configurata (il numero di slot utilizzati e il rispettivo valore massimo); l'ultima tupla di dati fa riferimeno all'unità utilizzata durante la lettura |
| show-text-mode-parameters | abilita la visualizzazione di informazioni di diagnostica aggiuntiva per ogni SM ricevuto |
| inhibit-text-mode-parameters | il complementare di show-text-mode-parameters |
| disable-echo | disabilita l'eco dei comandi del modem (questa è l'impostazione rispetto alla quale è stato implementato il meccanismo di ricezione) |
| enable-echo | il complementare di disable-echo |
| attention | causa l'invio di un ATtention |

### Esempi

lettura di tutti gli SM

```bash
python3 modem_communication.py modules/requirements.txt read-all-sms --read-timeout 2000
```

### Note di sviluppo

- la classe Stream_configurator può essere ereditata e i metodi retrieve e parse possono essere ridefiniti per supportare una nuova sorgente di dati di configurazione;
- la classe AbstractEntity definisce una categoria di eccezioni associate a istruzioni la cui implementazione è assente
