const {chromium}=require('playwright');const fs=require('fs');
const F=[
 ["Tem gente que admira o seu resultado,","mas não aguentaria uma semana da sua rotina."],
 ["Você não está atrasado.","Está pagando o preço que os outros não tiveram coragem de pagar."],
 ["Quem critica a sua empresa de fora nunca pagou um boleto dela.","Opinião sem risco é só barulho."],
 ["Amigo que diz “vai dar certo” é fácil de achar.","Difícil é achar quem te indica para um cliente."],
 ["Disciplina é treinar quando ninguém está olhando.","Resultado é quando todo mundo começa a olhar."],
 ["Empreender é acordar desempregado todo dia","e ter que se contratar de novo."],
];
const av='data:image/jpeg;base64,'+fs.readFileSync(__dirname+'/avatar.jpg').toString('base64');
const html=([a,b])=>`<html><head><link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;800&display=swap" rel="stylesheet"><style>
*{margin:0;padding:0;box-sizing:border-box}body{width:1080px;height:1350px;background:#fff;color:#0f1419;font-family:Inter,sans-serif;display:flex;align-items:center}
.w{padding:0 96px;width:100%}.h{display:flex;align-items:center;gap:30px;margin-bottom:56px}
.h img{width:150px;height:150px;border-radius:50%;object-fit:cover;box-shadow:0 0 0 5px #fff,0 0 0 9px #e2e6ec}
.n{font-weight:800;font-size:44px;letter-spacing:-.01em}.u{font-weight:400;font-size:38px;color:#536471;margin-top:4px}
.t{font-size:70px;line-height:1.16;letter-spacing:-.02em;font-weight:400;text-wrap:pretty}.t b{font-weight:800}
</style></head><body><div class="w"><div class="h"><img src="${av}"><div><div class="n">Lenildo Duarte</div><div class="u">@lenildo.ads</div></div></div>
<div class="t">${a} <b>${b}</b></div></div></body></html>`;
(async()=>{const br=await chromium.launch();const p=await br.newPage({viewport:{width:1080,height:1350}});
for(let i=0;i<F.length;i++){await p.setContent(html(F[i]),{waitUntil:'networkidle'});await p.evaluate(()=>document.fonts.ready);await p.screenshot({path:__dirname+`/out/frase${i+1}.png`});}
await br.close()})();
