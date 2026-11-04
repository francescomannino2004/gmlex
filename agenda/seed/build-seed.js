// Builds the initial database rows (courses, lessons, settings) from the five syllabi.
// Usage: node build-seed.js <outdir>  → writes batch-N.json files of {op,collection,doc_id,data}.
const fs = require('fs'), path = require('path');
const out = process.argv[2] || path.join(__dirname, 'out');
fs.mkdirSync(out, { recursive: true });
const base = { level: 'todo', rstep: 0, nextReview: null, notes: 'none', readings: [], caseStudy: '', instructor: '' };

const courses = {
  cvis: { name: 'Corporate Venturing and Innovation Strategy', short: 'CVIS', code: '21074', color: '#4F5BD5', examDate: '2026-12-11', examTentative: true, attending: true,
    format: 'Scritto individuale con domande aperte e/o chiuse (50% del voto) · dettagli ancora da comunicare', examMinutes: 75, examQuestions: 15, examTypes: ['open', 'mc'],
    examNotes: "Frequentanti: partecipazione 30% · group work 20% · scritto 50%. Materiale d'esame: handouts, i 10 casi, O'Reilly & Tushman (2008). Shane (2009) solo consigliato, non in esame. Appello del syllabus: 11 dicembre (poi 25 gennaio). Durata e numero di domande sono stime da aggiornare.",
    start: { mode: 'now' } },
  vc: { name: 'Venture Capital and Valuation', short: 'VC', code: '20453', color: '#1E8A5A', examDate: '2026-12-21', examTentative: false, attending: true,
    format: 'Secondo parziale: multiple choice con esercizi numerici e mini-casi (solo Parte Three)', examMinutes: 60, examQuestions: 30, examTypes: ['mc', 'num'],
    examNotes: 'Primo parziale (Parti One e Two) già superato con 30 e lode. Il secondo parziale copre solo la Parte Three (lezioni 13–24, prof.ssa Zava) e vale il 50%. Durata e numero di domande sono stime da aggiornare.',
    start: { mode: 'now' } },
  da: { name: 'Data Analysis Module I (Data Lab for Entrepreneurship)', short: 'Data', code: '21072', color: '#B7740A', examDate: '2027-01-07', examTentative: false, attending: false,
    format: 'Non frequentante: scritto da 2,5 h con domande aperte, chiuse e multiple choice (100% del voto)', examMinutes: 150, examQuestions: 25, examTypes: ['mc', 'num', 'open'],
    examNotes: "Non frequentante: solo esame scritto (100%), 2,5 ore, su Blackboard con Respondus Lockdown. Focus su tecniche econometriche e loro applicazione a dati reali. Materiali: notebook Jupyter (Parte I), slide e paper (Parte II); Molin (2021) cap. 1–4 facoltativo; Hill, Griffiths & Lim (2018) capitoli selezionati.",
    start: { mode: 'now' } },
  ent: { name: 'The Emergence of Entrepreneurial Ventures', short: 'Entrep', code: '21077', color: '#B8327A', examDate: '2027-01-15', examTentative: false, attending: true,
    format: 'Scritto individuale con domande aperte e chiuse, 30 punti (60% del voto)', examMinutes: 90, examQuestions: 15, examTypes: ['open', 'mc'],
    examNotes: 'Frequentanti: scritto 60% · group project (memo) 40% · partecipazione fino a +1. Domande d’esempio discusse in classe e su Blackboard. Testo di supporto: Gans, Scott & Stern, Entrepreneurship: Choice and Strategy (2024). Durata e numero di domande sono stime.',
    start: { mode: 'now' } },
  ip: { name: 'Intellectual Property Law for Business', short: 'IP Law', code: '21070', color: '#127C8C', examDate: '2027-01-18', examTentative: false, attending: true,
    format: 'Domande aperte (dettagli ancora da comunicare)', examMinutes: 90, examQuestions: 5, examTypes: ['open'],
    examNotes: 'Appunti costruiti da: pagine del libro indicate per ogni lezione + slide + registrazione del professore. Il PDF del syllabus si interrompe a pagina 13: modalità d’esame e lezione 19 da completare.',
    start: { mode: 'now' } },
};

const L = [];
const add = (courseId, n, date, title, o = {}) => L.push({ id: `${courseId}-${String(n).padStart(2, '0')}`, data: { ...base, courseId, n, date, title, kind: 'lesson', inExam: true, ...o } });

