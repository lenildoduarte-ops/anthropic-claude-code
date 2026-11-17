const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1350}});
for(const n of [1,2,3,4,5]){await p.goto('file://'+__dirname+'/p'+n+'.html');await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(500);await p.screenshot({path:__dirname+'/out/post'+n+'.png'});}
await b.close()})();
