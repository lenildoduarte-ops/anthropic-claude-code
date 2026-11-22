const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1350},deviceScaleFactor:1});
for(const n of ['p1','p2']){await p.goto('file://'+__dirname+'/'+n+'.html',{waitUntil:'networkidle'});await p.evaluate(()=>document.fonts.ready);
const o=await p.evaluate(()=>{const f=document.querySelector('.foot').getBoundingClientRect().top;let m=0;document.querySelectorAll('body > *:not(.foot):not(script):not(link):not(style)').forEach(e=>{m=Math.max(m,e.getBoundingClientRect().bottom)});return [Math.round(m),Math.round(f)]});
console.log(n,'content bottom',o[0],'footer top',o[1]);await p.screenshot({path:__dirname+'/out/'+n+'.png'});}
await b.close()})();
