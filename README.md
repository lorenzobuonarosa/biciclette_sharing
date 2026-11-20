# Sharing di bici e monopattini – dataviz Radar QN

Quattro dataviz per il pezzo di Radar – QN sulla sharing mobility in Italia. Pagine HTML statiche (D3 v7, stile Radar) da pubblicare su GitHub Pages dalla root di `main` e incorporare nel CMS con un iframe.

Indirizzo base previsto: `https://lorenzobuonarosa.github.io/biciclette_sharing/`. `index.html` mostra le anteprime desktop/mobile e lo snippet da copiare per ogni dataviz.

| Cartella | Dataviz | CSV | Altezza iniziale iframe |
|---|---|---|---|
| `monopattini/` | Più corse in monopattino, con meno mezzi e meno servizi (linee, numero indice 2022 = 100) | `data/monopattini.csv` | 750 |
| `capoluoghi/` | Il monopattino in sharing nei capoluoghi (mappa a punti con slider 2020–2024, vista Monopattini/Bici) | `data/capoluoghi.csv`, `data/regioni.json` | 1075 |
| `capitali/` | I capitali per la micromobilità sono quasi spariti (barre impilate) | `data/capitali.csv` | 725 |
| `rotazione/` | Corse al giorno per mezzo in sharing, 2024 (barre orizzontali) | `data/rotazione.csv` | 595 |

Per aggiornare un grafico basta cambiare il CSV: titoli calcolati, big number, contatori e frasi che dipendono dai dati si ricalcolano.

## Fonti e trasformazioni dei dati

### `data/monopattini.csv`
Osservatorio nazionale sharing mobility, 9° Rapporto nazionale sulla sharing mobility (ottobre 2025). Valori come forniti dalla redazione. Unica modifica: i campi `nota` del 2022 e del 2025 contengono un `;` e sono stati messi tra virgolette per non spezzare la riga.
- Il grafico parte dal 2022 (anno record dell'offerta, base dell'indice); 2020 e 2021 servono solo per la variazione sull'anno precedente nel tooltip del 2022.
- Numero indice = valore / valore 2022 × 100, calcolato nella pagina.
- Big number: noleggi 2025 / noleggi 2022 − 1 (+27%); didascalia: flotta 2025 (primo quadrimestre) / flotta 2022 − 1 (−20%).
- 2025: noleggi = stima annua dell'Osservatorio sul primo quadrimestre; flotta e servizi = dato del primo quadrimestre. Segnato con tratto tratteggiato e punto vuoto.
- 2022, noleggi: valore letto dal grafico del Rapporto, approssimato.

### `data/capoluoghi.csv`
Istat, Dati ambientali nelle città – tavole "Mobilità urbana". Colonne: `capoluogo;regione;lat;lon;anno;monopattini;bici;monopattini_10k;bici_10k`.
- **Periodo 2020–2024.** La tavola dell'edizione Anno 2024 copre solo 2022–2024, quindi le serie sono state unite con le edizioni precedenti, usando per ogni anno l'edizione più recente che lo contiene:
  - 2022, 2023, 2024: `MOBILITA_URBANA_2024.xlsx` (Ambiente urbano – Anno 2024), tavole 16.2, 17.1, 18.2, 19.1;
  - 2021: `MOBILITA_URBANA_2023.xlsx` (Ambiente urbano – Anno 2023), stesse tavole;
  - 2020: `MOBILITA_2021.xlsx` (Ambiente urbano – Anno 2021), tavole 18.2 e 19.1.
- `monopattini` = presenza (1/0) di servizi di **micromobilità elettrica** in sharing (Istat: monopattini o altri veicoli del D.M. 229/2019; in pratica monopattini). `monopattini_10k` = veicoli per 10.000 abitanti.
- `bici` = presenza (1/0) di bike sharing, **totale** a postazione fissa e a flusso libero; `bici_10k` = biciclette per 10.000 abitanti, totale.
- Celle Istat: `X` → 1, `-` → 0 (per i valori per 10.000 abitanti `-` → 0,0). Le note di rimando ai dati stimati da Istat (es. "Torino (e)") sono state tolte dal nome; i valori stimati sono usati come pubblicati. "Bolzano - Bozen" (edizione 2021) uniformato a "Bolzano/Bozen".
- **Cesena escluso**: le tavole riportano Forlì e Cesena separatamente, ma i totali Istat (109 capoluoghi) non includono Cesena; la mappa segue i totali Istat. Con questa scelta i conteggi coincidono con quelli delle tavole: monopattini 22, 42, 45, 42, 40 capoluoghi (2020–2024); bike sharing 55, 60, 64, 64, 65.
- Coordinate: centroidi dei poligoni comunali Istat (confini generalizzati al 1° gennaio 2024, `Com01012024_g`, filtro `CC_UTS = 1`), riproiettati in WGS84, 4 decimali. File intermedio in `scripts/centroidi-capoluoghi.csv`.
- Base: confini regionali Istat generalizzati al 1° gennaio 2024 (`Reg01012024_g`), WGS84, semplificati al 4% con mapshaper, isole sotto i 30 km² tolte, TopoJSON in `data/regioni.json`. Proiezione nella pagina: conica conforme (paralleli 38° e 46°, meridiano centrale 12,5° E).
- Stato di un capoluogo in un anno: *attivo* se il servizio c'è quell'anno; *chiuso* (anello rosso) se c'era in almeno un anno precedente dal 2020 e quell'anno non c'è; *mai attivo* altrimenti.
- Lo script `scripts/capoluoghi.py` rifà `data/capoluoghi.csv` dalle tavole Istat.

### `data/capitali.csv`
Via ID-Dealroom, State of European Mobility Startups 2025, in Osservatorio nazionale sharing mobility, 9° Rapporto. Valori letti dal grafico del Rapporto (senza tabella), approssimati al decimo. Big number: micromobilità 2024 / picco (2021) − 1 = −87%.

### `data/rotazione.csv`
Italia: tassi di rotazione pubblicati dall'Osservatorio (9° Rapporto, p65 e p72). Parigi, Barcellona, Madrid: elaborazione Radar – QN, noleggi annui / flotta / 366 giorni (Agemob; BSM e AMB; Ayuntamiento de Madrid). Berlino e le bici italiane a flusso libero, presenti nella prima versione, sono stati tolti. Il campo `fonte` di Barcellona contiene un `;` ed è tra virgolette.

## Snippet per il CMS

Ogni snippet è l'iframe seguito dallo script di `assets/embed.min.js` (altezza automatica e tema del sito). Lo script si può lasciare in ogni snippet: se in una pagina ci sono più dataviz non si ripete (controllo `__radarQNv2`). Lo script va sempre incollato inline, mai richiamato da un file esterno.

```html
<iframe src="https://lorenzobuonarosa.github.io/biciclette_sharing/monopattini/" width="100%" height="750" frameborder="0" scrolling="no" title="Più corse in monopattino, con meno mezzi e meno servizi"></iframe>
<script>/* contenuto di assets/embed.min.js */</script>
```

Anteprime senza CMS: `?bg=grigio|bianco|nero|notte` forza lo sfondo, `?theme=dark` il tema.
