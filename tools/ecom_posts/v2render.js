const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1350}});
for(const n of ['v2p1','v2p2']){await p.goto('file://'+__dirname+'/'+n+'.html',{waitUntil:'networkidle'});await p.evaluate(()=>document.fonts.ready);
const o=await p.evaluate(()=>{const f=document.querySelector('.foot').getBoundingClientRect().top;let m=0;document.querySelectorAll('.wrap > *:not(.foot)').forEach(e=>{m=Math.max(m,e.getBoundingClientRect().bottom)});
const ov=[...document.querySelectorAll('.wrap *')].filter(e=>e.scrollWidth>e.clientWidth+2&&getComputedStyle(e).overflow!='visible').length;return [Math.round(m),Math.round(f),document.fonts.check('900 40px Archivo')]});
console.log(n,o);await p.screenshot({path:__dirname+'/out/'+n+'.png'});}
await b.close()})();
