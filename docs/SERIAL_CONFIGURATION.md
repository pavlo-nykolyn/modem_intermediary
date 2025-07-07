# Formato del file contenente la configurazione della porta seriale

il file è strutturato secondo lo standard YAML. Allo stato attuale, è necessaria la definizione
di un singolo documento che contiene la chiave **port**. Il valore associato a quest'ultima è,
a sua volta, una mappa la cui unica chiave obbligatoria è **name**, ovvero il nome della porta
seriale. La chiave **configuration**, invece, è opzionale. Specifica una serie di coppie
chiave-valore che descrivono un determinato parametro della porta. Quelli supportati sono:

| chiave | valore |
| --- | --- |
| baud-rate | {50, 75, 110, 134, 150, 200, 300, 600, 1200, 1800, 2400, 4800, 9600, 14400, 19200, 38400, 57600, 115200} |
| parity | {none, even, odd, mark, space} |
| data-bits | {5, 6, 7, 8} |
| stop-bits | {1, 2} |

l'assenza della chiave configuration comporta l'utilizzo di un baud rate pari a 9600 e di un framing seriale 8N1
