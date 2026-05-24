# M5Stick Weather Station

A real-time weather dashboard for **M5StickC Plus** with ENV III sensor unit.

Una dashboard meteo in tempo reale per **M5StickC Plus** con unità sensore ENV III.

## Features / Funzionalità

- Live temperature, humidity and barometric pressure
- Calcolo del punto di rugiada e dell'indice di calore (sensazione termica)
- Pressure trend indicator (^ = v)
- Monitoraggio dei valori massimi per tutti i sensori
- Battery level monitor and session uptime
- Modalità risparmio: schermo acceso/spento

## Hardware / Hardware

| Component / Componente | Details / Dettagli                 |
|------------------------|------------------------------------|
| Board / Scheda         | M5StickC Plus                      |
| Sensor / Sensore       | ENV III Unit (SHT30 + BMP280)      |
| Connection / Connessione | Grove port — SDA=32, SCL=33      |
| Firmware               | UIFlow 2 / MicroPython             |

## Pages / Pagine

| Page / Pagina | Content / Contenuto | |
|---------------|---------------------|--|
| 0 | Live data — temperature, dew point, feels like, humidity, pressure | default |
| 0 | Dati in tempo reale — temperatura, punto di rugiada, sensazione termica, umidità, pressione | default |
| 1 | Max records — peak values since last reset | |
| 1 | Valori massimi — picchi registrati dall'ultimo reset | |
| 2 | System info — battery percentage, uptime, sampling interval | |
| 2 | Info di sistema — livello batteria, uptime, intervallo di campionamento | |

## Controls / Controlli

| Button / Pulsante | Action / Azione |
|-------------------|-----------------|
| BtnA (click)      | Cycle to next page / Cambia pagina |
| BtnA (hold)       | Toggle screen on/off / Accende/spegne lo schermo |
| BtnB (hold)       | Reset all max records / Reimposta i valori massimi |

## Installation / Installazione

1. Clone or download this repository
1. Clona o scarica questo repository
2. Open the project folder in VS Code with the M5Stack extension
2. Apri la cartella del progetto in VS Code con l'estensione M5Stack
3. Connect your M5StickC Plus via USB
3. Collega il tuo M5StickC Plus via USB
4. Flash `main.py` to the device
4. Flash `main.py` sul dispositivo

## License / Licenza

MIT — see [LICENSE](LICENSE)
MIT — vedi [LICENSE](LICENSE)
