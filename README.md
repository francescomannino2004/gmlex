# gmlex

Sito web dello Studio Legale Mannino (Avv. Manlio Mannino – Palermo e Roma).
Pubblicato con GitHub Pages: https://francescomannino2004.github.io/gmlex/

Sito statico in italiano e inglese, senza dipendenze esterne e senza cookie propri.

## Come modificare i contenuti

Tutti i testi (italiano e inglese), le aree di attività, le sedi e la rassegna stampa
sono in `_build/build.py`. Dopo una modifica rigenerare le pagine con:

    python3 _build/build.py

Lo script scrive le pagine italiane nella cartella principale e quelle inglesi in `en/`.
La cartella `_build/` non viene pubblicata.

## Struttura

- `index.html`, `aree-di-attivita.html`, `rassegna-stampa.html`, `contatti.html` – pagine italiane
- `en/` – pagine inglesi
- `assets/style.css` – stile
- `assets/main.js` – menu mobile, mappe caricate solo su richiesta, animazioni
- `assets/logo*.svg`, `assets/favicon.svg` – logo
- `assets/fonts/` – Cormorant Garamond e Inter (licenza SIL OFL)

## Rassegna stampa e copyright

Per ogni articolo si riportano solo il titolo originale con la fonte, una sintesi scritta
dallo Studio e il link all'articolo. Non copiare testo o immagini degli articoli.

## Da completare

- Partita IVA (obbligatoria): variabile `VAT` in `_build/build.py`
- Date di pubblicazione degli articoli in rassegna stampa
