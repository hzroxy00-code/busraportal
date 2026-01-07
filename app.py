from flask import Flask, render_template_string
import datetime

app = Flask(__name__)

NAME = "Büşra"
START_DATE = datetime.date(2025, 12, 17)

# Sevgili notları
NOTES = [
    "Seninle geçen her saniye, kalbimin en güzel melodisi oluyor 🎶💖",
    "Gözlerinde kaybolmak, dünyadaki en huzurlu yolculuk benim için ✨",
    "Sen benim en güzel tesadüfüm, en doğru seçimim ve en büyük şansım 💕",
    "Yanımda olduğunda dünya daha renkli, daha umut dolu 🌸",
    "Varlığın, en karanlık gecelerime bile ışık saçan bir yıldız 🌙⭐",
    "Her günümüz, bir öncekinden daha özel ve daha unutulmaz 💘",
    "Seninle hayat, şiir gibi akıyor; her mısrası aşkla dolu 📖💗",
    "Kalbim seninle attığında, tüm evren daha anlamlı oluyor 🌍💞",
    "Sen benim en güzel hikâyem, en değerli sırlarımsın 💌",
    "Birlikteyken zaman duruyor; sadece biz kalıyoruz 💍💖",
]

# Özel günler
SPECIAL_DATES = {
    "Tanışma Günü 💞": (17, 12),
    "Büşra’nın Doğum Günü 🎂": (28, 10),
    "Yıl Dönümümüz 💍": (17, 12),
}

# Türkçe aylar
MONTHS_TR = {
    1: "Ocak", 2: "Şubat", 3: "Mart", 4: "Nisan",
    5: "Mayıs", 6: "Haziran", 7: "Temmuz", 8: "Ağustos",
    9: "Eylül", 10: "Ekim", 11: "Kasım", 12: "Aralık",
}

def format_date_tr(date):
    return f"{date.day} {MONTHS_TR[date.month]} {date.year}"

def days_together():
    from datetime import datetime, timezone, timedelta
    tz = timezone(timedelta(hours=3))
    today = datetime.now(tz).date()
    delta = today - START_DATE
    return delta.days if delta.days > 0 else 0

def days_until(date):
    from datetime import datetime, timezone, timedelta
    tz = timezone(timedelta(hours=3))
    today = datetime.now(tz).date()
    delta = (date - today).days
    return delta if delta >= 0 else 0

def next_occurrence(day, month):
    from datetime import datetime, timezone, timedelta, date
    tz = timezone(timedelta(hours=3))
    today = datetime.now(tz).date()
    year = today.year
    target = date(year, month, day)
    if target < today:
        target = date(year + 1, month, day)
    return target

