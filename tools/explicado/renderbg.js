const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
await p.goto('file://'+__dirname+'/bg.html',{waitUntil:'networkidle'});await p.evaluate(()=>document.fonts.ready);
const fps=15,a=+process.argv[2],e=+process.argv[3];for(let i=Math.round(a*fps);i<Math.round(e*fps);i++){await p.evaluate(t=>scene(t),i/fps);await p.screenshot({path:`${__dirname}/bgf/b${String(i).padStart(5,'0')}.png`});}
await b.close()})();
