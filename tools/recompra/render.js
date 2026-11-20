const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
await p.goto('file://'+__dirname+'/panel.html',{waitUntil:'networkidle'});await p.evaluate(()=>document.fonts.ready);
const a=+process.argv[2],e=+process.argv[3],o=process.argv[4];for(let i=Math.round(a*30);i<Math.round(e*30);i++){await p.evaluate(t=>scene(t),i/30);await p.screenshot({path:`${__dirname}/${o}/f${String(i).padStart(5,'0')}.png`,omitBackground:true});}
await b.close()})();