HTML = """
<!doctype html>
<html lang="tr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Büşra’nın Özel Portalı 💖</title>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.2/css/all.min.css"/>
<style>
body { margin:0; font-family: Arial, sans-serif; overflow:hidden; background:#fdeff2; transition: background 0.5s;}
canvas {display:block;}
#ui {position:fixed; top:10px; right:10px; font-size:14px;}
#musicToggle {position:fixed; bottom:10px; left:10px; padding:8px 12px; border-radius:20px; background:#fff; cursor:pointer;}
#nightToggle {position:fixed; bottom:10px; right:10px; padding:8px 12px; border-radius:20px; background:#fff; cursor:pointer;}
#menu {position:fixed; top:10px; left:10px; background:#fff; padding:10px; border-radius:12px; box-shadow:0 4px 12px rgba(0,0,0,0.15);}
#menu button {margin:3px;}
#content {position:absolute; top:60px; left:0; width:100%; text-align:center;}
#daysCounter, #notesArea, #specialDays, #socials {display:none; margin-top:50px; font-family: Georgia, 'Times New Roman', serif;}

#daysNumber {
  font-size: 100px;
  background: linear-gradient(45deg, #ffc1cc, #ffb6c1, #ff9eb1, #ff85a1);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  animation: popIn 600ms ease;
}

#daysText { font-size: 24px; color: #ff4f91; margin-top:10px; letter-spacing:0.4px;}

@keyframes popIn {
  0% {transform:scale(0.85); opacity:0;}
  100%{transform:scale(1); opacity:1;}
}

#notesArea {
  font-size:20px;
  color:#ff4f91;
  min-height:120px;
  display:flex;
  align-items:center;
  justify-content:center;
  flex-direction:column;
}

#currentNote {padding:0 16px; transition: opacity 0.5s;}
#changeNote {margin-top:15px; padding:8px 16px; border-radius:20px; background:#fff; border:none; cursor:pointer;}

#specialDays h2 {color:#ff4f91;}
#specialDays ul {list-style:none; padding:0; margin:0 auto; max-width:600px;}

#specialDays li {
  margin:12px;
  padding:12px;
  border-radius:12px;
  box-shadow:0 4px 10px rgba(0,0,0,0.1);
  display:flex;
  justify-content:space-between;
  align-items:center;
}

.highlight {background:#fff0f5;}
.normal {background:#f9f9f9;}

.badge {
  background:#ff6f91;
  color:#fff;
  padding:4px 10px;
  border-radius:20px;
  font-size:12px;
}

#socials {
  display:flex;
  justify-content:center;
  gap:40px;
  margin-top:50px;
}

.social-card {
  display:flex;
  flex-direction:column;
  align-items:center;
  justify-content:center;
  width:120px;
  height:120px;
  border-radius:12px;
  box-shadow:0 4px 10px rgba(0,0,0,0.1);
  background:#fff;
  transition: transform 0.3s;
  cursor:pointer;
}

.social-card:hover {transform:translateY(-6px);}
.social-card i {font-size:36px; color:#ff4f91; margin-bottom:8px;}
.social-card span {font-weight:bold;}
</style>
</head>
<body>

<canvas id="game"></canvas>
<div id="ui"></div>

<div id="menu">
  <button onclick="showSection('days')">Gün Sayacı 📅</button>
  <button onclick="showSection('notes')">Sevgili Notları 💌</button>
  <button onclick="showSection('special')">Özel Günler 🎉</button>
  <button onclick="showSection('socials')">Sosyal Medya 🌐</button>
</div>

<div id="content">
  <div id="daysCounter">
    <div id="daysNumber">{{ days }}</div>
    <div id="daysText">gündür birlikteyiz 💖</div>
  </div>

  <div id="notesArea">
    <div id="currentNote"></div>
    <button id="changeNote" onclick="nextNote()">💌 Yeni Not</button>
  </div>

  <div id="specialDays">
    <h2>Özel Günlerimiz ✨</h2>
    <ul>
      {% for name, dm in special_dates.items() %}
      {% set target = next_occurrence(dm[0], dm[1]) %}
      <li class="{% if 'Doğum Günü' in name %}highlight{% else %}normal{% endif %}">
        <div>
          <strong style="color:#ff6f91;">{{ name }}</strong><br>
          <span>{{ format_date_tr(target) }}</span>
        </div>
        <span class="badge">{{ days_until(target) }} gün kaldı</span>
      </li>
      {% endfor %}
    </ul>
  </div>

  <div id="socials">
    <div class="social-card" onclick="window.open('https://www.tiktok.com/@hz.roxy','_blank')">
      <i class="fab fa-tiktok"></i><span>Kurucu</span>
    </div>
    <div class="social-card" onclick="window.open('https://www.instagram.com/hzroxyofficial/?utm_source=ig_web_button_share_sheet','_blank')">
      <i class="fab fa-instagram"></i><span>Kurucu</span>
    </div>
    <div class="social-card" onclick="window.open('https://www.tiktok.com/@queenbusra00','_blank')">
      <i class="fab fa-tiktok"></i><span>Büşra</span>
    </div>
    <div class="social-card" onclick="window.open('https://www.instagram.com/bus.ra9896/?utm_source=ig_web_button_share_sheet','_blank')">
      <i class="fab fa-instagram"></i><span>Büşra</span>
    </div>
  </div>
</div>

<div id="musicToggle" onclick="toggleMusic()">🎵</div>
<div id="nightToggle" onclick="toggleNight()">🌙/☀️</div>

<audio id="music" loop>
  <source src="https://cdn.pixabay.com/download/audio/2022/03/15/audio_7b7f0c6a53.mp3" type="audio/mpeg">
</audio>

<script>
const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");
const music = document.getElementById("music");
let musicOn = false;
let nightMode = false;
let w,h;

function resize(){
  w = canvas.width = window.innerWidth;
  h = canvas.height = window.innerHeight;
}
window.addEventListener("resize", resize);
resize();

let bgHearts = Array.from({length:18},()=>({
  x:Math.random()*w,
  y:Math.random()*h,
  speed:0.3+Math.random()
}));

function showSection(section){
  ["daysCounter","notesArea","specialDays","socials"].forEach(id=>{
    document.getElementById(id).style.display="none";
  });
  if(section==="days") daysCounter.style.display="block";
  if(section==="notes") notesArea.style.display="flex";
  if(section==="special") specialDays.style.display="block";
  if(section==="socials") socials.style.display="flex";
}

function toggleMusic(){
  musicOn=!musicOn;
  if(musicOn) music.play().catch(()=>{});
  else music.pause();
}

function toggleNight(){
  nightMode=!nightMode;
  document.body.style.background = nightMode ? "#1c1c2b" : "#fdeff2";
}

function drawHearts(){
  ctx.clearRect(0,0,w,h);
  bgHearts.forEach(hh=>{
    hh.y+=hh.speed;
    if(hh.y>h){hh.y=-20;hh.x=Math.random()*w;}
    ctx.font="18px serif";
    ctx.fillText("💗",hh.x,hh.y);
  });
  requestAnimationFrame(drawHearts);
}
drawHearts();

let currentNoteIndex = 0;
const notes = {{ notes|tojson }};

function nextNote(){
  currentNoteIndex=(currentNoteIndex+1)%notes.length;
  const noteDiv=document.getElementById("currentNote");
  noteDiv.style.opacity=0;
  setTimeout(()=>{
    noteDiv.innerText=notes[currentNoteIndex];
    noteDiv.style.opacity=1;
  },500);
}

document.getElementById("currentNote").innerText = notes[currentNoteIndex];

function updateClock(){
  document.getElementById("ui").innerText =
    new Date().toLocaleString("tr-TR");
}
setInterval(updateClock,1000);
updateClock();

showSection("notes");
</script>

</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(
        HTML,
        days=days_together(),
        notes=NOTES,
        special_dates=SPECIAL_DATES,
        days_until=days_until,
        format_date_tr=format_date_tr,
        next_occurrence=next_occurrence
    )

if __name__ == "__main__":
    app.run(debug=False)
