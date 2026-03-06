# 🌌 AstroCategorizer

Una moderna applicazione desktop in Python pensata per gli astronomi amatoriali e gli astrofotografi, utile ad organizzare, categorizzare ed archiviare le loro catture del profondo cielo e planetarie.

![AstroCategorizer Logo](logo.png)

## ✨ Funzionalità

- **Visualizzazione Tabellare Ordinabile**: Visualizza tutte le tue immagini in una griglia strutturata. Ordina le tue catture per Titolo, Tipologia, AR, Dec, o Tempo di Integrazione con un semplice click.
- **Titoli Personalizzati**: Non sei più vincolato al nome grezzo dei file (es. `IMG_001.jpg`). Assegna veri titoli astronomici (es. `Nebulosa di Orione (M42)`) mentre l'app tiene traccia automaticamente del file originale sul tuo disco.
- **Diario Astrofotografico**: Salva metadati avanzati, incluse l'Ascensione Retta (AR), la Declinazione (Dec), la Costellazione, la Strumentazione utilizzata, il Tempo di Integrazione e il Luogo di Acquisizione (es. scala di Bortle). Sono supportate anche comode note di descrizione multiriga.
- **Doppia Mappa Stellare Integrata**:
  - **Mappa IAU (Wikipedia)**: Fornendo la costellazione, l'app scarica direttamente da Wikimedia Commons la meravigliosa mappa stellare ufficiale della International Astronomical Union.
  - **Mappa DSS2**: Una volta inserite le coordinate di AR e Dec, l'applicazione può scaricare in background (tramite le API di Strasbourg CDS) una vera immagine fotografica di quella porzione di cielo (DSS2 color survey) perfettamente centrata sul tuo obiettivo.
- **Menu Laterale Overlay Elegante**: Un moderno pannello semitrasparente fluttuante riassumerà tutti ti dati di scatto e le descrizioni scomparendo fluidamente per non comprimere la lista d'immagini principale. Dispone di un comodissimo TEMA SCURO, pensato specialmente per l'uso notturno.
- **Categorizzazione Focale Automatica**: Inserisci la lunghezza focale in mm, e l'app le assegnerà automaticamente la categoria più opportuna (Wide Field, Deep Sky, o Ultra Deep Sky).
- **Modifica Massiva**: Seleziona simultaneamente più righe della tabella per applicare la medesima strumentazione, il luogo o la vocale a molteplici scatti con un click.

## 📦 Installazione

1. Clona questa repository sul tuo computer locale.
2. Installa le dipendenze richieste aprendo il terminale ed eseguendo: 
   ```bash
   pip install -r requirements.txt