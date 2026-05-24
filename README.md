# StickPlus2 Termometro

Programma MicroPython per M5Stack Stick Plus 2 che legge un sensore ambientale (unità `ENVUnit`) via I2C e mostra temperatura, umidità, pressione e valori derivati su schermo.

**Caratteristiche**
- Pagina LIVE: temperatura, dew point, "feels like", umidità, pressione e trend di pressione.
- Pagina RECORDS: massimi registrati per temperatura, umidità e pressione.
- Pagina SYSTEM: percentuale batteria, uptime e intervallo di acquisizione.
- Toggle schermo (hold su A), cambio pagina (click su A), reset record (hold su B).

File principale
- `StickSPlus2_Termometro.py` — script principale incluso in questo repository.

Requisiti
- Firmware MicroPython compatibile con M5Stack Stick Plus 2.
- Moduli Python per M5: `M5`, `hardware` (Pin, I2C), `unit` (ENVUnit), e `Widgets` forniti dall'ambiente M5.

Connessioni hardware
- I2C: SCL -> GPIO33, SDA -> GPIO32 (configurati nello script).
- Sensore: unità `ENVUnit` tipo 3 collegata all'I2C.

Configurazione
- `SAMPLING_INTERVAL` (millisecondi) definisce l'intervallo di lettura dei sensori. Modificare il valore in `StickSPlus2_Termometro.py` se necessario.

Installazione e deploy
1. Caricare il firmware MicroPython per M5Stack Stick Plus 2.
2. Copiare `StickSPlus2_Termometro.py` nella memoria del dispositivo (es. come `main.py` o eseguirlo via REPL).
3. Collegare il sensore ENVUnit ai pin I2C indicati e riavviare il dispositivo.

Uso
- Bottone A: click per cambiare pagina; hold per spegnere/accendere lo schermo.
- Bottone B: hold per resettare i record massimi (emette un breve segnale acustico).

Dettagli implementativi
- Il file usa `ENVUnit` per ottenere temperatura (`read_temperature()`), umidità (`read_humidity()`) e pressione (`read_pressure()`).
- Calcoli inclusi: indice di calore (heat index) e punto di rugiada (dew point).

Note
- Lo script gestisce casi di pressione con valore raw alto normalizzando il valore in hPa.
- In caso di eccezioni durante la lettura dei sensori lo script ignora l'errore (bloc try/except generale).

Contatti
- Autore: (inserisci il tuo nome o contatto qui)

Se desideri, posso aggiornare il README con dettagli aggiuntivi (esempio di installazione del firmware, immagini, o istruzioni di debug).
