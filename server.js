// Agenda di studio — server Express.
// Serve il frontend (public/), i contenuti dei corsi (content/), i materiali caricati (materiali/)
// e fa da proxy verso Claude per il tutor, la correzione delle risposte aperte e la generazione di esercizi.
import express from "express";
import multer from "multer";
import fs from "node:fs/promises";
import { existsSync, mkdirSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import Anthropic from "@anthropic-ai/sdk";
import { extractText, getDocumentProxy } from "unpdf";
import JSZip from "jszip";

const ROOT = path.dirname(fileURLToPath(import.meta.url));
const CONTENT = path.join(ROOT, "content");
const MATERIALS = path.join(ROOT, "materiali");
const DATA = path.join(ROOT, "data");
const PROGRESS_FILE = path.join(DATA, "progress.json");
const PORT = Number(process.env.PORT) || 3000;
const MODEL = process.env.CLAUDE_MODEL || "claude-opus-5-5";
// Limite di caratteri di materiali (slide, note, casi) inviati al tutor per ogni richiesta.
const MATERIAL_CHAR_BUDGET = Number(process.env.MATERIAL_CHAR_BUDGET) || 400_000;

for (const dir of [DATA, MATERIALS]) if (!existsSync(dir)) mkdirSync(dir, { recursive: true });

const hasKey = Boolean(process.env.ANTHROPIC_API_KEY || process.env.ANTHROPIC_AUTH_TOKEN);
const client = new Anthropic();

// ---------- util ----------
const safeId = (s) => /^[a-z0-9-]+$/.test(s);
const safeFile = (s) => /^[\w.\-() ]+$/.test(s) && !s.includes("..");

async function readJSON(file, fallback) {
  try {
    return JSON.parse(await fs.readFile(file, "utf8"));
  } catch {
    return fallback;
  }
}
async function writeJSON(file, value) {
  await fs.mkdir(path.dirname(file), { recursive: true });
  await fs.writeFile(file, JSON.stringify(value, null, 2));
}

function parseFrontmatter(md) {
  const m = md.match(/^---\n([\s\S]*?)\n---\n?/);
  if (!m) return { meta: {}, body: md };
  const meta = {};
  for (const line of m[1].split("\n")) {
    const i = line.indexOf(":");
    if (i > 0) meta[line.slice(0, i).trim()] = line.slice(i + 1).trim();
  }
  return { meta, body: md.slice(m[0].length) };
}

async function listCourseIds() {
  const entries = await fs.readdir(CONTENT, { withFileTypes: true });
  return entries.filter((e) => e.isDirectory() && existsSync(path.join(CONTENT, e.name, "course.json"))).map((e) => e.name);
}

async function loadCourse(id) {
  if (!safeId(id)) return null;
  const course = await readJSON(path.join(CONTENT, id, "course.json"), null);
  if (!course) return null;
  const quiz = await readJSON(path.join(CONTENT, id, "quiz.json"), {});
  const generated = await readJSON(path.join(DATA, "generated-quiz", `${id}.json`), {});
  const lecturesDir = path.join(CONTENT, id, "lectures");
  const lectures = {};
  for (const file of existsSync(lecturesDir) ? await fs.readdir(lecturesDir) : []) {
    if (!file.endsWith(".md")) continue;
    const { meta, body } = parseFrontmatter(await fs.readFile(path.join(lecturesDir, file), "utf8"));
    lectures[file] = {
      file,
      title: meta.title || file,
      date: meta.date || "",
      wispr: meta.wispr || "",
      body,
      quizCount: (quiz[file]?.length || 0) + (generated[file]?.length || 0),
    };
  }
  const materials = await readJSON(path.join(MATERIALS, id, "index.json"), []);
  return { course, quiz, generated, lectures, materials };
}

// ---------- progresso ----------
// Ogni lezione: studied (letta e capita) + bestScore del quiz (0..1).
// Punteggio lezione = 30% "studiata" + 70% miglior punteggio quiz (se la lezione ha un quiz).
// Punteggio argomento = media delle sue lezioni; un argomento senza lezioni vale "studiato" manuale (0 o 1).
// Percentuale materia = media sugli argomenti che contano per l'esame (status != done, kind lesson/guest).
function lectureScore(p, hasQuiz) {
  if (!p) return 0;
  const studied = p.studied ? 1 : 0;
  if (!hasQuiz) return studied;
  return 0.3 * studied + 0.7 * (p.bestScore || 0);
}

function countsForExam(topic) {
  return topic.status !== "done" && (topic.kind === "lesson" || topic.kind === "guest");
}

function computeProgress(loaded, progress) {
  const { course, lectures } = loaded;
  const cp = progress.courses?.[course.id] || {};
  const lp = cp.lectures || {};
  const tp = cp.topics || {};
  const today = new Date().toISOString().slice(0, 10);
  const topics = course.topics.map((t) => {
    let score;
    if (t.lectures.length) {
      score = t.lectures.reduce((s, f) => s + lectureScore(lp[f], (lectures[f]?.quizCount || 0) > 0), 0) / t.lectures.length;
    } else {
      score = tp[t.n]?.studied ? 1 : 0;
    }
    return { ...t, score, counts: countsForExam(t), held: !t.date || t.date <= today };
  });
  const counted = topics.filter((t) => t.counts);
  const percent = counted.length ? Math.round((100 * counted.reduce((s, t) => s + t.score, 0)) / counted.length) : 0;
  const heldCount = counted.filter((t) => t.held && t.date).length;
  const recorded = counted.filter((t) => t.lectures.length).length;
  return {
    topics,
    percent,
    totalTopics: counted.length,
    heldTopics: heldCount,
    recordedTopics: recorded,
    examDate: cp.examDate ?? course.exam?.date ?? "",
  };
}

// ---------- app ----------
const app = express();
app.use(express.json({ limit: "2mb" }));
app.use(express.static(path.join(ROOT, "public")));
app.use("/vendor/marked", express.static(path.join(ROOT, "node_modules", "marked", "lib")));
app.use("/materiali", express.static(MATERIALS));

app.get("/api/status", (_req, res) => res.json({ ai: hasKey, model: MODEL }));

app.get("/api/courses", async (_req, res) => {
  const progress = await readJSON(PROGRESS_FILE, {});
  const out = [];
  for (const id of await listCourseIds()) {
    const loaded = await loadCourse(id);
    const p = computeProgress(loaded, progress);
    const c = loaded.course;
    out.push({
      id: c.id,
      name: c.name,
      short: c.short,
      color: c.color,
      order: c.order ?? 99,
      scope: c.scope,
      exam: { ...c.exam, date: p.examDate },
      percent: p.percent,
      totalTopics: p.totalTopics,
      heldTopics: p.heldTopics,
      recordedTopics: p.recordedTopics,
      lectureCount: Object.keys(loaded.lectures).length,
      materialCount: loaded.materials.length,
    });
  }
  out.sort((a, b) => a.order - b.order);
  res.json(out);
});

app.get("/api/courses/:id", async (req, res) => {
  const loaded = await loadCourse(req.params.id);
  if (!loaded) return res.status(404).json({ error: "Materia non trovata" });
  const progress = await readJSON(PROGRESS_FILE, {});
  const p = computeProgress(loaded, progress);
  const cp = progress.courses?.[loaded.course.id] || {};
  const lectures = Object.fromEntries(
    Object.entries(loaded.lectures).map(([f, l]) => [f, { ...l, body: undefined, progress: cp.lectures?.[f] || {} }]),
  );
  res.json({
    course: { ...loaded.course, exam: { ...loaded.course.exam, date: p.examDate } },
    topics: p.topics,
    percent: p.percent,
    lectures,
    materials: loaded.materials,
    topicProgress: cp.topics || {},
  });
});

app.get("/api/courses/:id/lectures/:file", async (req, res) => {
  const loaded = await loadCourse(req.params.id);
  const lec = loaded?.lectures[req.params.file];
  if (!lec) return res.status(404).json({ error: "Lezione non trovata" });
  const topic = loaded.course.topics.find((t) => t.lectures.includes(lec.file));
  const materials = loaded.materials.filter((m) => topic && m.topic === topic.n);
  res.json({ ...lec, topic: topic || null, materials });
});

app.get("/api/courses/:id/quiz/:file", async (req, res) => {
  const loaded = await loadCourse(req.params.id);
  if (!loaded) return res.status(404).json({ error: "Materia non trovata" });
  const f = req.params.file;
  res.json([...(loaded.quiz[f] || []), ...(loaded.generated[f] || []).map((q) => ({ ...q, generated: true }))]);
});

// Aggiorna il progresso: { lecture?, topic?, studied?, quizScore?, examDate? }
app.post("/api/courses/:id/progress", async (req, res) => {
  const loaded = await loadCourse(req.params.id);
  if (!loaded) return res.status(404).json({ error: "Materia non trovata" });
  const progress = await readJSON(PROGRESS_FILE, {});
  progress.courses ??= {};
  const cp = (progress.courses[loaded.course.id] ??= { lectures: {}, topics: {} });
  cp.lectures ??= {};
  cp.topics ??= {};
  const { lecture, topic, studied, quizScore, examDate, wrong } = req.body || {};
  if (typeof examDate === "string") cp.examDate = examDate;
  if (lecture && loaded.lectures[lecture]) {
    const lp = (cp.lectures[lecture] ??= {});
    if (typeof studied === "boolean") lp.studied = studied;
    if (typeof quizScore === "number") {
      lp.bestScore = Math.max(lp.bestScore || 0, Math.min(1, Math.max(0, quizScore)));
      lp.attempts = (lp.attempts || 0) + 1;
      lp.lastScore = quizScore;
      lp.lastAttempt = new Date().toISOString();
      if (Array.isArray(wrong)) lp.wrong = wrong.slice(0, 50); // domande sbagliate, per il ripasso
    }
  }
  if (topic !== undefined && typeof studied === "boolean") {
    cp.topics[topic] = { ...(cp.topics[topic] || {}), studied };
  }
  await writeJSON(PROGRESS_FILE, progress);
  res.json({ ok: true });
});

// ---------- materiali (slide, note del docente, casi) ----------
async function extractMaterialText(filePath, original) {
  const ext = path.extname(original).toLowerCase();
  const buf = await fs.readFile(filePath);
  if (ext === ".pdf") {
    const pdf = await getDocumentProxy(new Uint8Array(buf));
    const { text } = await extractText(pdf, { mergePages: false });
    return text.map((t, i) => `[Pagina ${i + 1}]\n${t}`).join("\n\n");
  }
  if (ext === ".pptx") {
    const zip = await JSZip.loadAsync(buf);
    const slides = Object.keys(zip.files)
      .filter((n) => /^ppt\/slides\/slide\d+\.xml$/.test(n))
      .sort((a, b) => Number(a.match(/\d+/)[0]) - Number(b.match(/\d+/)[0]));
    const out = [];
    for (const [i, name] of slides.entries()) {
      const xml = await zip.file(name).async("string");
      const text = [...xml.matchAll(/<a:t>([^<]*)<\/a:t>/g)].map((m) => m[1]).join(" ");
      const notesName = name.replace("slides/slide", "notesSlides/notesSlide");
      let notes = "";
      if (zip.file(notesName)) {
        const nx = await zip.file(notesName).async("string");
        notes = [...nx.matchAll(/<a:t>([^<]*)<\/a:t>/g)].map((m) => m[1]).join(" ");
      }
      out.push(`[Slide ${i + 1}]\n${text}${notes ? `\nNote: ${notes}` : ""}`);
    }
    return out.join("\n\n");
  }
  if (ext === ".docx") {
    const zip = await JSZip.loadAsync(buf);
    const xml = (await zip.file("word/document.xml")?.async("string")) || "";
    return xml.replace(/<\/w:p>/g, "\n").replace(/<[^>]+>/g, "");
  }
  if ([".txt", ".md", ".csv"].includes(ext)) return buf.toString("utf8");
  return "";
}

const upload = multer({
  storage: multer.diskStorage({
    destination: (req, _file, cb) => {
      const dir = path.join(MATERIALS, req.params.id);
      mkdirSync(dir, { recursive: true });
      cb(null, dir);
    },
    filename: (_req, file, cb) => {
      const name = Buffer.from(file.originalname, "latin1").toString("utf8").replace(/[^\w.\-() ]+/g, "_");
      cb(null, name);
    },
  }),
  limits: { fileSize: 80 * 1024 * 1024 },
});

app.post("/api/courses/:id/materials", (req, res, next) => {
  if (!safeId(req.params.id) || !existsSync(path.join(CONTENT, req.params.id))) return res.status(404).json({ error: "Materia non trovata" });
  next();
}, upload.array("files", 20), async (req, res) => {
  const id = req.params.id;
  const indexFile = path.join(MATERIALS, id, "index.json");
  const index = await readJSON(indexFile, []);
  const topic = req.body.topic ? Number(req.body.topic) : null;
  const kind = ["slides", "notes", "case", "reading", "exercises", "other"].includes(req.body.kind) ? req.body.kind : "other";
  const added = [];
  for (const f of req.files || []) {
    let text = "";
    try {
      text = await extractMaterialText(f.path, f.filename);
    } catch (e) {
      console.warn("Estrazione testo fallita per", f.filename, e.message);
    }
    const textFile = path.join(MATERIALS, id, ".text", `${f.filename}.txt`);
    await fs.mkdir(path.dirname(textFile), { recursive: true });
    await fs.writeFile(textFile, text);
    const entry = { file: f.filename, kind, topic, size: f.size, chars: text.length, uploadedAt: new Date().toISOString() };
    const i = index.findIndex((m) => m.file === f.filename);
    if (i >= 0) index[i] = entry;
    else index.push(entry);
    added.push(entry);
  }
  await writeJSON(indexFile, index);
  res.json({ added });
});

app.delete("/api/courses/:id/materials/:file", async (req, res) => {
  const { id, file } = req.params;
  if (!safeId(id) || !safeFile(file)) return res.status(400).json({ error: "Nome non valido" });
  const indexFile = path.join(MATERIALS, id, "index.json");
  const index = (await readJSON(indexFile, [])).filter((m) => m.file !== file);
  await writeJSON(indexFile, index);
  await fs.rm(path.join(MATERIALS, id, file), { force: true });
  await fs.rm(path.join(MATERIALS, id, ".text", `${file}.txt`), { force: true });
  res.json({ ok: true });
});

// ---------- contesto per Claude ----------
async function buildContext(loaded, lectureFile) {
  const { course, lectures, materials } = loaded;
  const focusTopic = lectureFile ? course.topics.find((t) => t.lectures.includes(lectureFile)) : null;

  const syllabus = course.topics
    .map((t) => `${t.n}. [${t.date || "data n.d."}] ${t.title}${t.status === "done" ? " (GIÀ SUPERATO, fuori programma d'esame)" : ""}${t.kind !== "lesson" ? ` (${t.kind})` : ""}`)
    .join("\n");

  const notes = Object.values(lectures)
    .sort((a, b) => a.file.localeCompare(b.file))
    .map((l) => `<lecture file="${l.file}" title="${l.title}" date="${l.date}">\n${l.body}\n</lecture>`)
    .join("\n\n");

  // Materiali: prima quelli dell'argomento in focus, poi gli altri, fino al budget di caratteri.
  const ordered = [...materials].sort((a, b) => (b.topic === focusTopic?.n) - (a.topic === focusTopic?.n));
  let budget = MATERIAL_CHAR_BUDGET;
  const parts = [];
  const skipped = [];
  for (const m of ordered) {
    const text = await fs.readFile(path.join(MATERIALS, course.id, ".text", `${m.file}.txt`), "utf8").catch(() => "");
    if (!text) continue;
    if (text.length > budget) {
      skipped.push(m.file);
      continue;
    }
    budget -= text.length;
    parts.push(`<material file="${m.file}" kind="${m.kind}" topic="${m.topic ?? "generale"}">\n${text}\n</material>`);
  }

  const stable = `Materia: ${course.name} (${course.code}) — docenti: ${course.professors}
Ambito di studio: ${course.scope}
Esame: ${course.exam?.label} — ${course.exam?.format}
Valutazione: ${(course.assessment || []).join("; ")}

<syllabus>
${syllabus}
</syllabus>

<appunti_lezioni fonte="registrazioni Wispr Flow (riassunti delle trascrizioni)">
${notes}
</appunti_lezioni>

<materiali_docenti fonte="slide, student notes, casi e letture caricati dallo studente">
${parts.join("\n\n") || "(nessun materiale caricato per ora)"}
</materiali_docenti>${skipped.length ? `\n(Materiali non inclusi per limiti di lunghezza: ${skipped.join(", ")})` : ""}`;

  return { stable, focusTopic, focusLecture: lectureFile ? lectures[lectureFile] : null };
}

const TUTOR_INSTRUCTIONS = `Sei il tutor personale di Francesco, studente del master INTENT/EMIT in Bocconi, che si sta preparando agli esami.
Rispondi in italiano (mantieni in inglese i termini tecnici usati nel corso, perché le lezioni e l'esame sono in inglese).
Basati prima di tutto sugli appunti delle lezioni e sui materiali dei docenti forniti qui sotto; quando qualcosa viene da lì, indica la fonte (es. "slide 12 di …", "lezione del 29-10"). Se aggiungi conoscenze generali che non sono nel materiale del corso, dillo esplicitamente, così Francesco sa cosa è "da esame" e cosa no.
Le note Wispr sono riassunti automatici di registrazioni: possono contenere nomi trascritti male; se noti un'incongruenza segnalala.
Spiega in modo chiaro e ordinato: prima l'intuizione, poi la definizione precisa, poi un esempio (meglio se preso dai casi del corso). Per gli esercizi numerici mostra tutti i passaggi.
Se lo studente sbaglia, correggilo con gentilezza ma senza ambiguità. Quando è utile, chiudi con una breve domanda di verifica per controllare che abbia capito.`;

function systemBlocks(stable) {
  return [
    { type: "text", text: TUTOR_INSTRUCTIONS },
    { type: "text", text: stable, cache_control: { type: "ephemeral", ttl: "1h" } },
  ];
}

// Opzioni comuni: fallback lato server sui rifiuti dei classificatori di sicurezza.
const FALLBACK = { betas: ["server-side-fallback-2026-07-01"], fallbacks: "default" };

function requireAI(res) {
  if (hasKey) return false;
  res.status(503).json({ error: "Manca ANTHROPIC_API_KEY: avvia il server con la tua chiave API per usare il tutor (vedi README)." });
  return true;
}

// ---------- tutor (streaming SSE) ----------
app.post("/api/courses/:id/chat", async (req, res) => {
  if (requireAI(res)) return;
  const loaded = await loadCourse(req.params.id);
  if (!loaded) return res.status(404).json({ error: "Materia non trovata" });
  const { lecture, messages } = req.body || {};
  if (!Array.isArray(messages) || !messages.length) return res.status(400).json({ error: "Nessun messaggio" });

  const { stable, focusTopic, focusLecture } = await buildContext(loaded, lecture);
  const history = messages
    .filter((m) => (m.role === "user" || m.role === "assistant") && typeof m.content === "string" && m.content.trim())
    .slice(-30)
    .map((m) => ({ role: m.role, content: m.content }));
  if (focusLecture && history.length) {
    const first = history[0];
    if (first.role === "user") {
      history[0] = {
        role: "user",
        content: `[Sto studiando la lezione "${focusLecture.title}" (${focusLecture.date}), argomento del syllabus n. ${focusTopic?.n}: ${focusTopic?.title}]\n\n${first.content}`,
      };
    }
  }

  res.writeHead(200, { "Content-Type": "text/event-stream", "Cache-Control": "no-cache", Connection: "keep-alive" });
  const send = (obj) => res.write(`data: ${JSON.stringify(obj)}\n\n`);
  try {
    const stream = client.beta.messages.stream({
      model: MODEL,
      max_tokens: 16000,
      ...FALLBACK,
      output_config: { effort: "medium" },
      system: systemBlocks(stable),
      messages: history,
    });
    req.on("close", () => stream.abort());
    for await (const event of stream) {
      if (event.type === "content_block_delta" && event.delta.type === "text_delta") send({ text: event.delta.text });
    }
    const final = await stream.finalMessage();
    if (final.stop_reason === "refusal") send({ error: "La richiesta è stata rifiutata dal modello. Prova a riformularla." });
    send({ done: true });
  } catch (e) {
    console.error("chat error", e);
    send({ error: e instanceof Anthropic.APIError ? `Errore API (${e.status}): ${e.message}` : String(e.message || e) });
  }
  res.end();
});

// Richiesta JSON strutturata (correzione / generazione domande).
async function structured(stable, prompt, schema, effort = "medium") {
  const msg = await client.beta.messages.create({
    model: MODEL,
    max_tokens: 16000,
    ...FALLBACK,
    output_config: { effort, format: { type: "json_schema", schema } },
    system: systemBlocks(stable),
    messages: [{ role: "user", content: prompt }],
  });
  if (msg.stop_reason === "refusal") throw new Error("Richiesta rifiutata dal modello");
  const text = msg.content.filter((b) => b.type === "text").map((b) => b.text).join("");
  return JSON.parse(text);
}

// ---------- correzione risposte aperte ----------
app.post("/api/courses/:id/grade", async (req, res) => {
  if (requireAI(res)) return;
  const loaded = await loadCourse(req.params.id);
  if (!loaded) return res.status(404).json({ error: "Materia non trovata" });
  const { lecture, question, modelAnswer, userAnswer } = req.body || {};
  if (!question || typeof userAnswer !== "string") return res.status(400).json({ error: "Dati mancanti" });
  const { stable } = await buildContext(loaded, lecture);
  try {
    const result = await structured(
      stable,
      `Correggi la risposta dello studente a una domanda di esercizio, come farebbe il docente all'esame.
Domanda: ${question}
Traccia di risposta attesa: ${modelAnswer || "(nessuna: usa il materiale del corso)"}
Risposta dello studente: ${userAnswer || "(vuota)"}

Assegna un punteggio da 0 a 1 (1 = risposta completa e corretta, 0.5 = parziale, 0 = sbagliata o assente). Nel feedback (in italiano, conciso) di' cosa è corretto, cosa manca o è sbagliato e come migliorarla.`,
      {
        type: "object",
        properties: {
          score: { type: "number", description: "Punteggio tra 0 e 1" },
          feedback: { type: "string" },
          missing: { type: "array", items: { type: "string" }, description: "Concetti chiave mancanti" },
        },
        required: ["score", "feedback", "missing"],
        additionalProperties: false,
      },
      "low",
    );
    result.score = Math.min(1, Math.max(0, Number(result.score) || 0));
    res.json(result);
  } catch (e) {
    console.error("grade error", e);
    res.status(500).json({ error: String(e.message || e) });
  }
});

// ---------- nuove domande generate ----------
app.post("/api/courses/:id/generate-quiz", async (req, res) => {
  if (requireAI(res)) return;
  const loaded = await loadCourse(req.params.id);
  const { lecture, count = 5 } = req.body || {};
  if (!loaded?.lectures[lecture]) return res.status(404).json({ error: "Lezione non trovata" });
  const { stable } = await buildContext(loaded, lecture);
  const existing = [...(loaded.quiz[lecture] || []), ...(loaded.generated[lecture] || [])].map((q) => `- ${q.q}`).join("\n");
  try {
    const result = await structured(
      stable,
      `Crea ${Math.min(10, Math.max(1, Number(count) || 5))} nuove domande di esercizio sulla lezione "${loaded.lectures[lecture].title}" (file ${lecture}), utili a capire se lo studente è davvero pronto per l'esame (${loaded.course.exam?.format}).
Usa sia gli appunti della lezione sia gli eventuali materiali dei docenti dello stesso argomento. Mescola domande a scelta multipla (anche con più risposte corrette, indicate in "answer" come indici a partire da 0) e domande aperte o esercizi numerici ("type": "open", con traccia di risposta in "model_answer"). Per le domande a scelta multipla usa "explain" per spiegare la soluzione. Scrivi in italiano mantenendo i termini tecnici in inglese.
Non ripetere queste domande già presenti:
${existing || "(nessuna)"}`,
      {
        type: "object",
        properties: {
          questions: {
            type: "array",
            items: {
              type: "object",
              properties: {
                type: { type: "string", enum: ["mc", "open"] },
                q: { type: "string" },
                options: { type: "array", items: { type: "string" } },
                answer: { type: "array", items: { type: "integer" } },
                explain: { type: "string" },
                model_answer: { type: "string" },
              },
              required: ["type", "q", "options", "answer", "explain", "model_answer"],
              additionalProperties: false,
            },
          },
        },
        required: ["questions"],
        additionalProperties: false,
      },
      "medium",
    );
    const questions = result.questions
      .filter((q) => q.q && (q.type === "open" || (q.options.length >= 2 && q.answer.length && q.answer.every((i) => i >= 0 && i < q.options.length))))
      .map((q) => (q.type === "mc" ? { type: "mc", q: q.q, options: q.options, answer: q.answer, explain: q.explain } : { type: "open", q: q.q, answer: q.model_answer }));
    const file = path.join(DATA, "generated-quiz", `${loaded.course.id}.json`);
    const all = await readJSON(file, {});
    all[lecture] = [...(all[lecture] || []), ...questions];
    await writeJSON(file, all);
    res.json({ added: questions.length });
  } catch (e) {
    console.error("generate error", e);
    res.status(500).json({ error: String(e.message || e) });
  }
});

app.listen(PORT, () => {
  console.log(`Agenda di studio pronta su http://localhost:${PORT}`);
  if (!hasKey) console.log("Attenzione: ANTHROPIC_API_KEY non impostata — tutor, correzione e generazione domande sono disattivati.");
});
