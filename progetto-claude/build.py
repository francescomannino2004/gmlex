"""Genera i file di conoscenza per il Progetto Claude (uno per materia) da content/ e materiali/."""
import json, re, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "progetto-claude"

def front(md):
    m = re.match(r"^---\n(.*?)\n---\n?", md, re.S)
    meta = {}
    if m:
        for line in m.group(1).splitlines():
            k, _, v = line.partition(":")
            if v: meta[k.strip()] = v.strip()
        md = md[m.end():]
    return meta, md.strip()

for d in sorted((ROOT / "content").iterdir()):
    if not (d / "course.json").exists(): continue
    c = json.loads((d / "course.json").read_text())
    quiz = json.loads((d / "quiz.json").read_text()) if (d / "quiz.json").exists() else {}
    lec = {}
    for f in sorted((d / "lectures").glob("*.md")):
        lec[f.name] = front(f.read_text())
    o = [f"# {c['name']} ({c['code']})", "",
         f"- Docenti: {c['professors']}",
         f"- Ambito d'esame: {c['scope']}",
         f"- Esame: {c['exam']['label']} — data: {c['exam']['date'] or 'da definire'}",
         f"- Formato: {c['exam']['format']}",
         f"- Valutazione: {'; '.join(c.get('assessment', []))}", "",
         "## Programma (syllabus)", "",
         "| N. | Data | Argomento | Stato | Appunti disponibili |", "|---|---|---|---|---|"]
    for t in c["topics"]:
        if t["kind"] == "project": continue
        stato = "GIÀ SUPERATO (fuori esame)" if t["status"] == "done" else {"lesson": "da esame", "guest": "da esame (guest)", "group": "lavoro di gruppo", "lab": "data lab"}.get(t["kind"], t["kind"])
        app = ", ".join(lec[f][0].get("title", f).split(" — ")[0] for f in t["lectures"]) or "nessuna registrazione"
        o.append(f"| {t['n']} | {t['date'] or 'n.d.'} | {t['title']} | {stato} | {app} |")
    o += ["", "## Appunti delle lezioni (dalle registrazioni Wispr Flow)", ""]
    for t in c["topics"]:
        for f in t["lectures"]:
            meta, body = lec[f]
            body = re.sub(r"^### ", "#### ", body, flags=re.M)
            tag = " — GIÀ SUPERATO" if t["status"] == "done" else ""
            o += [f"### {meta.get('title', f)}{tag}", f"_Data: {meta.get('date','')} · Argomento del syllabus {t['n']}: {t['title']}_", "", body, ""]
    o += ["## Banca domande di esercizio (con soluzioni: NON mostrarle prima che lo studente risponda)", ""]
    for t in c["topics"]:
        for f in t["lectures"]:
            qs = quiz.get(f, [])
            if not qs or t["status"] == "done": continue
            o.append(f"### Domande — {lec[f][0].get('title', f)}")
            for i, q in enumerate(qs, 1):
                if q["type"] == "mc":
                    opts = " | ".join(f"{chr(65+j)}) {x}" for j, x in enumerate(q["options"]))
                    ans = ", ".join(chr(65+j) for j in q["answer"])
                    o.append(f"{i}. [Scelta multipla] {q['q']} — Opzioni: {opts} — Soluzione: {ans}. {q.get('explain','')}")
                else:
                    o.append(f"{i}. [Aperta] {q['q']} — Traccia di soluzione: {q['answer']}")
            o.append("")
    mdir = ROOT / "materiali" / c["id"]
    idx = json.loads((mdir / "index.json").read_text()) if (mdir / "index.json").exists() else []
    if idx:
        o += ["## Materiali dei docenti", ""]
        for m in idx:
            t = mdir / ".text" / (m["file"] + ".txt")
            txt = re.sub(r"[ \t]+", " ", t.read_text()) if t.exists() else ""
            o += [f"### {m['file']} ({m['kind']})", "", txt.strip(), ""]
    name = {"vc": "1-VC", "corporate-venturing": "2-Corporate-Venturing", "emergence": "3-The-Emergence", "data-analysis": "4-Data-Analysis", "ip-law": "5-IP-Law"}[c["id"]]
    (OUT / f"{name}.md").write_text("\n".join(o))
    print(name, len("\n".join(o)) // 1024, "KB")
