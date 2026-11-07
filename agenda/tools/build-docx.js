// node build-docx.js <course>   reads word/<course>/manifest.json + word/<course>/<id>.json, writes word/out/<file>.docx
// Lesson JSON: {id,title,subtitle,blocks:[...]}; block types:
//  {t:"p",text}  {t:"h1",text} (section)  {t:"h2",text} (subsection)
//  {t:"formula",text} (centred, Cambria Math; several formulas separated by "   ")
//  {t:"table",head:[..],rows:[[..]],widths?:[relative],caption}
//  {t:"figure",file,caption,width?(inches, default 6.3)}
//  {t:"box",title,text}  (shaded example box; text may contain "\n\n" for paragraphs)
//  {t:"bullets",items:[..]}  {t:"numbered",items:[..]}
//  {t:"code",lines:[{code,out?,type?}],caption?}
// Inline markup in any text: **bold**, *italic*, _{sub}, ^{sup}
const fs = require('fs'), path = require('path');
const D = require('docx');
const { Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType, Table, TableRow, TableCell, WidthType,
  ShadingType, BorderStyle, ImageRun, LineRuleType, Bookmark, InternalHyperlink, LevelFormat, Footer, PageNumber, TableOfContents, PageBreak, TableLayoutType } = D;

const W = __dirname, course = process.argv[2];
const man = JSON.parse(fs.readFileSync(`${W}/${course}/manifest.json`));
const BODY = 'Aptos', HEAD = 'Calibri', TXT = '222222', NAVY = '17365D', ROW = 'F6F8FA', BOX = 'EAF0F7', GREY = '7F8C9B';
const CONTENT_W = 12240 - 2 * 1224; // 9792 dxa

function runs(text, base = {}) {
  const out = []; const re = /(\*\*[^*]+\*\*|\*[^*]+\*|_\{[^}]*\}|\^\{[^}]*\})/g;
  let last = 0, m; text = String(text ?? '');
  const push = (s, o) => { if (s) out.push(new TextRun({ text: s, ...base, ...o })); };
  while ((m = re.exec(text))) {
    push(text.slice(last, m.index), {});
    const tok = m[0];
    if (tok.startsWith('**')) {
      // allow nested sub/sup inside bold
      runs(tok.slice(2, -2), { ...base, bold: true }).forEach(r => out.push(r));
    } else if (tok.startsWith('*')) push(tok.slice(1, -1), { italics: true });
    else if (tok.startsWith('_{')) push(tok.slice(2, -1), { subScript: true });
    else push(tok.slice(2, -1), { superScript: true });
    last = m.index + tok.length;
  }
  push(text.slice(last), {});
  return out;
}
const P = (text, opt = {}) => new Paragraph({ children: runs(text, opt.run || {}), ...opt.par });
const border = { style: BorderStyle.SINGLE, size: 4, color: 'D0D7DE' };
const borders = { top: border, bottom: border, left: border, right: border };
let tableNo = 0, figNo = 0;

function caption(text) {
  return new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 60, after: 200 },
    children: runs(text, { italics: true, color: GREY, size: 17 }) });
}
function cellParas(text, o) { return String(text ?? '').split('\n').map(s => new Paragraph({ spacing: { after: 0 }, children: runs(s, o) })); }