// ---- CVIS (class 27) ----
const shane = c => `Shane S.A. (2009), Technology Strategy for Managers and Entrepreneurs, ${c} (consigliato, non in esame)`;
add('cvis', 1, '2026-09-08', 'Industrial Revolutions and the emerging AI revolution', { instructor: 'Verona & Mignini', readings: [
  'Schumpeter J., The Theory of Economic Development — https://cruel.org/books/hy/shortschumpeter/SchumpeterTheoryofEconDev.pdf',
  'Dosi G. (1982), Research Policy — http://sjbae.pbworks.com/w/file/fetch/38055602/dosi_1982.pdf'] });
add('cvis', 2, '2026-09-10', 'From Theory to Practice: Why Innovation and Corporate Entrepreneurship are Crucial', { instructor: 'Verona', readings: [
  'McKinsey, State of AI trust in 2026: shifting to the agentic era — https://www.mckinsey.com/capabilities/tech-and-ai/our-insights/tech-forward/state-of-ai-trust-in-2026-shifting-to-the-agentic-era',
  'Mokyr J., Vickers C. & Ziebarth N.L., Journal of Economic Perspectives — https://pubs.aeaweb.org/doi/pdfplus/10.1257/jep.29.3.31',
  'Draghi M., The future of European competitiveness — https://commission.europa.eu/document/download/97e481fd-2dc3-412d-be4c-f152a8232961_en?filename=The%20future%20of%20European%20competitiveness%20_%20A%20competitiveness%20strategy%20for%20Europe.pdf'] });
add('cvis', 3, '2026-09-15', 'Corporate R&D', { instructor: 'Verona', caseStudy: 'Strategy in the twenty-first century pharmaceutical industry: Merck & Co. and Pfizer Inc. [HBS 9707509]', readings: [
  'Case: Merck & Co. and Pfizer Inc. [HBS 9707509]',
  'Arora A. et al., Strategic Management Journal — https://sms.onlinelibrary.wiley.com/doi/full/10.1002/smj.2693', shane('Chapter 4')] });
add('cvis', 4, '2026-09-17', 'Emergence of Dominant Designs', { instructor: 'Verona', caseStudy: 'Responding to the Wii? [HBS 9709448]', readings: [
  'Case: Responding to the Wii? [HBS 9709448]',
  'Abernathy W.J. & Utterback J.M. (1978), MIT Review — https://teaching.up.edu/bus580/bps/Abernathy%20and%20Utterback%2C%201978.pdf', shane('Chapter 2')] });
add('cvis', 5, '2026-09-22', 'The role of demand: Adoption dynamics and Lead Users', { instructor: 'Verona', readings: [
  'Von Hippel E., Democratizing Innovation — https://web.mit.edu/evhippel/www/books/DI/DemocInn.pdf', shane('Chapter 3')] });
add('cvis', 6, '2026-09-24', 'Inertia of competences, organizations, and industrial systems', { instructor: 'Verona', caseStudy: 'Kodak and the digital revolution (A) [HBS 9705448]', readings: [
  'Case: Kodak and the digital revolution (A) [HBS 9705448]',
  'Christensen C.M., The Innovator’s Dilemma — https://rudyct.com/InovBis/The%20Innovator%E2%80%99s%20Dilemma%20(Clayton%20M.%20Christensen)2000.pdf'] });
add('cvis', 7, '2026-09-29', 'Group work kick-off', { kind: 'group', inExam: false, instructor: 'Mignini' });
add('cvis', 8, '2026-10-01', 'Guest Speaker', { kind: 'guest', inExam: false, instructor: 'Verona' });
add('cvis', 9, '2026-10-06', 'Ambidexterity and Corporate venturing and development', { instructor: 'Verona', caseStudy: 'SNAM Case [SDA Bocconi]', readings: [
  'Case: SNAM [SDA Bocconi]', 'Tushman M. et al., Industrial and Corporate Change — https://academic.oup.com/icc/article-abstract/19/5/1331/783939'] });
