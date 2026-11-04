# Note per Claude

Progetto: agenda di studio di Francesco (master INTENT/EMIT, Bocconi, a.a. 2026/27). Lingua dell'interfaccia e delle spiegazioni: italiano; termini tecnici in inglese (i corsi sono in inglese).

## Aggiornare gli appunti da Wispr Flow
1. `search_meetings` (Wispr Flow) per le lezioni nuove; le cartelle Wispr sono: VC, the emergence, data analysis, Corporate Venturing, IP law (alcune lezioni non sono in cartella: classificale dal titolo).
2. `get_meeting` → crea `content/<materia>/lectures/AAAA-MM-GG-slug.md` con frontmatter `title`, `date`, `wispr` (share_link) e il summary come corpo.
3. Aggiungi il file alla lista `lectures` dell'argomento giusto in `content/<materia>/course.json` (confronta data e titolo col syllabus).
4. Aggiungi 3-6 domande in `content/<materia>/quiz.json` (chiave = nome file; `mc` con `answer` = array di indici, `open` con `answer` = traccia).

## Pubblicazione su Claude
- Dopo ogni modifica a content/ o materiali/: `python3 artifact/build.py`, poi ripubblica artifact/agenda.html sullo stesso URL (https://claude.ai/artifact/9nP1WdwM12iiqwQxUvrFWc).

## Regole
- VC: solo il 2° parziale (Part Three, argomenti 13-24) conta per l'esame; il 1° parziale è già superato (30 e lode) → `status: "done"`.
- Gli appunti finali vanno costruiti integrando slide/student notes/casi dei docenti (in `materiali/`) con le registrazioni. Francesco spiegherà il formato degli appunti materia per materia: seguire le sue indicazioni.
- Non inventare date d'esame: lasciare `""` se non note.
