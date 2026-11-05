// node prep.js cvis-13  → validates out/<id>.notes.json + quiz.json, writes up/<id>/*.json, prints batch writes
const fs=require('fs'),path=require('path');const SP=__dirname;const id=process.argv[2];
const n=JSON.parse(fs.readFileSync(`${SP}/out/${id}.notes.json`));const q=JSON.parse(fs.readFileSync(`${SP}/out/${id}.quiz.json`));
const strip=s=>String(s||'').replace(/<[^>]+>/g,' ').replace(/&nbsp;/g,' ').replace(/&amp;/g,'&').replace(/&#39;|&rsquo;/g,"'").replace(/\s+/g,' ').trim().toLowerCase();
const errs=[];const chs=Object.fromEntries((n.chapters||[]).map(c=>[c.id,strip(c.html)]));
if(!n.intro||!n.message||!n.chapters||n.chapters.length<4||!n.recap)errs.push('notes missing parts');
if(/`/.test(JSON.stringify(n)))errs.push('backtick in notes');
for(const x of q){if(!x.id||!x.q)errs.push('bad q '+x.id);if(x.type!=='open'&&!(Array.isArray(x.options)&&Number.isInteger(x.answer)&&x.answer<x.options.length))errs.push('bad mc '+x.id);
 if(x.type==='open'&&!x.model)errs.push('no model '+x.id);if(!chs[x.chapter]&&x.chapter!=='recap')errs.push('bad chapter '+x.id);
 else{const t=x.chapter==='recap'?strip(n.recap):chs[x.chapter];if(!t.includes(strip(x.quote).slice(0,60)))errs.push('quote not found '+x.id)}}
const size=Buffer.byteLength(JSON.stringify(n));if(size>240000)errs.push('notes too big '+size);
if(errs.length){console.log('ERRORS',errs);process.exit(1)}
const up=`${SP}/up/${id}`;fs.mkdirSync(up,{recursive:true});
n.lessonId=id;n.courseId=n.courseId||id.split('-')[0];n.updatedAt=n.updatedAt||Date.now();
fs.writeFileSync(`${up}/notes.json`,JSON.stringify(n));
const w=[{op:'set',collection:'notes',doc_id:id,file_path:`${up}/notes.json`}];
q.forEach((x,i)=>{const d={...x,courseId:n.courseId,lessonId:id,order:x.order||i+1};delete d.id;fs.writeFileSync(`${up}/${x.id}.json`,JSON.stringify(d));w.push({op:'set',collection:'quiz',doc_id:x.id,file_path:`${up}/${x.id}.json`})});
w.push({op:'set',collection:'log',doc_id:'notes-'+id,data:{at:Date.now(),date:new Date().toISOString().slice(0,10),type:'notes',text:`Appunti e ${q.length} domande: ${n.title}`,courseId:n.courseId}});
console.log(JSON.stringify(w));console.error(`OK ${id}: ${n.chapters.length} chapters, ${q.length} questions, ${Math.round(size/1024)} KB`);
