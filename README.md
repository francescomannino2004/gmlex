# gmlex — Agenda di studio

App web locale per preparare gli esami del semestre:

- **Dashboard**: ogni materia con la **percentuale di programma** studiato e verificato, il countdown all'esame e consigli su cosa fare oggi.
- **Appunti**: per ogni lezione gli appunti ricavati dalle registrazioni **Wispr Flow**, collegati all'argomento del syllabus e ai **materiali dei docenti** (slide, student notes, casi). Accanto c'è un **tutor AI** (Claude) che risponde ai dubbi usando appunti e materiali del corso, citando le fonti.
- **Esercizi**: domande per ogni lezione (scelta multipla, anche con più risposte corrette, e domande aperte/numeriche corrette dall'AI). Puoi generarne di nuove e ripetere solo quelle sbagliate.
- **Programma**: il syllabus completo con lo stato di ogni argomento (svolto, registrato, studiato) e la data d'esame modificabile.
- **Materiali**: caricamento di PDF/PPTX/DOCX; il testo viene estratto e usato da tutor ed esercizi.

## Materie

| Materia | Ambito | Esame |
|---|---|---|
| Venture Capital and Valuation (VC) | solo 2° parziale (Part Three, prof. Zava) | 21 dicembre 2026 (MCQ) |
| The Emergence of Entrepreneurial Ventures | programma completo | da definire (60% scritto + 40% progetto) |
| Corporate Venturing and Innovation Strategy | programma completo | 11 dicembre 2026 (anche 25 gennaio) |
| Data Analysis Module I | programma completo | da definire (60% scritto + 40% progetto) |
| IP Law for Business | programma completo | sessione gennaio/febbraio |

## Come avviarla

Serve Node.js 20 o superiore.

```bash
npm install
```

```bash
ANTHROPIC_API_KEY=sk-ant-... npm start
```

Poi apri http://localhost:3000. Senza `ANTHROPIC_API_KEY` l'app funziona lo stesso (appunti, esercizi a scelta multipla, progressi), ma tutor, correzione delle risposte aperte e generazione di domande restano disattivati.

Variabili opzionali: `PORT` (default 3000), `CLAUDE_MODEL` (default `claude-opus-5-5`), `MATERIAL_CHAR_BUDGET` (caratteri di materiali inviati al tutor per richiesta, default 400000).

## Come si calcola la percentuale

- Lezione = 30% "segnata come studiata" + 70% miglior risultato agli esercizi.
- Argomento del syllabus = media delle sue lezioni (per argomenti senza registrazione puoi spuntare "studiato" a mano nella scheda Programma).
- Materia = media degli argomenti che contano per l'esame (esclusi lavori di gruppo, data lab e, per VC, il 1° parziale già superato).

I progressi sono salvati in `data/progress.json` (non versionato).

## Struttura

```
content/<materia>/course.json      syllabus, esame, mappa argomento → lezioni
content/<materia>/lectures/*.md    appunti per lezione (frontmatter: title, date, link Wispr)
content/<materia>/quiz.json        domande per lezione
materiali/<materia>/               materiali dei docenti + .text/ (testo estratto) + index.json
server.js                          API, upload, tutor Claude (streaming), correzione, generazione domande
public/                            frontend
```

## Versione su Claude (artifact)

La stessa agenda è pubblicata come pagina su Claude: https://claude.ai/artifact/9nP1WdwM12iiqwQxUvrFWc

- Il tutor, la correzione delle risposte aperte e la generazione di domande usano direttamente Claude con l'account di chi apre la pagina (nessuna chiave API).
- I progressi sono salvati sull'account (database privato per utente dell'artifact).
- La pagina viene generata con `python3 artifact/build.py` a partire da `artifact/template.html`, `content/` e `materiali/`; dopo ogni aggiornamento dei contenuti va rigenerata e ripubblicata.
