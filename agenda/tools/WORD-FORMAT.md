# Word notes: format for one lesson (read fully)

Goal: for each lesson, a compact, discursive set of "explanatory notes" in the style of the student's model document
(/tmp/claude-0/-home-user-gmlex/9701f911-1682-5db2-8380-7d99912ad823/scratchpad/word/ex/example.txt is its text;
ex/page-01.jpg, page-03.jpg, page-04.jpg show the look). Study the example first: that is the target style.

## Style (from the model document)
- English. Flowing prose paragraphs, dense but readable; **bold** the key terms and key results inside sentences (several per paragraph, like the example). *Italics* for asides.
- Opening paragraph (no heading): where the lesson comes from (link to the previous lesson), what it covers, which sessions/dates, what to focus on for the exam.
- 4–8 sections ("h1"), with "h2" sub-sections only where useful. Section titles are topic names (e.g. "Pre-Money and Post-Money Valuation"), not questions.
- Visual elements only when they help: tables (comparisons, worked computations, typologies) with a caption; centred formulas; a figure when a graph/diagram really explains something (payoff curves, frameworks, timelines, bar charts of key numbers, flow diagrams). Typical lesson: 1–3 tables, 0–2 figures, formulas when there is math.
- Worked examples with the numbers checked. Professor's remarks/exam angle woven in (e.g. "the professor stressed…", "exam trap: …"); a closing short section "Exam angle" or "Key takeaways" is fine.
- NOT TOO LONG: target 1,300–2,200 words of text per lesson (≈3–5 pages). Condense: keep every fundamental concept, definition, framework, number and case that matters, drop repetition and anecdotes. No quiz questions.
- Group work is excluded. Cases (e.g. CVIS cases) are included.

## Source
The full web notes of the lesson: /tmp/claude-0/-home-user-gmlex/9701f911-1682-5db2-8380-7d99912ad823/scratchpad/word/db/notes/<id>.json
(fields intro, message, thread, chapters[].html, recap; HTML with boxes/tables/bars/code). These are complete and verified: rewrite/condense them, do not invent new facts. Lesson metadata (date, title, instructor) in word/db/lessons/<id>.json.
If a figure would benefit from the original slide, slide PDFs may exist under scratchpad/ (vc/, ent/, ip/, cvis…); optional.

## Output: word/<course>/<id>.json
{"id":"vc-13","title":"<lesson title, Title Case>","subtitle":"Lesson 13 (28/10) explanatory notes","blocks":[ ... ]}
Guest lessons: subtitle like "Guest speaker · ENGIE · 15/10".
Blocks (in order):
- {"t":"p","text":"…"}                         paragraph. Inline markup: **bold**, *italic*, _{sub}, ^{sup}. No HTML, no backticks, no LaTeX.
- {"t":"h1","text":"Section title"}            {"t":"h2","text":"Sub-section"}
- {"t":"formula","text":"Post-money = Pre-money + I   s = I / Post-money"}   plain-text math with Unicode (×, −, ≤, Σ, √, →) and _{ } ^{ }; separate several formulas on one line with 3+ spaces.
- {"t":"table","head":["…","…"],"rows":[["…","…"]],"widths":[1,2],"caption":"Pre/post-money arithmetic (illustrative)"}  first column is shown bold; cells may use **bold** and "\n" for line breaks. Keep cells short; ≤5 columns.
- {"t":"figure","file":"figs/<id>-1.png","caption":"Investor payoffs with …","width":6.3}  (width in inches, ≤6.5; use 4–5 for small diagrams)
- {"t":"box","title":"Worked example","text":"…\n\n…"}   shaded box, use sparingly (worked example, exam trap).
- {"t":"bullets","items":["…"]} / {"t":"numbered","items":["…"]}  use sparingly; prose first.
- {"t":"code","lines":[{"code":"df.shape","out":"(10, 4)","type":"tuple"}],"caption":"…"}  (Data Analysis only: one entry per statement, output and type below; keep only the important lines).
Captions without "Table N"/"Figure N" (numbering is automatic).

## Figures
Make them with matplotlib (installed) via a python script word/<course>/figs/<id>.py writing PNGs to word/<course>/figs/ at dpi=200, figsize width ≈6.5 in, white background, font size 9, navy #17365D / orange #D9822B / grey palette, no top/right spines, light grid, labelled axes, legend without frame. Diagrams (flows, frameworks, 2×2 matrices) can be drawn with matplotlib patches + text. Check numbers. Look at every PNG you make (Read it) before using it.

## Check
After writing your lessons run:  node /tmp/claude-0/-home-user-gmlex/9701f911-1682-5db2-8380-7d99912ad823/scratchpad/word/build-docx.js <course>
It must print "wrote …" with no "MISSING FIGURE"/"unknown block". Also count words: python3 -c "import json,sys,re;d=json.load(open(sys.argv[1]));print(sum(len(re.sub(r'[*_^{}]','',str(b.get('text','')+' '.join(map(str,b.get('items',[])))+' '.join(' '.join(map(str,r)) for r in b.get('rows',[])))).split()) for b in d['blocks']))" word/<course>/<id>.json
