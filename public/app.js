// Agenda di studio — frontend (vanilla JS, routing con hash).
const app = document.getElementById("app");
const KIND_LABEL = { slides: "Slide", notes: "Student notes", case: "Caso", reading: "Lettura", exercises: "Esercizi", other: "Altro" };

marked.use({ renderer: { html: (token) => esc(typeof token === "string" ? token : token.text) } });
const md = (s) => marked.parse(s || "");

function esc(s) {
  return String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[c]);
}
async function api(url, opts = {}) {
  const res = await fetch(url, {
    ...opts,
    headers: opts.body && !(opts.body instanceof FormData) ? { "Content-Type": "application/json" } : undefined,
    body: opts.body && !(opts.body instanceof FormData) ? JSON.stringify(opts.body) : opts.body,
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data.error || `Errore ${res.status}`);
  return data;
}
function daysUntil(date) {
  if (!date) return null;
  const d = new Date(date + "T00:00:00");
  return Math.ceil((d - new Date(new Date().toDateString())) / 86400000);
}
function fmtDate(date) {
  if (!date) return "data da definire";
  return new Date(date + "T00:00:00").toLocaleDateString("it-IT", { day: "numeric", month: "long", year: "numeric" });
}
function examBadge(date) {
  const d = daysUntil(date);
  if (d === null) return `<span class="pill">Esame: data da definire</span>`;
  if (d < 0) return `<span class="pill">Esame passato (${fmtDate(date)})</span>`;
  const cls = d <= 14 ? "warn" : "";
  return `<span class="pill ${cls}">Esame tra ${d} giorni · ${fmtDate(date)}</span>`;
}
const store = {
  get(k, def) { try { return JSON.parse(localStorage.getItem(k)) ?? def; } catch { return def; } },
  set(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch {} },
};

let STATUS = { ai: false };
api("/api/status").then((s) => {
  STATUS = s;
  const el = document.getElementById("ai-status");
  el.textContent = s.ai ? "Tutor AI attivo" : "Tutor AI non configurato";
  el.className = `pill ${s.ai ? "ok" : "warn"}`;
}).catch(() => {});

// ---------------- Router ----------------
window.addEventListener("hashchange", route);
route();

async function route() {
  const parts = location.hash.replace(/^#\/?/, "").split("/").filter(Boolean).map(decodeURIComponent);
  try {
    if (parts[0] === "c" && parts[1]) await coursePage(parts[1], parts[2] || "appunti", parts[3]);
    else await dashboard();
  } catch (e) {
    app.innerHTML = `<div class="card"><b>Errore:</b> ${esc(e.message)}</div>`;
  }
  window.scrollTo(0, 0);
}

// ---------------- Dashboard ----------------
async function dashboard() {
  const courses = await api("/api/courses");
  const cards = courses.map((c) => `
    <a class="card course-card" style="--c:${c.color}" href="#/c/${c.id}">
      <h3>${esc(c.short)}</h3>
      <div class="muted small">${esc(c.name)}</div>
      <div class="big-percent">${c.percent}%</div>
      <div class="bar"><span style="width:${c.percent}%"></span></div>
      <div class="small muted">${c.heldTopics}/${c.totalTopics} argomenti già svolti in aula · ${c.recordedTopics} con registrazione · ${c.materialCount} materiali caricati</div>
      <div class="meta-row">${examBadge(c.exam?.date)}<span class="pill">${esc(c.exam?.label || "")}</span></div>
    </a>`).join("");
  app.innerHTML = `
    <h1>Le tue materie</h1>
    <p class="muted">La percentuale misura quanto del programma d'esame hai studiato e verificato: per ogni lezione conta 30% “studiata” + 70% miglior risultato agli esercizi.</p>
    <div class="grid">${cards}</div>
    <div class="card tips"><h2 style="margin-top:0">Consigli per oggi</h2><ul>${tips(courses)}</ul></div>`;
}

function tips(courses) {
  const out = [];
  const upcoming = courses.filter((c) => c.exam?.date && daysUntil(c.exam.date) >= 0).sort((a, b) => daysUntil(a.exam.date) - daysUntil(b.exam.date));
  if (upcoming[0]) {
    const c = upcoming[0];
    const d = daysUntil(c.exam.date);
    const remaining = 100 - c.percent;
    out.push(`<b>${esc(c.short)}</b> è il prossimo esame (tra ${d} giorni): ti manca il ${remaining}% del programma, cioè circa ${d > 0 ? (remaining / d).toFixed(1) : remaining}% al giorno.`);
  }
  const noDate = courses.filter((c) => !c.exam?.date);
  if (noDate.length) out.push(`Imposta la data d'esame per ${noDate.map((c) => `<a href="#/c/${c.id}/programma">${esc(c.short)}</a>`).join(", ")} (scheda Programma) per avere countdown e ritmo giornaliero.`);
  const missing = courses.filter((c) => c.heldTopics > c.recordedTopics && c.materialCount === 0);
  if (missing.length) out.push(`Alcune lezioni già svolte non hanno registrazione: carica slide/student notes per ${missing.map((c) => `<a href="#/c/${c.id}/materiali">${esc(c.short)}</a>`).join(", ")}, così tutor ed esercizi le coprono.`);
  out.push("Metodo: leggi gli appunti, fai gli esercizi della lezione <i>senza</i> guardare, poi chiedi al tutor di spiegarti solo gli errori. Ripeti gli esercizi sbagliati dopo 2-3 giorni (ripetizione dilazionata).");
  return out.map((t) => `<li>${t}</li>`).join("");
}

// ---------------- Course page ----------------
async function coursePage(id, tab, sub) {
  const data = await api(`/api/courses/${id}`);
  const c = data.course;
  const tabs = [["appunti", "Appunti"], ["esercizi", "Esercizi"], ["programma", "Programma"], ["materiali", "Materiali"]];
  app.innerHTML = `
    <div class="course-head" style="--c:${c.color}">
      <div>
        <a href="#/" class="small">← Tutte le materie</a>
        <h1>${esc(c.name)}</h1>
        <div class="muted small">${esc(c.professors)} · ${esc(c.scope)}</div>
      </div>
      <div style="text-align:right">
        <div class="big-percent" style="--c:${c.color};margin:0">${data.percent}%</div>
        ${examBadge(c.exam?.date)}
      </div>
    </div>
    <nav class="tabs" style="--c:${c.color}">${tabs.map(([k, l]) => `<a href="#/c/${id}/${k}" class="${tab === k ? "active" : ""}">${l}</a>`).join("")}</nav>
    <section id="tab"></section>`;
  const el = document.getElementById("tab");
  if (tab === "esercizi") return exercisesTab(el, data, sub);
  if (tab === "programma") return programTab(el, data);
  if (tab === "materiali") return materialsTab(el, data);
  return notesTab(el, data, sub);
}

function lectureSidebar(data, base, activeFile) {
  const group = (t) => `
      <div class="group">
        <div class="group-title">${t.n ? `${t.n}. ` : ""}${esc(t.title)}${t.status === "done" ? " · già superato" : ""}</div>
        ${t.lectures.map((f) => {
          const l = data.lectures[f];
          const ok = l.progress?.studied ? `<span class="check">✓</span> ` : "";
          const score = l.progress?.bestScore != null ? ` <span class="muted small">${Math.round(l.progress.bestScore * 100)}%</span>` : "";
          return `<a class="item ${f === activeFile ? "active" : ""}" href="${base}/${encodeURIComponent(f)}">${ok}${esc(l.title.replace(/^.*? — /, ""))}${score}</a>`;
        }).join("")}
      </div>`;
  const withLectures = data.topics.filter((t) => t.lectures.length);
  const active = withLectures.filter((t) => t.status !== "done");
  const done = withLectures.filter((t) => t.status === "done");
  const doneOpen = done.some((t) => t.lectures.includes(activeFile));
  const groups = active.map(group).join("") +
    (done.length ? `<details ${doneOpen ? "open" : ""}><summary class="group-title" style="cursor:pointer">Parziale già superato (${done.reduce((n, t) => n + t.lectures.length, 0)} lezioni)</summary>${done.map(group).join("")}</details>` : "");
  const missing = data.topics.filter((t) => !t.lectures.length && t.counts && t.held && t.date).length;
  return `<div class="card side">
    <a class="item ${!activeFile ? "active" : ""}" href="${base}">🎓 Tutor su tutta la materia</a>
    ${groups}
    ${missing ? `<div class="empty">${missing} argomenti già svolti senza registrazione: <a href="#/c/${data.course.id}/materiali">carica i materiali</a>.</div>` : ""}
  </div>`;
}

// ---------- Appunti + tutor ----------
async function notesTab(el, data, file) {
  const id = data.course.id;
  const base = `#/c/${id}/appunti`;
  if (!file) {
    const first = data.topics.filter((t) => t.counts && t.lectures.length).at(-1);
    el.innerHTML = `<div class="notes-layout">${lectureSidebar(data, base, null)}
      <article class="card notes">
        <h2 style="margin-top:0">Appunti di ${esc(data.course.short)}</h2>
        <p>Scegli una lezione a sinistra. Ogni scheda unisce gli <b>appunti dalla registrazione Wispr Flow</b> e i <b>materiali dei docenti</b> collegati a quell'argomento del syllabus (slide, student notes, casi), che il tutor legge per risponderti.</p>
        <p class="muted">${Object.keys(data.lectures).length} lezioni registrate · ${data.materials.length} materiali caricati.</p>
        ${first ? `<p>Ultima lezione: <a href="${base}/${encodeURIComponent(first.lectures.at(-1))}">${esc(data.lectures[first.lectures.at(-1)].title)}</a></p>` : ""}
        <div class="source-box"><b>Come vengono calcolati i progressi:</b> segna una lezione come “studiata” quando hai letto e capito gli appunti, poi fai gli esercizi. Il miglior risultato degli esercizi pesa il 70%.</div>
      </article>
      ${chatPanel(id, null)}</div>`;
    return bindChat(id, null);
  }
  const lec = await api(`/api/courses/${id}/lectures/${encodeURIComponent(file)}`);
  const lp = data.lectures[file]?.progress || {};
  const mats = lec.materials.length
    ? lec.materials.map((m) => `<li><a href="/materiali/${id}/${encodeURIComponent(m.file)}" target="_blank">${esc(m.file)}</a> <span class="tag">${KIND_LABEL[m.kind] || m.kind}</span></li>`).join("")
    : `<li class="muted">Nessun materiale collegato a questo argomento. <a href="#/c/${id}/materiali">Carica slide o student notes</a>.</li>`;
  el.innerHTML = `<div class="notes-layout">${lectureSidebar(data, base, file)}
    <article class="card notes">
      <div class="muted small">${fmtDate(lec.date)}${lec.topic ? ` · Syllabus n. ${lec.topic.n}: ${esc(lec.topic.title)}` : ""}</div>
      <h2 style="margin-top:4px">${esc(lec.title)}</h2>
      <div class="lecture-actions">
        <button id="studied" class="${lp.studied ? "" : "primary"}">${lp.studied ? "✓ Studiata (annulla)" : "Segna come studiata"}</button>
        <a class="btn" href="#/c/${id}/esercizi/${encodeURIComponent(file)}">✍️ Esercizi su questa lezione</a>
        ${lec.wispr ? `<a class="btn" href="${esc(lec.wispr)}" target="_blank">🎙️ Apri in Wispr Flow</a>` : ""}
      </div>
      <div class="source-box"><b>Materiali del docente per questo argomento</b><ul>${mats}</ul></div>
      ${md(lec.body)}
    </article>
    ${chatPanel(id, file)}</div>`;
  document.getElementById("studied").onclick = async () => {
    await api(`/api/courses/${id}/progress`, { method: "POST", body: { lecture: file, studied: !lp.studied } });
    route();
  };
  bindChat(id, file, lec.title);
}

function chatPanel(id, file) {
  return `<aside class="card chat-col">
    <div class="chat-head"><b>Tutor</b> <span class="muted small">${file ? "su questa lezione (e il resto del corso)" : "su tutta la materia"}</span></div>
    <div class="chat-log" id="chat-log"></div>
    <form class="chat-form" id="chat-form">
      <textarea id="chat-input" placeholder="Chiedimi qualsiasi dubbio…" rows="1"></textarea>
      <button class="primary" type="submit">Invia</button>
    </form>
  </aside>`;
}

function bindChat(id, file, title) {
  const key = `chat:${id}:${file || "_course"}`;
  let history = store.get(key, []);
  const log = document.getElementById("chat-log");
  const form = document.getElementById("chat-form");
  const input = document.getElementById("chat-input");
  const suggestions = file
    ? ["Spiegami i concetti chiave di questa lezione", "Fammi un esempio numerico", "Quali domande potrebbero uscire all'esame?", "Collega questa lezione alle altre del corso"]
    : ["Fammi un riassunto del programma d'esame", "Su cosa dovrei concentrarmi?", "Interrogami su un argomento a caso"];

  function render() {
    log.innerHTML = history.length
      ? history.map((m) => `<div class="msg ${m.role}">${m.role === "assistant" ? md(m.content) : esc(m.content)}</div>`).join("")
      : `<div class="muted small">${STATUS.ai ? "Fai una domanda o scegli un suggerimento:" : "Per attivare il tutor avvia il server con ANTHROPIC_API_KEY (vedi README)."}</div>
         <div class="suggestions">${suggestions.map((s) => `<button type="button">${esc(s)}</button>`).join("")}</div>
`;
    log.querySelectorAll(".suggestions button").forEach((b) => (b.onclick = () => ask(b.textContent)));
    log.scrollTop = log.scrollHeight;
  }
  if (history.length) {
    const clear = document.createElement("button");
    clear.textContent = "Nuova chat";
    clear.style.cssText = "float:right;font-size:12px;padding:2px 8px";
    clear.onclick = () => { history = []; store.set(key, history); render(); clear.remove(); };
    document.querySelector(".chat-head").appendChild(clear);
  }

  async function ask(text) {
    if (!text.trim()) return;
    history.push({ role: "user", content: text.trim() });
    const answer = { role: "assistant", content: "" };
    history.push(answer);
    render();
    const bubble = log.lastElementChild;
    bubble.innerHTML = `<span class="muted">Sto pensando…</span>`;
    form.querySelector("button").disabled = true;
    try {
      const res = await fetch(`/api/courses/${id}/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ lecture: file, messages: history.slice(0, -1) }),
      });
      if (!res.ok) throw new Error((await res.json().catch(() => ({}))).error || `Errore ${res.status}`);
      const reader = res.body.getReader();
      const dec = new TextDecoder();
      let buf = "";
      for (;;) {
        const { value, done } = await reader.read();
        if (done) break;
        buf += dec.decode(value, { stream: true });
        const events = buf.split("\n\n");
        buf = events.pop();
        for (const ev of events) {
          const line = ev.replace(/^data: /, "");
          if (!line) continue;
          const msg = JSON.parse(line);
          if (msg.text) { answer.content += msg.text; bubble.innerHTML = md(answer.content); log.scrollTop = log.scrollHeight; }
          if (msg.error) throw new Error(msg.error);
        }
      }
    } catch (e) {
      if (!answer.content) history.pop();
      history.pop();
      store.set(key, history);
      render();
      log.insertAdjacentHTML("beforeend", `<div class="msg error">${esc(e.message)}</div>`);
      form.querySelector("button").disabled = false;
      return;
    }
    store.set(key, history);
    form.querySelector("button").disabled = false;
  }
  form.onsubmit = (e) => { e.preventDefault(); const t = input.value; input.value = ""; ask(t); };
  input.onkeydown = (e) => { if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); form.requestSubmit(); } };
  render();
}

// ---------- Esercizi ----------
async function exercisesTab(el, data, file) {
  const id = data.course.id;
  const base = `#/c/${id}/esercizi`;
  if (!file) {
    const rows = data.topics.filter((t) => t.lectures.length && t.status !== "done").flatMap((t) => t.lectures.map((f) => {
      const l = data.lectures[f];
      const p = l.progress || {};
      return `<div class="topic"><div class="n">${t.n || "—"}</div>
        <div><a href="${base}/${encodeURIComponent(f)}">${esc(l.title)}</a><div class="muted small">${l.quizCount} domande${p.attempts ? ` · ${p.attempts} tentativi · ultimo ${Math.round((p.lastScore || 0) * 100)}%` : ""}${p.wrong?.length ? ` · <span class="tag warn">${p.wrong.length} da ripassare</span>` : ""}</div></div>
        <div class="score">${p.bestScore != null ? Math.round(p.bestScore * 100) + "%" : "—"}</div></div>`;
    })).join("");
    el.innerHTML = `<div class="card" style="padding:0">${rows || `<p style="padding:16px">Nessuna lezione con esercizi.</p>`}</div>
      <p class="muted small">Le lezioni del parziale già superato non sono incluse.</p>`;
    return;
  }
  const questions = await api(`/api/courses/${id}/quiz/${encodeURIComponent(file)}`);
  const lec = data.lectures[file];
  const prevWrong = new Set(lec.progress?.wrong || []);
  el.innerHTML = `<div class="notes-layout" style="grid-template-columns:270px minmax(0,1fr)">
    ${lectureSidebar(data, base, file)}
    <div>
      <div class="card">
        <div class="row" style="justify-content:space-between">
          <div><h2 style="margin:0">${esc(lec.title)}</h2><div class="muted small">${questions.length} domande · le domande a scelta multipla possono avere più risposte corrette</div></div>
          <div class="row">
            ${prevWrong.size ? `<button id="only-wrong">Solo le ${prevWrong.size} sbagliate l'ultima volta</button>` : ""}
            <button id="gen" ${STATUS.ai ? "" : "disabled title='Serve ANTHROPIC_API_KEY'"}>✨ Genera altre domande</button>
            <a class="btn" href="#/c/${id}/appunti/${encodeURIComponent(file)}">📖 Appunti</a>
          </div>
        </div>
      </div>
      <form id="quiz"></form>
    </div></div>`;
  let current = questions.map((q, i) => ({ ...q, i }));
  const quiz = document.getElementById("quiz");
  function renderQuiz() {
    quiz.innerHTML = current.map((q, k) => `
      <div class="card quiz-q" data-k="${k}">
        <div class="qtext">${k + 1}. ${esc(q.q)} ${q.generated ? `<span class="tag">generata</span>` : ""}${prevWrong.has(q.q) ? `<span class="tag warn">sbagliata l'ultima volta</span>` : ""}</div>
        ${q.type === "mc"
          ? q.options.map((o, j) => `<label class="opt"><input type="checkbox" name="q${k}" value="${j}"> <span>${esc(o)}</span></label>`).join("")
          : `<textarea name="q${k}" placeholder="Scrivi la tua risposta come all'esame…"></textarea>`}
        <div class="fb"></div>
      </div>`).join("") + `<div class="row"><button class="primary" type="submit">Correggi</button><span id="result" class="result-banner"></span></div>`;
  }
  renderQuiz();
  document.getElementById("only-wrong")?.addEventListener("click", () => { current = current.filter((q) => prevWrong.has(q.q)); renderQuiz(); });
  document.getElementById("gen").onclick = async (e) => {
    e.target.disabled = true; e.target.textContent = "Sto creando le domande…";
    try { await api(`/api/courses/${id}/generate-quiz`, { method: "POST", body: { lecture: file, count: 5 } }); route(); }
    catch (err) { alert(err.message); e.target.disabled = false; e.target.textContent = "✨ Genera altre domande"; }
  };
  quiz.onsubmit = async (e) => {
    e.preventDefault();
    const submit = quiz.querySelector("button[type=submit]");
    submit.disabled = true;
    let total = 0;
    const wrong = [];
    const pending = [];
    current.forEach((q, k) => {
      const box = quiz.querySelector(`[data-k="${k}"]`);
      const fb = box.querySelector(".fb");
      if (q.type === "mc") {
        const chosen = [...box.querySelectorAll("input:checked")].map((x) => Number(x.value));
        const right = new Set(q.answer);
        box.querySelectorAll(".opt").forEach((opt, j) => {
          if (right.has(j)) opt.classList.add("correct");
          else if (chosen.includes(j)) opt.classList.add("wrong");
        });
        const ok = chosen.length === right.size && chosen.every((j) => right.has(j));
        total += ok ? 1 : 0;
        if (!ok) wrong.push(q.q);
        fb.innerHTML = `<div class="feedback ${ok ? "good" : "bad"}">${ok ? "✓ Corretto." : "✗ Non corretto."} ${esc(q.explain || "")}</div>`;
      } else {
        const ans = box.querySelector("textarea").value;
        const showModel = `<details style="margin-top:6px"><summary>Traccia di risposta</summary>${md(q.answer || "")}</details>`;
        if (!STATUS.ai) {
          fb.innerHTML = `<div class="feedback">Confronta la tua risposta con la traccia (correzione automatica disattivata senza API key).${showModel}</div>`;
          total += ans.trim() ? 0.5 : 0;
          return;
        }
        fb.innerHTML = `<div class="feedback">Correzione in corso…</div>`;
        pending.push(api(`/api/courses/${id}/grade`, { method: "POST", body: { lecture: file, question: q.q, modelAnswer: q.answer, userAnswer: ans } })
          .then((r) => {
            total += r.score;
            if (r.score < 0.6) wrong.push(q.q);
            const cls = r.score >= 0.8 ? "good" : r.score >= 0.5 ? "mid" : "bad";
            fb.innerHTML = `<div class="feedback ${cls}"><b>${Math.round(r.score * 100)}%</b> — ${md(r.feedback)}${r.missing?.length ? `<div class="small"><b>Mancava:</b> ${r.missing.map(esc).join("; ")}</div>` : ""}${showModel}</div>`;
          })
          .catch((err) => { wrong.push(q.q); fb.innerHTML = `<div class="feedback bad">${esc(err.message)}${showModel}</div>`; }));
      }
    });
    await Promise.all(pending);
    const score = current.length ? total / current.length : 0;
    document.getElementById("result").textContent = `Risultato: ${Math.round(score * 100)}%`;
    if (current.length === questions.length) {
      await api(`/api/courses/${id}/progress`, { method: "POST", body: { lecture: file, quizScore: score, wrong } });
    }
    submit.textContent = "Rifai";
    submit.disabled = false;
    submit.onclick = (ev) => { ev.preventDefault(); route(); };
  };
}

// ---------- Programma ----------
function programTab(el, data) {
  const id = data.course.id;
  const c = data.course;
  const rows = data.topics.filter((t) => t.kind !== "project").map((t) => {
    const tags = [];
    if (t.status === "done") tags.push(`<span class="tag ok">già superato</span>`);
    if (t.kind !== "lesson") tags.push(`<span class="tag">${{ guest: "guest speaker", group: "lavoro di gruppo", lab: "data lab" }[t.kind] || t.kind}</span>`);
    if (t.counts && t.held && t.date && !t.lectures.length) tags.push(`<span class="tag warn">nessuna registrazione</span>`);
    if (t.date && !t.held) tags.push(`<span class="tag">da svolgere</span>`);
    const mats = data.materials.filter((m) => m.topic === t.n).length;
    if (mats) tags.push(`<span class="tag">${mats} materiali</span>`);
    const lectures = t.lectures.map((f) => `<a href="#/c/${id}/appunti/${encodeURIComponent(f)}">${esc(data.lectures[f].title.replace(/^.*? — /, ""))}</a>`).join(" · ");
    const manual = !t.lectures.length && t.counts
      ? `<label class="small" style="display:inline-flex;gap:6px;align-items:center;margin-top:4px"><input type="checkbox" data-topic="${t.n}" style="width:auto" ${data.topicProgress[t.n]?.studied ? "checked" : ""}> studiato</label>`
      : "";
    return `<div class="topic ${t.status === "done" || !t.counts ? "done" : ""}">
      <div class="n">${t.n}</div>
      <div><div>${esc(t.title)} ${tags.join("")}</div><div class="muted small">${t.date ? fmtDate(t.date) : ""}${t.note ? ` · ${esc(t.note)}` : ""}</div>${lectures ? `<div class="small">${lectures}</div>` : ""}${manual}</div>
      <div class="score">${t.counts ? Math.round(t.score * 100) + "%" : ""}</div>
    </div>`;
  }).join("");
  el.innerHTML = `
    <div class="card">
      <div class="row" style="justify-content:space-between">
        <div><b>${esc(c.exam?.label || "Esame")}</b><div class="muted small">${esc(c.exam?.format || "")}</div>
        <div class="small">${(c.assessment || []).map(esc).join(" · ")}</div></div>
        <label class="small">Data esame <input type="date" id="exam-date" value="${esc(c.exam?.date || "")}" style="width:auto"></label>
      </div>
    </div>
    <h2>Syllabus</h2>
    <div class="card" style="padding:0">${rows}</div>`;
  document.getElementById("exam-date").onchange = async (e) => {
    await api(`/api/courses/${id}/progress`, { method: "POST", body: { examDate: e.target.value } });
    route();
  };
  el.querySelectorAll("input[data-topic]").forEach((cb) => (cb.onchange = async () => {
    await api(`/api/courses/${id}/progress`, { method: "POST", body: { topic: Number(cb.dataset.topic), studied: cb.checked } });
    route();
  }));
}

// ---------- Materiali ----------
function materialsTab(el, data) {
  const id = data.course.id;
  const topicName = (n) => data.topics.find((t) => t.n === n)?.title || "Generale";
  const rows = data.materials.map((m) => `<tr>
      <td><a href="/materiali/${id}/${encodeURIComponent(m.file)}" target="_blank">${esc(m.file)}</a></td>
      <td>${KIND_LABEL[m.kind] || m.kind}</td>
      <td>${m.topic ? `${m.topic}. ${esc(topicName(m.topic))}` : "Generale"}</td>
      <td class="muted">${m.chars ? `${Math.round(m.chars / 1000)}k caratteri letti` : "<span class='tag warn'>testo non estratto</span>"}</td>
      <td><button data-del="${esc(m.file)}">Rimuovi</button></td></tr>`).join("");
  el.innerHTML = `
    <div class="card">
      <h2 style="margin-top:0">Carica materiali del docente</h2>
      <p class="muted small">PDF, PPTX, DOCX, TXT/MD. Il testo viene estratto e dato al tutor e al generatore di esercizi. Collega il file all'argomento del syllabus giusto, così compare negli appunti di quella lezione.</p>
      <form id="up" class="upload-form">
        <label>File <input type="file" name="files" multiple required accept=".pdf,.pptx,.docx,.txt,.md,.csv"></label>
        <label>Tipo <select name="kind">${Object.entries(KIND_LABEL).map(([k, v]) => `<option value="${k}">${v}</option>`).join("")}</select></label>
        <label style="grid-column:1/-1">Argomento del syllabus <select name="topic"><option value="">Generale (tutto il corso)</option>
          ${data.topics.filter((t) => t.n).map((t) => `<option value="${t.n}">${t.n}. ${esc(t.title)}${t.status === "done" ? " (già superato)" : ""}</option>`).join("")}</select></label>
        <div><button class="primary" type="submit">Carica</button> <span id="up-status" class="muted small"></span></div>
      </form>
    </div>
    <h2>Materiali caricati (${data.materials.length})</h2>
    <div class="card" style="padding:0;overflow-x:auto">${data.materials.length
      ? `<table class="materials-table"><tr><th>File</th><th>Tipo</th><th>Argomento</th><th>Testo</th><th></th></tr>${rows}</table>`
      : `<p style="padding:16px" class="muted">Nessun materiale ancora.</p>`}</div>`;
  document.getElementById("up").onsubmit = async (e) => {
    e.preventDefault();
    const status = document.getElementById("up-status");
    status.textContent = "Caricamento ed estrazione del testo…";
    try {
      const r = await api(`/api/courses/${id}/materials`, { method: "POST", body: new FormData(e.target) });
      status.textContent = `Caricati ${r.added.length} file.`;
      route();
    } catch (err) { status.textContent = err.message; }
  };
  el.querySelectorAll("button[data-del]").forEach((b) => (b.onclick = async () => {
    if (!confirm(`Rimuovere ${b.dataset.del}?`)) return;
    await api(`/api/courses/${id}/materials/${encodeURIComponent(b.dataset.del)}`, { method: "DELETE" });
    route();
  }));
}
