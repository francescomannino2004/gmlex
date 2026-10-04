# gmlex

Sito web dello Studio Legale Mannino (Avv. Manlio Mannino – Palermo e Roma).
Pubblicato con GitHub Pages: https://francescomannino2004.github.io/gmlex/

Sito statico in italiano, inglese e francese, senza dipendenze esterne e senza cookie propri.

## Come modificare i contenuti

Tutti i testi (italiano, inglese e francese), le aree di attività, le sedi e la rassegna stampa
sono in `_build/build.py`. Dopo una modifica rigenerare le pagine con:

    python3 _build/build.py

Lo script scrive le pagine italiane nella cartella principale, quelle inglesi in `en/` e quelle francesi in `fr/`.
La cartella `_build/` non viene pubblicata.

## Struttura

- `index.html`, `avvocato.html`, `aree-di-attivita.html`, `rassegna-stampa.html`, `contatti.html` – pagine italiane
- `en/` – pagine inglesi
- `fr/` – pagine francesi
- `assets/style.css` – stile
- `assets/main.js` – menu mobile, mappe caricate solo su richiesta, animazioni
- `assets/logo*.svg`, `assets/favicon.svg` – logo: M con bilancia e alloro (dal disegno fornito dallo Studio, ricolorato)
- `_build/hero-mark.svg` – versione su fondo scuro del simbolo, inserita nell'apertura della home
- `assets/palermo-skyline.svg` – illustrazione originale di Palermo usata come sfondo provvisorio
- `assets/fonts/` – Cormorant Garamond e Inter (licenza SIL OFL)

## Foto di sfondo della home

Copiare la foto in `assets/` e impostare `HERO_PHOTO` in `_build/build.py` con il nome del file
e i crediti richiesti dalla licenza; poi rigenerare le pagine. Usare solo foto con licenza
che ne consenta l'uso (ad es. CC0, CC BY, CC BY-SA citando l'autore).

## Dati personali e deontologia

Dal CV sono stati ripresi solo il percorso professionale e gli incarichi. Non pubblicare
nomi dei clienti (art. 35 Codice Deontologico Forense), numeri di ruolo delle cause,
data di nascita o recapiti personali.

## Rassegna stampa e copyright

Per ogni articolo si riportano solo il titolo originale con la fonte, una sintesi scritta
dallo Studio e il link all'articolo. Non copiare testo o immagini degli articoli.

## Da completare

- Partita IVA (obbligatoria): variabile `VAT` in `_build/build.py` (per ora non mostrata)
