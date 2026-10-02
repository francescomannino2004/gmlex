# gmlex

Sito web dello Studio Legale Mannino (Avv. Manlio Mannino – Palermo e Roma).

Sito statico, senza dipendenze esterne e senza cookie propri:

- `index.html` – Home page (Lo Studio, contatti, aree di attività)
- `aree-di-attivita.html` – dettaglio delle aree di attività
- `contatti.html` – sedi di Palermo e Roma con mappe
- `assets/style.css` – stile
- `assets/main.js` – menu, mappe caricate su richiesta e traduzione inglese
- `assets/fonts/` – carattere EB Garamond (licenza SIL OFL)

## Lingue

Il testo italiano è scritto direttamente nelle pagine HTML. Le traduzioni inglesi
sono in `assets/main.js` (oggetto `EN`), collegate tramite l'attributo `data-i18n`.
Quando si modifica un testo italiano va aggiornata anche la voce inglese corrispondente.

## Pubblicazione

GitHub Pages: Settings → Pages → Deploy from a branch → scegliere il branch e la cartella `/ (root)`.

Da completare: Partita IVA nel footer (obbligatoria).
