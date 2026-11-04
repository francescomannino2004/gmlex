"""Genera artifact/agenda.html (la pagina pubblicata su Claude) da content/ e materiali/."""
import json, os, re, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
CFU = {"vc": 6, "emergence": 6, "corporate-venturing": 6, "data-analysis": 8, "ip-law": 6}

def front(md):
    m = re.match(r"^---\n(.*?)\n---\n?", md, re.S)
    if not m: return {}, md
    meta = {}
    for line in m.group(1).splitlines():
        k, _, v = line.partition(":")
        if v: meta[k.strip()] = v.strip()
    return meta, md[m.end():]

courses = []
for d in sorted((ROOT / "content").iterdir()):
    if not (d / "course.json").exists(): continue
    c = json.loads((d / "course.json").read_text())
    c["cfu"] = CFU.get(c["id"], "")
    c["quiz"] = json.loads((d / "quiz.json").read_text()) if (d / "quiz.json").exists() else {}
    c["lectures"] = {}
    for f in sorted((d / "lectures").glob("*.md")):
        meta, body = front(f.read_text())
        c["lectures"][f.name] = {"file": f.name, "title": meta.get("title", f.name), "date": meta.get("date", ""), "wispr": meta.get("wispr", ""), "body": body.strip()}
    mdir = ROOT / "materiali" / c["id"]
    idx = json.loads((mdir / "index.json").read_text()) if (mdir / "index.json").exists() else []
    for m in idx:
        t = mdir / ".text" / (m["file"] + ".txt")
        m["text"] = re.sub(r"[ \t]+", " ", t.read_text()) if t.exists() else ""
    c["materials"] = idx
    courses.append(c)
courses.sort(key=lambda c: c.get("order", 99))
data = json.dumps({"courses": courses}, ensure_ascii=False).replace("</", "<\\/")
tpl = (ROOT / "artifact" / "template.html").read_text()
out = tpl.replace("/*__DATA__*/", data)
(ROOT / "artifact" / "agenda.html").write_text(out)
print("ok", len(out) // 1024, "KB")