add('cvis', 10, '2026-10-08', 'Group work check', { kind: 'group', inExam: false, instructor: 'Mignini' });
add('cvis', 11, '2026-10-13', 'Building the agile organization', { instructor: 'Verona', caseStudy: 'Leadership Online (A): Barnes & Noble vs. Amazon.com [HBS 9798063]', readings: [
  'Case: Leadership Online (A): Barnes & Noble vs. Amazon.com [HBS 9798063]',
  'Teece D.J. et al. (1997), Strategic Management Journal — https://sms.onlinelibrary.wiley.com/doi/abs/10.1002/%28SICI%291097-0266%28199708%2918%3A7%3C509%3A%3AAID-SMJ882%3E3.0.CO%3B2-Z',
  "O'Reilly C.A. & Tushman M. (2008), Ambidexterity as a dynamic capability, Research in Organizational Behavior (in esame) — https://papers.ssrn.com/sol3/papers.cfm?abstract_id=978493"] });
add('cvis', 12, '2026-10-15', 'Guest Speaker', { kind: 'guest', inExam: false, instructor: 'Verona' });
add('cvis', 13, '2026-10-29', 'Sustaining Innovation', { instructor: 'Mignini', caseStudy: 'Red Bull (A) [HBS 9714401]', readings: ['Case: Red Bull (A) [HBS 9714401]', shane('Chapter 10')] });
add('cvis', 14, '2026-11-03', 'Delivering Innovation', { instructor: 'Mignini', caseStudy: 'Tesla, Inc. [MH 0067]', readings: ['Case: Tesla, Inc. [MH 0067]', shane('Chapter 7')] });
add('cvis', 15, '2026-11-05', 'Group work check', { kind: 'group', inExam: false, instructor: 'Mignini' });
add('cvis', 16, '2026-11-10', 'Make or Buy?', { instructor: 'Mignini', caseStudy: 'The Walt Disney Company and Pixar Inc: To acquire or not to acquire? [HBS 9709462]', readings: ['Case: Disney and Pixar [HBS 9709462]', shane('Chapters 3 and 4')] });
add('cvis', 17, '2026-11-12', 'Open Innovation', { instructor: 'Mignini', caseStudy: 'Lego (A): The crisis [HBS 9713478]', readings: ['Case: Lego (A): The crisis [HBS 9713478]',
  'Chesbrough H.W., Open Innovation — https://books.google.com/books/about/Open_Innovation.html?id=4hTRWStFhVgC', shane('Chapter 14')] });
add('cvis', 18, '2026-11-17', 'Market creation', { instructor: 'Mignini', caseStudy: '$19B 4 txt app WhatsApp… omg! [HBS 9715441]', readings: ['Case: $19B 4 txt app WhatsApp… omg! [HBS 9715441]', shane('Chapter 10')] });
add('cvis', 19, '2026-11-17', 'Group work check', { kind: 'group', inExam: false, instructor: 'Mignini' });
add('cvis', 20, '2026-11-24', 'Creativity and Watches', { instructor: 'Mignini', readings: ['Raffaelli R., Administrative Science Quarterly — https://www.jstor.org/stable/48589581'] });
add('cvis', 21, '2026-11-26', 'Guest Speaker', { kind: 'guest', inExam: false, instructor: 'Mignini' });
add('cvis', 22, '2026-12-01', 'Group work presentations', { kind: 'group', inExam: false, instructor: 'Verona & Mignini' });
add('cvis', 23, '2026-12-01', 'Group work presentations', { kind: 'group', inExam: false, instructor: 'Verona & Mignini' });
add('cvis', 24, '2026-12-03', 'Wrap up and takeaways', { instructor: 'Verona & Mignini' });

