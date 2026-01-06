from flask import Flask, render_template_string
import datetime
import random

app = Flask(__name__)

NAME = "Büşra"
START_DATE = datetime.date(2025, 12, 17)

NOTES = [
    "Seni her düşündüğümde kalbim hızlanıyor 💖",
    "Gülüşün günümü aydınlatıyor 🌸",
    "Beraber geçirdiğimiz her an çok değerli 💘",
    "Sen yanımdayken dünya daha güzel 🦖💗",
    "Büşra, sen benim en tatlı maceramsın 💌",
    "Her günümüz bir öncekinden daha özel 💕",
]

def days_together():
    today = datetime.date.today()
    delta = today - START_DATE
    return delta.days if delta.days > 0 else 0

HTML = """
<!doctype html>
<html lang="tr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Büşra’nın Özel Portalı 💖</title>
<style>
body { margin:0; font-family: Arial; overflow:hidden; background:#fdeff2; transition: background 0.5s;}
canvas {display:block;}
#ui {position:fixed; top:10px; right:10px; font-size:14px;}
#musicToggle {position:fixed; bottom:10px; left:10px; padding:8px 12px; border-radius:20px; background:#fff; cursor:pointer;}
#nightToggle {position:fixed; bottom:10px; right:10px; padding:8px 12px; border-radius:20px; background:#fff; cursor:pointer;}
#menu {position:fixed; top:10px; left:10px; background:#fff; padding:10px; border-radius:12px; box-shadow:0 4px 12px rgba(0,0,0,0.15);}
#menu button {margin:3px;}
#content {position:absolute; top:60px; left:0; width:100%; text-align:center;}
#daysCounter, #notesArea {display:none; margin-top:50px; font-family: 'Georgia', serif; cursor:pointer;}
#daysNumber {font-size:80px; color:#ff6f91;}
#daysText {font-size:18px; color:#555;}
#note {font-size:14px; color:#333; margin-top:5px;}
#startBtn, #stopBtn {margin:15px; padding:10px 20px; border-radius:20px; background:#ff6f91; border:none; color:#fff; cursor:pointer;}
#notesArea {font-size:20px; color:#ff4f91; min-height:120px; display:flex; align-items:center; justify-content:center; flex-direction:column;}
#changeNote {margin-top:15px; padding:8px 16px; border-radius:20px; background:#fff; border:none; cursor:pointer;}
</style>
</head>
<body>

<canvas id="game"></canvas>
<div id="ui"></div>

<div id="menu">
<button onclick="showSection('game')">Oyun 🦖</button>
<button onclick="showSection('days')">Gün Sayacı 📅</button>
<button onclick="showSection('notes')">Sevgili Notları 💌</button>
</div>

<div id="content">
  <div id="daysCounter">
      <div id="daysNumber">{{ days }}</div>
      <div id="daysText">gündür birlikteyiz</div>
  </div>

  <div id="gameControls">
    <button id="startBtn" onclick="togglePause()">Başlat 🦖</button>
    <div id="note">Bu oyun sana özel 💖</div>
    <button id="stopBtn" onclick="togglePause()" style="display:none;">Durdur ⏸️</button>
  </div>

  <div id="notesArea">
    <div id="currentNote"></div>
    <button id="changeNote" onclick="nextNote()">💌 Yeni Not</button>
  </div>
</div>

<div id="musicToggle" onclick="toggleMusic()">🎵</div>
<div id="nightToggle" onclick="toggleNight()">🌙/☀️</div>

<audio id="music" loop>
  <source src="https://cdn.pixabay.com/download/audio/2022/03/15/audio_7b7f0c6a53.mp3">
</audio>

<script>
const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");
const music = document.getElementById("music");
let musicOn = true;
let nightMode = false;
let paused = true;

let w,h;
function resize(){ w=canvas.width=window.innerWidth; h=canvas.height=window.innerHeight; }
window.addEventListener("resize", resize);
resize();

// Arka plan kalpleri
let bgHearts = Array.from({length:18},()=>({x:Math.random()*w,y:Math.random()*h,speed:0.3+Math.random()}));
let hearts=[];

// Menü
function showSection(section){
    document.getElementById("game").style.display='none';
    document.getElementById("daysCounter").style.display='none';
    document.getElementById("notesArea").style.display='none';
    document.getElementById("gameControls").style.display='none';

    if(section==='game'){
        document.getElementById("game").style.display='block';
        document.getElementById("gameControls").style.display='block';
    }
    if(section==='days'){
        document.getElementById("daysCounter").style.display='block';
        paused = true; // gün sayacı açılınca oyun duracak
        document.getElementById('stopBtn').style.display='none';
        document.getElementById('startBtn').style.display='inline-block';
        music.pause();
    }
    if(section==='notes'){
        document.getElementById("notesArea").style.display='flex';
        paused = true; // notlar açılınca oyun duracak
        document.getElementById('stopBtn').style.display='none';
        document.getElementById('startBtn').style.display='inline-block';
        music.pause();
    }
}

// Music toggle
function toggleMusic(){ musicOn=!musicOn; if(musicOn && !paused){ music.play().catch(()=>{}); document.getElementById('musicToggle').innerText='🎵'; } else { music.pause(); document.getElementById('musicToggle').innerText='🔇'; } }

// Night toggle
function toggleNight(){ nightMode=!nightMode; document.body.style.background=nightMode?'#1c1c2b':'#fdeff2'; }

// Gün sayacı tıklanınca mini kalpler
const daysCounter=document.getElementById('daysCounter');
daysCounter.addEventListener('click',function(e){
    for(let i=0;i<15;i++){
        hearts.push({x:e.clientX,y:e.clientY,speed:Math.random()*2+1,size:10+Math.random()*10});
    }
});

// Kalpler çizimi
function drawHearts(){
    ctx.clearRect(0,0,w,h);
    bgHearts.forEach(hh=>{
        hh.y+=hh.speed;
        if(hh.y>h){ hh.y=-20; hh.x=Math.random()*w; }
        ctx.font = "18px serif";
        ctx.fillText("💗", hh.x, hh.y);
    });
    hearts.forEach((h,i)=>{
        h.y-=h.speed; h.size*=0.97;
        if(h.size<1) hearts.splice(i,1);
        else{ ctx.font=h.size+'px serif'; ctx.fillText('💖',h.x,h.y); }
    });
}

// Dino Run
let dino={x:80,y:h-110,vy:0,size:40,grounded:true};
let obstacles=[], score=0, bestScore=localStorage.getItem('bestScore')||0;
let speed=6, gravity=1, jumpForce=-18, spawnTimer=0;

function togglePause(){
    paused = !paused;
    document.getElementById('startBtn').style.display = paused ? 'inline-block' : 'none';
    document.getElementById('stopBtn').style.display = paused ? 'none' : 'inline-block';
    if(!paused && musicOn){ music.play().catch(()=>{}); } else { music.pause(); }
}

// Kontroller
document.addEventListener('keydown',e=>{ if(e.code==='Space') jump(); });
document.addEventListener('touchstart',jump);
function jump(){ if(dino.grounded && !paused){ dino.vy=jumpForce; dino.grounded=false; } }

function spawnObstacle(){ spawnTimer++; if(spawnTimer>80+Math.random()*60){ obstacles.push({x:w+40}); spawnTimer=0; } }

function loop(){
    requestAnimationFrame(loop);
    drawHearts();

    if(paused) return;

    // Zemin
    ctx.fillStyle=nightMode?'#aaa':'#333';
    ctx.fillRect(0,h-70,w,2);

    // Dino physics
    dino.vy+=gravity;
    dino.y+=dino.vy;
    if(dino.y>=h-70-dino.size){ dino.y=h-70-dino.size; dino.vy=0; dino.grounded=true; }

    // Draw dino
    ctx.font='40px serif'; ctx.fillText('🦖',dino.x,dino.y+dino.size);

    // Obstacles
    spawnObstacle();
    obstacles.forEach((obs,i)=>{
        obs.x-=speed;
        ctx.font='36px serif';
        ctx.fillText('🌵',obs.x,h-75);
        if(dino.x+30>obs.x && dino.x<obs.x+30 && dino.y+dino.size>h-75) endGame();
    });

    speed+=0.002;
    score++;
    document.getElementById('ui').innerText='Skor: '+score+' | Rekor: '+bestScore;
}

function endGame(){
    paused=true;
    music.pause();
    document.getElementById('stopBtn').style.display='none';
    document.getElementById('startBtn').style.display='inline-block';
    if(score>bestScore){ bestScore=score; localStorage.setItem('bestScore',score); bestScore=score; }
    let msg=score<300?"Tatlı bir başlangıç 💖":score<800?"Kalbim seninle gurur duyuyor 💘":"Büşra, bu dinozor kalbimi tamamen kazandı 🦖💖";
    alert("Oyun bitti!\\nSkor: "+score+"\\n"+msg); 
}

// Sevgili notları
let currentNoteIndex = 0;
const notes = {{ notes|tojson }};
function nextNote(){
    currentNoteIndex = (currentNoteIndex+1)%notes.length;
    document.getElementById('currentNote').innerText = notes[currentNoteIndex];
}
document.getElementById('currentNote').innerText = notes[currentNoteIndex];

// Başlangıç
loop();
setInterval(drawHearts,16);
</script>

</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML, days=days_together(), notes=NOTES)

if __name__ == "__main__":
    app.run(debug=False)
