const {chromium}=require('playwright');const fs=require('fs');const SP=process.argv[2],id=process.argv[3];
const seed=JSON.parse(fs.readFileSync(SP+'/seed/all.json'));const store={};for(const w of seed){(store[w.collection]=store[w.collection]||{})[w.doc_id]=w.data}
store.notes={[id]:JSON.parse(fs.readFileSync(`${SP}/up/${id}/notes.json`))};store.quiz={};
for(const f of fs.readdirSync(`${SP}/up/${id}`))if(f!=='notes.json')store.quiz[f.replace('.json','')]=JSON.parse(fs.readFileSync(`${SP}/up/${id}/${f}`));
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1280,height:900}});const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.addInitScript(store=>{const snap=(c,w)=>{let d=Object.entries(store[c]||{}).map(([id,x])=>({id,exists:true,data:()=>x}));if(w)d=d.filter(x=>x.data()[w[0]]===w[2]);return{docs:d}};
 const q=(c,w)=>({where:(a,b,v)=>q(c,[a,b,v]),orderBy:()=>q(c,w),limit:()=>q(c,w),get:async()=>snap(c,w),onSnapshot:n=>{setTimeout(()=>n(snap(c,w)),10);return()=>{}}});
 const doc=pth=>{const s=pth.split('/');return{get:async()=>{const x=(store[s[0]]||{})[s[1]];return{exists:!!x,data:()=>x}},set:async()=>{},update:async()=>{},delete:async()=>{}}};
 window.claude={use:async n=>n==='db'?{collection:c=>q(c),doc}:null}},store);
await p.goto('file:///home/user/gmlex/agenda/index.html');await p.waitForTimeout(500);
const qs=Object.values(store.quiz);
await p.evaluate(id=>openReader(id),id);await p.waitForTimeout(500);
const r=await p.evaluate(()=>({ch:document.querySelectorAll('details.ch').length,boxes:document.querySelectorAll('.box').length,tables:document.querySelectorAll('article table').length,bars:document.querySelectorAll('.bars .br').length}));console.log(id,JSON.stringify(r));
let miss=0;for(const x of qs){await p.evaluate(x=>{document.querySelectorAll('mark.flash').forEach(m=>m.replaceWith(...m.childNodes));focusQuote(x.chapter,x.quote)},x);if(!(await p.$('mark.flash')))miss++}
console.log('quotes not highlighted:',miss,'/',qs.length);
if(process.argv[4])await p.screenshot({path:`${SP}/r-${id}.png`});console.log('errors',errs);await b.close()})();