// ---- VC (class 27): only Part Three is in the second mid-term ----
const vc = [
  ['Course start up: rules of thumb and general overview', 'Gigante'], ['The fundamentals of venture capital: definition and main schemes', 'Gigante'],
  ['Venture Capital Clusters: seed, start-up, and early stage', 'Gigante'], ['VC Investors: legal framework in Europe for equity investors', 'Gigante'],
  ['VC Investors: legal framework for Anglo-Saxon countries (US and UK)', 'Gigante'], ['VC Investors: management fees, carried interest, risk and return; fiscal framework', 'Gigante'],
  ['Financing Innovation: Angel Investors and VCs', 'Bottazzi'], ["How do VCs choose and how do they affect firms' decisions", 'Bottazzi'],
  ['The Deal Structure: Contracts and Incentives (I)', 'Bottazzi'], ['The Deal Structure (II)', 'Bottazzi'], ['The Contract: Dermacare', 'Bottazzi'], ['Guest Speaker: a VC', 'Bottazzi'],
  ['VC Trends Outlook 2026', 'Zava'], ['Raising a fund and creating a fund thesis', 'Zava'], ['Deal sourcing and matching investor and company', 'Zava'],
  ['Venture Capital Networks', 'Zava'], ['Due Diligence and Financial Models', 'Zava'], ['Investing: Valuation Methods I', 'Zava'], ['Investing: Valuation Methods II', 'Zava'],
  ['Portfolio Company Management and Follow-on Investments', 'Zava'], ['The end: Exits (M&A)', 'Zava'], ['The end: Exits (IPO)', 'Zava'],
  ['Working in VC: Hiring and Interview Process', 'Zava'], ['Artificial Intelligence applications in VC', 'Zava'],
];
vc.forEach(([t, ins], i) => { const n = i + 1; const part3 = n >= 13;
  add('vc', n, null, t, { instructor: ins, inExam: part3, kind: n === 12 ? 'guest' : 'lesson',
    readings: ['Slide e letture ad hoc su Blackboard' + (n >= 17 && n <= 19 ? ' · software ed esercizi su Blackboard' : ''), ...(n === 11 ? ['Case: Dermacare (Course Reserves)'] : [])] }); });

// ---- Data Analysis (class group 27, non-attending) ----
const da = [['2026-09-07', 'Intro + Python recap'], ['2026-09-11', 'Pandas'], ['2026-09-14', 'Pandas: subset, add, remove data'], ['2026-09-21', 'Pandas: cleaning data'],
  ['2026-09-25', 'Pandas: grouping data'], ['2026-09-28', 'Pandas: merging data'], ['2026-10-02', 'Pandas: working with text'], ['2026-10-05', 'Nature of data'],
  ['2026-10-09', 'Descriptive statistics'], ['2026-10-12', 'Linear model (1)'], ['2026-10-16', 'Linear model (2)'], ['2026-10-30', 'Hypothesis testing'],
  ['2026-11-02', 'Further topics in regression'], ['2026-11-06', 'Binary outcome models']];
da.forEach(([d, t], i) => add('da', i + 1, d, t, { instructor: 'Breschi / Gagliardi', readings: i < 7
  ? ['Notebook Jupyter della lezione (Blackboard)', 'Molin S. (2021), Hands-On Data Analysis with Pandas, cap. 1–4 (facoltativo)']
  : ['Slide della lezione e paper selezionati (Blackboard)', 'Hill R.C., Griffiths W.E. & Lim G.C. (2018), Principles of Econometrics (capitoli selezionati)'] }));
['2026-11-09', '2026-11-13', '2026-11-16', '2026-11-23'].forEach((d, i) => add('da', 15 + i, d, 'Data lab / Guest speaker', { kind: 'guest', inExam: false }));
['2026-11-27', '2026-11-30', '2026-12-04'].forEach((d, i) => add('da', 19 + i, d, 'Final project presentations', { kind: 'group', inExam: false }));

// ---- Entrepreneurship (class 27) ----
const ent = [['2026-09-07', 'Introduction. The returns to entrepreneurship', 'Gutierrez'], ['2026-09-09', 'Entrepreneurial judgment and action: deciding under uncertainty', 'Gutierrez'],
  ['2026-09-14', 'Entrepreneurial opportunities', 'Gutierrez', 'Embrace'], ['2026-09-16', 'Entrepreneurial strategy', 'Gutierrez'],
  ['2026-09-21', 'Customers and business models', 'Gutierrez', 'Rent the Runway'], ['2026-09-23', 'From problem to business model', 'Valenti'],
  ['2026-09-28', 'Founding teams', 'Gutierrez', 'Ockham'], ['2026-09-30', 'Co-founders & founder prenups', 'Valenti'],
  ['2026-10-05', 'Financing entrepreneurial ventures', 'Gutierrez', 'Jibo'], ['2026-10-07', 'Scaling and exit', 'Gutierrez', 'Baroo'],
  ['2026-10-12', 'The industry and the mindset', 'Valenti'], ['2026-10-28', 'Building before you raise', 'Valenti'],
  ['2026-11-04', 'Session with Colao', 'Colao', null, 'guest'], ['2026-11-11', 'Session with Colao (2)', 'Colao', null, 'guest'],
  ['2026-11-18', 'The geography of entrepreneurship', 'Gutierrez'], ['2026-11-23', 'Social entrepreneurship & wrap up', 'Gutierrez', 'Sababa']];
