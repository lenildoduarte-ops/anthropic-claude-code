const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
await p.goto('file://'+__dirname+'/overlay.html',{waitUntil:'networkidle'});await p.evaluate(()=>document.fonts.ready);
const fps=30,start=+(process.argv[2]||0),end=+(process.argv[3]||32.1),out=process.argv[4]||'frames';
let i=Math.round(start*fps);for(;i<Math.round(end*fps);i++){await p.evaluate(t=>scene(t),i/fps);await p.screenshot({path:`${__dirname}/${out}/f${String(i).padStart(5,'0')}.png`,omitBackground:true});}
await b.close()})();
