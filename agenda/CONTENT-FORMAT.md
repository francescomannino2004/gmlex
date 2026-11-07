# Agenda di Sessione — content format

Live page: https://claude.ai/artifact/DbPRwYV4xPcgvvX1W19t7b (database written with ArtifactData).

## Collections
| Collection | Doc id | Written by |
|---|---|---|
| `courses` | `cvis`, `vc`, `da`, `ent`, `ip` | seed / page (Materie → Modifica) |
| `lessons` | `<course>-NN` (e.g. `ip-04`) | seed / page; Claude sets `notes: "full" \| "transcript"` when notes are written |
| `notes` | same id as the lesson | Claude |
| `quiz` | `<lessonId>-qNN` | Claude (page adds `ai` explanations) |
| `materials` | any | page upload or Claude (`{lessonId, courseId, name, kind: pdf\|slides\|transcript\|other, url, at}`) |
| `log` | any | `{at, date, type, text, courseId}` — add an entry when notes are uploaded |
| page-only | `qstate`, `cardstate`, `plans`, `sessions`, `diary`, `tasks`, `highlights`, `audio`, `settings` | page |

## `notes/<lessonId>` (English, narrative, never telegraphic)
```json
{ "courseId": "ip", "lessonId": "ip-04", "title": "…", "source": "full|transcript", "updatedAt": 0,
  "intro": "<p>2–3 paragraphs: where the lesson comes from, link to the previous one, the question it answers, why it matters</p>",
  "message": "The lesson in one sentence.",
  "thread": ["question each chapter answers", "…"],
  "chapters": [{ "id": "c1", "title": "…", "html": "<p>flowing prose with numbers inside sentences…</p>" }],
  "recap": "<p>summary of the thread</p><h3>Numbers to know</h3><ul><li><b>Term</b> — meaning</li></ul><h3>Exam angle</h3>…" }
```
5–8 chapters. Few boxes, only where useful:
`<div class="box def" data-q="What is …?"><div class="box-t">Definition · Term</div><p>…</p></div>` · classes `remember`, `why`, `example`, `read` (How to read it), `exam` (Exam angle / traps).
Flashcards are generated from `.box.def`, `.box.remember`, recap `<li><b>front</b> — back</li>` and code lines.

Visuals: math `\( … \)` / `\[ … \]` (KaTeX); tables; `<div class="flow"><div><b>Step</b>text</div>…</div>`; `<pre class="mermaid">…</pre>`;
bars `<div class="bars" data-title="…" data-unit="%" data-bars='[["label",12]]'></div>`; slide images `<figure><img src="ASSET_URL"><figcaption>How to read it…</figcaption></figure>`.

Code (programming courses), one `.cl` per line/statement, output below with its type, no backticks:
```html
<div class="code"><div class="cl"><pre>df.groupby("sector")["amount"].mean()</pre><div class="out"><span class="ty">Series</span><pre>sector
fintech    4.2
…</pre></div></div></div>
```

## `quiz/<lessonId>-qNN` (8–10 per lesson, exam format)
```json
{ "courseId": "vc", "lessonId": "vc-18", "order": 1, "type": "mc|num|open",
  "q": "<p>…</p>", "options": ["…","…","…","…"], "answer": 2,
  "explanation": "<p>why</p>", "chapter": "c3", "quote": "exact sentence copied from that chapter",
  "hint": "formula only, e.g. \\( V_{post} = V_{pre} + I \\)", "steps": "<ol><li>…numbers of the question, checked…</li></ol>",
  "model": "<p>model answer (open questions)</p>" }
```

## Workflow for case lessons (agreed with the student)
1. Case PDF → upload as asset, add a `materials` row on the lesson.
2. Look for the class recording in Wispr Flow (folders "Corporate Venturing", "VC", "IP law", "the emergence", "data analysis"; titles carry the date) and read the WHOLE transcript.
3. Notes integrate case + recording, with explicit attention to what the professors asked (questions, cold calls, group tasks, frameworks, takeaways, exam remarks): a "What the professor asked in class" chapter/box with model answers.
4. No recording → notes from the case only; say so to the student.
5. 10 quiz questions per lesson in the course's exam format, favouring the professors' questions.
6. Every multiple-choice question has EXACTLY ONE correct answer (student's rule, also for VC): never "B and D" or "select all that apply", even if a professor said otherwise in class.

## Word notes per subject (agreed with the student)
Each subject has one Word file (style: tools/WORD-FORMAT.md, builder: tools/build-docx.js) shown on the subject page as a `materials` doc `word-<course>` `{kind:'word', name, desc, pages:N, pagePrefix:'word/<course>/p-' (page images published with the page, made with pdftoppm -jpeg -r 110 from the LibreOffice PDF; opening a PDF link is blocked by claude.ai), url:<GitHub raw link to the .docx>, lessons:[ids included], at}`.
Whenever lesson notes are written or rewritten (log `notes-<id>` gets a newer `at`), also rewrite that lesson's Word JSON, rebuild the course .docx + PDF, re-render the page images and republish them with the page, push the .docx, and update `word-<course>` (`at`, `lessons`). The page flags "Word da aggiornare" when a log entry is newer than `at` or a lesson with notes is missing from `lessons`.