ent.forEach(([d, t, ins, cs, kind], i) => add('ent', i + 1, d, t, { instructor: ins, kind: kind || 'lesson', inExam: kind !== 'guest', caseStudy: cs ? `Case study: ${cs}` : '',
  readings: [...(cs ? [`Case study: ${cs}`] : []), 'Letture della sessione (elenco su Blackboard; copyright via Library reserve)', 'Gans, Scott & Stern (2024), Entrepreneurship: Choice and Strategy (companion)'] }));

// ---- IP Law (class 27): readings are book chapters/pages ----
const ip = [
  ['2026-09-07', 'Course introduction: the strategic role of IP for business', 'Manderieux', ['Book ch.1 The Concept of IP, p. 3–4', 'Book: The World Intellectual Property Organization, p. 4–8', 'Book ch.3 The Promotion of Innovation, p. 168–171', 'Book ch.5 Paris Convention, p. 241–249', 'Book: The TRIPS Agreement, p. 345–347 (until “General Provisions, Basic Principles and Final Provisions”)']],
  ['2026-09-10', 'The multifaceted nature of copyright', 'Wennersten', ['Book ch.2 Copyright and Related Rights, p. 40–51 (until “Piracy and Infringement”) and p. 56–67 (from “IP and Traditional Cultural Expressions” until “Trademarks”)', 'Book ch.5 The Berne Convention, p. 262–267 (until “Developing Countries and the Berne Convention”)', 'Book: The WIPO Copyright Treaty (WCT), p. 269–276', 'Book: The Rome Convention, p. 314–319 (until “The Rome Convention and Developing Countries”)']],
  ['2026-09-11', 'Copyright protection on the Internet: an opportunity or a threat for creativity?', 'Wennersten', ['Book: The WIPO Performances and Phonograms Treaty (WPPT), p. 325–331', 'Book ch.7 Computer Programs, p. 435–442', 'Book: Reprography, p. 448–449', 'Book: Audio and Video Recordings, p. 449–450', 'Book: Communication Technologies, p. 450–457']],
  ['2026-09-15', 'Copyright enforcement and remedies in the digital age, and Industrial Design', 'Wennersten', ['Book ch.2 Remedies, p. 52–56', 'Book ch.4 Enforcement of Copyright and Related Rights, p. 207–208 and 213–220', 'Book: Copyright Infringement, p. 226', 'Book: Remedies, p. 228–234', 'Book: The Legal Protection of Industrial Design, p. 112–118']],
  ['2026-09-15', 'Artificial intelligence and copyright: business risks and opportunities', 'Wennersten', ['Book ch.2 Ownership of Copyright, p. 49']],
  ['2026-09-16', 'Industrial Design & Introduction to Licensing as a business tool', 'Wennersten', ['Book: The Legal Protection of Industrial Design, p. 112–118', 'Book: Licensing, p. 172–184', 'Book: Copyright Licenses, p. 191–195']],
  ['2026-09-17', 'Copyright, design, sustainability, and new business models', 'Wennersten', ['Book ch.2 Piracy and Infringement, p. 51–52']],
  ['2026-09-24', 'Trademarks as an innovation tool', 'Manderieux (+ guest, KPMG Legal & Indicam)', ['Book ch.2 Trademarks, p. 67–92 (until “Change of Ownership”)', 'Ulteriori materiali in classe']],
  ['2026-10-08', 'Trademarks I: key principles, registration, use and enforcement', 'Manderieux', ['Book ch.5 Trademark Law Treaty, p. 297–300', 'Book: The TRIPS Agreement, p. 350–351 (Trademarks, Section 2)', 'Book ch.6 The Trademark Office, p. 372–375', 'Ulteriori materiali in classe']],
  ['2026-10-09', 'Trademarks II: EU Trade Mark, Madrid system, geographical indications', 'Manderieux (+ guest Avv. Sobol)', ['Book ch.2 Geographical Indications, p. 120–130', 'Book ch.5 The Madrid Agreement, p. 287–292', 'Book: Treaties on Classification, p. 308–313 (until “The Locarno Agreement”)', 'Ulteriori materiali in classe']],
  ['2026-10-29', 'Patents I: laws, treaties and systems', 'Manderieux', ['Book ch.2 Patents, p. 17–34 (until “Compulsory Licenses”)', 'Book: Patent Law Treaty, p. 301–305', 'Book: The TRIPS Agreement, p. 352–354 (Patents, Section 5)']],
  ['2026-10-30', 'Patents II: registration systems, PCT, US reforms and Bayh-Dole', 'Manderieux', ['Quinn G., “A brave new patent world – first to file becomes law”, IPWatchdog, 16 March 2013', 'Book ch.5 Patent Cooperation Treaty, p. 276–285 (until “Budapest Treaty”)', 'Ulteriori materiali in classe']],
  ['2026-10-30', 'Patents III: European patent system, regional systems, China, computer-implemented inventions', 'Manderieux (+ guest EPO)', ['Book ch.6 The Patent Office, p. 369–372', 'Book: Intergovernmental Cooperation, p. 376–381', 'Book ch.7 Protection of Computer Programs under Patents, p. 436']],
  ['2026-11-05', 'The circulation of IPRs I: technology transfer and licensing', 'Manderieux', ['Book ch.3 Licensing and the Transfer of Technology, p. 172–178 (until “Negotiation of Licensing Agreements”)', 'Book: Negotiation of Licensing Agreements, p. 178–188', 'Book: Types of IP Licenses, p. 188–193']],
  ['2026-11-06', 'The circulation of IPRs II: EU safe harbours, SEPs and FRAND', 'Manderieux', ['Book ch.4 Enforcement of Industrial Property Rights, p. 207–213 (until “Enforcement of Copyright”)', 'Book: Patent Infringement, p. 225–226 (until “Copyright Infringement”)']],
  ['2026-11-12', 'Licensing in practice: antitrust and essential facilities', 'Manderieux', ['Book ch.2 Patents – Compulsory Licensing, p. 34–40', 'Book: Trademarks, p. 92–96 (from “Change of Ownership”) and 97–101 (from “Franchising” until “Types of Franchise”)', 'Book ch.3 Government Control of Licensing Agreements, p. 193–195']],
  ['2026-11-13', 'International trade and IP: the TRIPS Agreement', 'Manderieux', ['Book ch.5 The Rome Convention, p. 314–319', 'Book: TRIPS and WIPO-WTO Cooperation, p. 345–357 (until “Cooperation between WIPO and WTO”)']],
  ['2026-11-19', 'Forced licensing in technology transfer: practical cases', 'Manderieux (+ Deloitte guest, tbc)', ['Materiali forniti in classe per le simulazioni']],
  ['2026-11-26', 'Session with Sekhon (topic to be announced)', 'Sekhon', ['Il syllabus si interrompe qui: argomento da completare']],
];
ip.forEach(([d, t, ins, r], i) => add('ip', i + 1, d, t, { instructor: ins, readings: r }));