function table(b) {
  const n = b.head ? b.head.length : b.rows[0].length;
  const rel = b.widths && b.widths.length === n ? b.widths : Array(n).fill(1);
  const sum = rel.reduce((a, c) => a + c, 0);
  const cw = rel.map(x => Math.floor(CONTENT_W * x / sum)); cw[n - 1] = CONTENT_W - cw.slice(0, -1).reduce((a, c) => a + c, 0);
  const mk = (cells, hdr) => new TableRow({ tableHeader: !!hdr, cantSplit: true, children: cells.map((c, i) => new TableCell({
    borders, width: { size: cw[i], type: WidthType.DXA }, margins: { top: 70, bottom: 70, left: 110, right: 110 },
    shading: { fill: hdr ? NAVY : (i === 0 ? ROW : 'FFFFFF'), type: ShadingType.CLEAR, color: 'auto' },
    children: cellParas(c, hdr ? { bold: true, color: 'FFFFFF', size: 18 } : { size: 18, bold: i === 0 && b.firstBold !== false ? true : undefined }) })) });
  const rows = []; if (b.head) rows.push(mk(b.head, true)); b.rows.forEach(r => rows.push(mk(r, false)));
  const out = [new Table({ width: { size: CONTENT_W, type: WidthType.DXA }, columnWidths: cw, rows })];
  if (b.caption) { tableNo++; out.push(caption(`Table ${tableNo}  ${b.caption.replace(/^Table\s*\d+\s*/i, '')}`)); }
  else out.push(new Paragraph({ spacing: { after: 120 }, children: [] }));
  return out;
}
function pngSize(buf) { return { w: buf.readUInt32BE(16), h: buf.readUInt32BE(20) }; }
function figure(b, dir) {
  const f = path.isAbsolute(b.file) ? b.file : path.join(dir, b.file);
  if (!fs.existsSync(f)) { console.error('MISSING FIGURE', f); return [P(`[missing figure ${b.file}]`)]; }
  const buf = fs.readFileSync(f); const { w, h } = pngSize(buf); const wi = Math.min(b.width || 6.3, 6.7);
  const out = [new Paragraph({ alignment: AlignmentType.CENTER, keepNext: true, spacing: { before: 120, after: 0, line: 240, lineRule: LineRuleType.AUTO },
    children: [new ImageRun({ type: 'png', data: buf, transformation: { width: Math.round(wi * 96), height: Math.round(wi * 96 * h / w) } })] })];
  if (b.caption) { figNo++; out.push(caption(`Figure ${figNo}  ${b.caption.replace(/^Figure\s*\d+\s*/i, '')}`)); }
  return out;
}
function box(b) {
  const paras = [];
  if (b.title) paras.push(new Paragraph({ spacing: { after: 60 }, children: runs(b.title, { bold: true, color: NAVY }) }));
  String(b.text || '').split(/\n\n+/).forEach(s => paras.push(new Paragraph({ spacing: { after: 60 }, children: runs(s) })));
  const lb = { style: BorderStyle.SINGLE, size: 18, color: NAVY }, nb = { style: BorderStyle.NONE, size: 0, color: 'FFFFFF' };
  return [new Table({ width: { size: CONTENT_W, type: WidthType.DXA }, columnWidths: [CONTENT_W], rows: [new TableRow({ cantSplit: true, children: [new TableCell({
    width: { size: CONTENT_W, type: WidthType.DXA }, borders: { left: lb, top: nb, bottom: nb, right: nb },
    shading: { fill: BOX, type: ShadingType.CLEAR, color: 'auto' }, margins: { top: 100, bottom: 100, left: 180, right: 180 }, children: paras })] })] }),
    new Paragraph({ spacing: { after: 120 }, children: [] })];
}
function code(b) {
  const nb = { style: BorderStyle.NONE, size: 0, color: 'FFFFFF' };
  const rows = [];
  for (const l of b.lines) {
    const ch = [new Paragraph({ spacing: { after: 0 }, children: String(l.code).split('\n').flatMap((s, i) => [new TextRun({ text: s, font: 'Consolas', size: 17, color: '0B3D6B', break: i ? 1 : 0 })]) })];
    if (l.out !== undefined && l.out !== null && l.out !== '') {
      ch.push(new Paragraph({ spacing: { before: 40, after: 0 }, children: [
        ...(l.type ? [new TextRun({ text: l.type + '  ', font: BODY, size: 15, bold: true, color: GREY })] : []),
        ...String(l.out).split('\n').map((s, i) => new TextRun({ text: s, font: 'Consolas', size: 16, color: '444444', break: i ? 1 : 0 }))] }));
    }
    rows.push(new TableRow({ cantSplit: true, children: [new TableCell({ width: { size: CONTENT_W, type: WidthType.DXA },
      borders: { top: nb, left: nb, right: nb, bottom: { style: BorderStyle.SINGLE, size: 2, color: 'E1E6EC' } },
      shading: { fill: ROW, type: ShadingType.CLEAR, color: 'auto' }, margins: { top: 60, bottom: 60, left: 140, right: 140 }, children: ch })] }));
  }
  const out = [new Table({ width: { size: CONTENT_W, type: WidthType.DXA }, columnWidths: [CONTENT_W], rows })];
  out.push(b.caption ? caption(b.caption) : new Paragraph({ spacing: { after: 120 }, children: [] }));
  return out;
}
function block(b, dir) {
  switch (b.t) {
    case 'p': return [P(b.text)];
    case 'h1': return [new Paragraph({ heading: HeadingLevel.HEADING_2, children: runs(b.text) })];
    case 'h2': return [new Paragraph({ heading: HeadingLevel.HEADING_3, children: runs(b.text) })];
    case 'formula': return [new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 80, after: 160 },
      children: String(b.text).split(/\s{3,}/).flatMap((s, i) => [...(i ? [new TextRun({ text: '\t', font: 'Cambria Math' })] : []), ...runs(s, { font: 'Cambria Math', size: 21 })]) ,
      tabStops: [] })];
    case 'table': return table(b);
    case 'figure': return figure(b, dir);
    case 'box': return box(b);
    case 'bullets': return b.items.map(s => new Paragraph({ numbering: { reference: 'bul', level: 0 }, spacing: { after: 60 }, children: runs(s) }));
    case 'numbered': { const ref = 'num' + (numCount++); numRefs.push(ref); return b.items.map(s => new Paragraph({ numbering: { reference: ref, level: 0 }, spacing: { after: 60 }, children: runs(s) })); }
    case 'code': return code(b);
    default: console.error('unknown block', b.t); return [];
  }
}
let numCount = 0; const numRefs = [];