const settings = { defaultMinutes: 120, baseBlock: 25, maxSubjects: 3, intervals: [1, 3, 7], phaseNew: 21, phaseReview: 7, newMin: 45, reviewMin: 15, quizMin: 15, theme: 'system', notesFont: 'serif', notesSize: 18, notesWidth: 68, newCardsPerDay: 20, showExcluded: false, rate: 1 };

const writes = [
  ...Object.entries(courses).map(([id, data]) => ({ op: 'set', collection: 'courses', doc_id: id, data })),
  { op: 'set', collection: 'settings', doc_id: 'main', data: settings },
  { op: 'set', collection: 'log', doc_id: 'seed', data: { at: Date.now(), date: '2026-11-04', type: 'setup', text: `Agenda creata: 5 corsi e ${L.length} lezioni dai syllabus`, courseId: null } },
  ...L.map(x => ({ op: 'set', collection: 'lessons', doc_id: x.id, data: x.data })),
];
for (let i = 0; i < writes.length; i += 45) fs.writeFileSync(path.join(out, `batch-${i / 45 + 1}.json`), JSON.stringify(writes.slice(i, i + 45)));
fs.writeFileSync(path.join(out, 'all.json'), JSON.stringify(writes));
console.log(writes.length, 'writes;', L.length, 'lessons');