const dir = `${W}/${course}`; const children = [];
// cover
children.push(new Paragraph({ spacing: { before: 2400, after: 120 }, children: [new TextRun({ text: man.title, font: HEAD, bold: true, size: 56 })] }));
children.push(new Paragraph({ spacing: { after: 120 }, children: [new TextRun({ text: man.subtitle, font: HEAD, size: 26, color: '4F6A8A' })] }));
if (man.note) children.push(new Paragraph({ spacing: { before: 240 }, children: runs(man.note, { color: '555555' }) }));
children.push(new Paragraph({ children: [new PageBreak()] }));
children.push(new Paragraph({ spacing: { after: 160 }, children: [new TextRun({ text: 'Contents', font: HEAD, bold: true, size: 34 })] }));
const tocAt = children.length;

const parts = [{ name: null, ids: man.lessons }];
if (man.guests && man.guests.length) parts.push({ name: man.guestTitle || 'Guest speakers', ids: man.guests });
const missing = []; const toc = [];
for (const part of parts) {
  if (part.name) {
    children.push(new Paragraph({ pageBreakBefore: true, spacing: { before: 1800, after: 120 }, children: [new TextRun({ text: part.name, font: HEAD, bold: true, size: 44, color: NAVY })] }));
    if (man.guestNote) children.push(P(man.guestNote, { run: { color: '555555' } }));
  }
  for (const id of part.ids) {
    const f = `${dir}/${id}.json`; if (!fs.existsSync(f)) { missing.push(id); continue; }
    const L = JSON.parse(fs.readFileSync(f));
    tableNo = 0; figNo = 0;
    const bm='L_'+id.replace(/[^A-Za-z0-9]/g,'_'); toc.push({bm,title:L.title,sub:L.subtitle,part:part.name});
    children.push(new Paragraph({ heading: HeadingLevel.HEADING_1, pageBreakBefore: true, children: [new Bookmark({ id: bm, children: runs(L.title) })] }));
    if (L.subtitle) children.push(new Paragraph({ spacing: { after: 200 }, children: [new TextRun({ text: L.subtitle, font: HEAD, size: 26, color: '4F6A8A' })] }));
    for (const b of L.blocks) children.push(...block(b, dir));
  }
}
{ const items=[]; let cur=null; for (const t of toc) { if (t.part!==cur && t.part) { items.push(new Paragraph({ spacing:{before:200,after:80}, children:[new TextRun({text:t.part,bold:true,color:NAVY,size:22})] })); } cur=t.part;
  items.push(new Paragraph({ spacing:{after:70}, children:[new InternalHyperlink({ anchor:t.bm, children:[new TextRun({text:t.title,color:'1F3B63',size:21})] }), ...(t.sub?[new TextRun({text:'  ·  '+t.sub,color:GREY,size:18})]:[])] })); }
  children.splice(tocAt,0,...items); }
if (missing.length) console.error('missing lessons:', missing.join(', '));

const H = (size, before, after, color = '000000') => ({ run: { font: HEAD, bold: true, size, color }, paragraph: { spacing: { before, after }, keepNext: true, keepLines: true } });
const doc = new Document({
  creator: 'Agenda di Sessione', title: man.title,
  
  styles: {
    default: { document: { run: { font: BODY, size: 20, color: TXT }, paragraph: { spacing: { after: 140, line: 264, lineRule: LineRuleType.AUTO } } } },
    paragraphStyles: [
      { id: 'Heading1', name: 'Heading 1', basedOn: 'Normal', next: 'Normal', quickFormat: true, ...H(46, 0, 80), paragraph: { spacing: { before: 0, after: 60 }, keepNext: true, outlineLevel: 0 } },
      { id: 'Heading2', name: 'Heading 2', basedOn: 'Normal', next: 'Normal', quickFormat: true, ...H(32, 280, 120), paragraph: { spacing: { before: 280, after: 120 }, keepNext: true, keepLines: true, outlineLevel: 1 } },
      { id: 'Heading3', name: 'Heading 3', basedOn: 'Normal', next: 'Normal', quickFormat: true, ...H(24, 200, 80), paragraph: { spacing: { before: 200, after: 80 }, keepNext: true, keepLines: true, outlineLevel: 2 } },
    ],
  },
  numbering: { config: [
    { reference: 'bul', levels: [{ level: 0, format: LevelFormat.BULLET, text: '•', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 540, hanging: 260 } } } }] },
    ...Array.from({ length: 400 }, (_, i) => ({ reference: 'num' + i, levels: [{ level: 0, format: LevelFormat.DECIMAL, text: '%1.', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 540, hanging: 300 } } } }] })),
  ] },
  sections: [{
    properties: { page: { size: { width: 12240, height: 15840 }, margin: { top: 1008, right: 1224, bottom: 1008, left: 1224 } } },
    footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.RIGHT, children: [new TextRun({ text: 'Page ', size: 18, color: GREY }), new TextRun({ children: [PageNumber.CURRENT], size: 18, color: GREY })] })] }) },
    children,
  }],
});
fs.mkdirSync(`${W}/out`, { recursive: true });
const outF = `${W}/out/${man.file}`;
Packer.toBuffer(doc).then(b => { fs.writeFileSync(outF, b); console.log('wrote', outF, Math.round(b.length / 1024) + ' KB'); });
