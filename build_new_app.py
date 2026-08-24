import os
import json
import base64
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import datetime

PASSWORD = b"suripamuk2026"

with open("data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Extract data for the narrative
traits = [
    ["Unsere Nächte", "Egal wie spät es war, zwischen 2 und 5 Uhr morgens hatten wir unsere ehrlichsten, lustigsten und intimsten Gespräche."],
    ["Suri & Pamuk", "Die wahren Herrscherinnen unseres Lebens. Wenn Suri auf dir liegt, bleibt die Welt eben stehen."],
    ["Unsere Eisliebe", "Über 2.400 mal haben wir von Eis geredet. Du bist meine süßeste Versuchung."],
    ["Die kleinen Dinge", "Wenn wir zusammenziehen, haben wir alles doppelt, weil wir immer denselben Geschmack haben."]
]

affirmations = [
    "Dein Lächeln.",
    "Deine Stimme.",
    "Deine Augen.",
    "Unsere Momente.",
    "Für immer."
]

js_content = f"""
const story = {{
  traits: {json.dumps(traits)},
  moments: {json.dumps([[m['date'], m['sender'] + ' sagte:', m['text']] for m in data['lateNight']['romantic'][:25]])},
  spotify: {json.dumps(data['spotify'][:40])},
  affirmations: {json.dumps(affirmations)},
  promises: {json.dumps(data['promises'])}
}};
"""

app_js = """
const $ = (selector, scope = document) => scope.querySelector(selector);
const $all = (selector, scope = document) => [...scope.querySelectorAll(selector)];
const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

function populateContent() {
  $('#traits-list').innerHTML = story.traits.map(([title, copy], index) => `<article class="trait reveal"><span>${String(index + 1).padStart(2, '0')}</span><h3>${title}</h3><p>${copy}</p></article>`).join('');
  
  $('#moments-list').innerHTML = story.moments.map(([date, text, quote], index) => `<article class="moment reveal"><span class="moment-index">${String(index + 1).padStart(2, '0')}</span><div><p class="moment-date">${date}</p><h3>${text}</h3><blockquote>${quote}</blockquote></div></article>`).join('');
  
  $('#spotify-list').innerHTML = story.spotify.map(s => `<article class="spotify-track reveal"><iframe src="${s.embedUrl}" width="100%" height="152" frameBorder="0" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy" style="border-radius:12px;"></iframe><p class="track-quote">"${s.msg}"</p><span class="track-sender">— ${s.sender}</span></article>`).join('');

  $('#promises-list').innerHTML = story.promises.map(p => `<article class="promise reveal"><div class="promise-seal">${p.seal}</div><h3>${p.title}</h3><p>${p.text}</p><small>${p.status}</small></article>`).join('');

  $('#affirmations').innerHTML = story.affirmations.map(word => `<p class="affirmation reveal">${word}</p>`).join('');
}

function revealOnScroll() {
  const observer = new IntersectionObserver(entries => entries.forEach(entry => {
    if (entry.isIntersecting) { entry.target.classList.add('is-visible'); observer.unobserve(entry.target); }
  }), { threshold: 0.1, rootMargin: '0px 0px -5% 0px' });
  $all('.reveal').forEach(el => observer.observe(el));
}

function createParticles() {
  const pContainer = $('.particles');
  for (let i = 0; i < 40; i++) {
    const el = document.createElement('i');
    el.style.left = Math.random() * 100 + '%';
    el.style.animationDuration = (Math.random() * 20 + 10) + 's';
    el.style.animationDelay = (Math.random() * 5) + 's';
    pContainer.appendChild(el);
  }
}

function interactions() {
  if (!reduceMotion && matchMedia('(pointer:fine)').matches) {
    document.addEventListener('pointermove', ({ clientX, clientY }) => { 
      document.documentElement.style.setProperty('--mx', `${clientX / innerWidth * 100}%`); 
      document.documentElement.style.setProperty('--my', `${clientY / innerHeight * 100}%`); 
    });
  }
  
  $('#final-button').addEventListener('click', () => { 
    $('#last-message').innerHTML = '<h2>Ich liebe dich, Pepsi. <em>♥</em></h2><p>Auf unsere 150 Jahre.</p><small>Dein Denis.</small>'; 
    $('#last-message').classList.add('is-open'); 
  });
}

function initApp() {
  populateContent();
  revealOnScroll();
  createParticles();
  interactions();
  
  // Play entrance animation
  const intro = $('#intro');
  if (intro) {
    intro.classList.add('is-opening');
    setTimeout(() => intro.classList.add('is-card'), 250);
    setTimeout(() => { intro.classList.add('is-finished'); $('#story').removeAttribute('aria-hidden'); window.scrollTo(0, 0); }, 1300);
  } else {
    $('#story').removeAttribute('aria-hidden');
  }
}

initApp();
"""

app_css = """
:root {
  --bg: #0b1320;
  --text: #f0f4f8;
  --text-muted: #94a3b8;
  --gold: #e5b869;
  --rose: #ff4d6d;
  --font-main: 'DM Sans', sans-serif;
  --font-serif: 'Playfair Display', serif;
}

* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  background: var(--bg);
  color: var(--text);
  font-family: var(--font-main);
  line-height: 1.6;
  overflow-x: hidden;
  background-image: radial-gradient(circle at var(--mx, 50%) var(--my, 50%), rgba(229,184,105,0.06) 0%, transparent 50%);
}

.particles {
  position: fixed; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: -1;
}
.particles i {
  position: absolute; display: block; width: 4px; height: 4px; background: var(--gold); border-radius: 50%; opacity: 0.3;
  animation: floatUp infinite linear;
}

@keyframes floatUp {
  0% { transform: translateY(100vh) scale(0.5); opacity: 0; }
  10% { opacity: 0.8; }
  90% { opacity: 0.8; }
  100% { transform: translateY(-10vh) scale(1.5); opacity: 0; }
}

.story { max-width: 800px; margin: 0 auto; padding: 20px; }
.section { padding: 12vh 0; min-height: 60vh; display: flex; flex-direction: column; justify-content: center; }

.eyebrow { font-size: 0.9rem; text-transform: uppercase; letter-spacing: 2px; color: var(--gold); margin-bottom: 10px; font-weight: bold; }
.display { font-family: var(--font-serif); font-size: 4rem; line-height: 1.1; margin-bottom: 20px; }
.display em { color: var(--rose); font-style: italic; font-weight: normal; }

.reveal { opacity: 0; transform: translateY(40px); transition: all 1s cubic-bezier(0.16, 1, 0.3, 1); }
.reveal.is-visible { opacity: 1; transform: translateY(0); }

.traits-list, .promises-list { margin-top: 40px; display: grid; gap: 30px; }
.moments-list, .spotify-list { margin-top: 40px; display: flex; flex-direction: column; gap: 30px; }

.trait, .moment, .promise, .spotify-track {
  background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); padding: 30px; border-radius: 20px;
  backdrop-filter: blur(10px); transition: transform 0.3s ease, border-color 0.3s ease, box-shadow 0.3s ease;
}
.trait:hover, .moment:hover, .promise:hover, .spotify-track:hover { 
  transform: translateY(-5px); border-color: rgba(229,184,105,0.3); box-shadow: 0 10px 30px rgba(0,0,0,0.5); 
}

.trait span, .moment-index { font-size: 3rem; color: var(--gold); font-family: var(--font-serif); opacity: 0.3; display: block; margin-bottom: 10px; line-height: 1;}
.trait h3, .promise h3 { font-size: 1.6rem; margin-bottom: 12px; font-family: var(--font-serif); }
.moment h3 { font-size: 1.2rem; color: var(--rose); margin-bottom: 8px; }
.moment blockquote { font-style: italic; font-size: 1.15rem; color: var(--text-muted); border-left: 3px solid var(--gold); padding-left: 18px; line-height: 1.7; }
.moment-date { font-size: 0.8rem; color: var(--gold); letter-spacing: 1px; margin-bottom: 5px; opacity: 0.8; }

.spotify-track { padding: 20px; }
.track-quote { font-style: italic; margin-top: 15px; color: var(--text-main); font-size: 1.1rem;}
.track-sender { font-size: 0.85rem; color: var(--gold); text-transform: uppercase; letter-spacing: 1.5px; display: block; margin-top: 8px;}

.promise-seal { font-size: 4rem; margin-bottom: 15px; text-align: center; display: block; }
.promise p { font-size: 1.1rem; margin-bottom: 15px; }
.promise small { color: var(--gold); text-transform: uppercase; letter-spacing: 1px; font-weight: bold; font-size: 0.8rem; }

.affirmations { display: flex; flex-direction: column; align-items: center; gap: 30px; font-size: 3rem; font-family: var(--font-serif); font-style: italic; margin: 15vh 0; }
.affirmations p { color: var(--rose); text-align: center; line-height: 1.2; }

.final-button { 
  display: block; margin: 60px auto 20px; padding: 18px 50px; background: transparent; color: var(--gold); 
  border: 1px solid var(--gold); border-radius: 40px; font-size: 1.2rem; cursor: pointer; transition: all 0.3s; 
}
.final-button:hover { background: var(--gold); color: #000; box-shadow: 0 0 25px rgba(229,184,105,0.4); transform: scale(1.05); }

.last-message { text-align: center; opacity: 0; transform: translateY(20px); transition: all 1s; display: none; }
.last-message.is-open { display: block; opacity: 1; transform: translateY(0); margin-top: 40px; }
.last-message h2 { font-size: 3.5rem; font-family: var(--font-serif); color: var(--rose); margin-bottom: 15px; line-height: 1.1; }
.last-message p { font-size: 1.3rem; margin-bottom: 10px; }

@media (max-width: 768px) {
  .display { font-size: 2.8rem; }
  .section { padding: 8vh 0; }
  .trait, .moment, .promise, .spotify-track { padding: 20px; }
  .affirmations { font-size: 2.2rem; }
}
"""

full_html = f"""
<!doctype html>
<html lang="de">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta name="robots" content="noindex,nofollow" />
  <title>Für Pepsi</title>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&family=Playfair+Display:ital,wght@0,500;0,700;1,500;1,700&display=swap" rel="stylesheet" />
  <style>
    {app_css}
  </style>
</head>
<body>
  <div class="particles" aria-hidden="true"></div>
  <main class="story" id="story" aria-hidden="true">
    
    <header class="section hero">
      <p class="eyebrow reveal">Ein kleiner digitaler Brief</p>
      <h1 class="display reveal">Für<br /><em>Pepsi.</em></h1>
      <p class="hero-copy reveal" style="font-size: 1.2rem; max-width: 500px;">Eine Reise durch unsere schönsten Momente, tiefsten Nächte und unendlichen Versprechen.</p>
      <p class="quiet reveal" style="margin-top:50px; opacity: 0.5; text-transform:uppercase; letter-spacing:2px; font-size:0.8rem;">Scroll, Schnecke ↓</p>
    </header>

    <section class="section">
      <p class="eyebrow reveal">Kapitel 01</p>
      <h2 class="display reveal">Wie ich<br /><em>uns sehe.</em></h2>
      <div id="traits-list" class="traits-list"></div>
    </section>

    <section class="section">
      <p class="eyebrow reveal">Kapitel 02</p>
      <h2 class="display reveal">Late Night<br /><em>Whispers.</em></h2>
      <p class="reveal text-muted">Wenn die Welt schlief, waren wir am wachsten.</p>
      <div id="moments-list" class="moments-list"></div>
    </section>

    <section class="section">
      <p class="eyebrow reveal">Kapitel 03</p>
      <h2 class="display reveal">Unser<br /><em>Soundtrack.</em></h2>
      <p class="reveal text-muted" style="max-width: 500px;">Die Lieder, die wir uns geschickt haben. Keine Duplikate, nur pure Vibes. (Eine vertikale Playlist zum Scrollen und Hören).</p>
      <div id="spotify-list" class="spotify-list"></div>
    </section>

    <section class="section">
      <p class="eyebrow reveal">Kapitel 04</p>
      <h2 class="display reveal">Unsere<br /><em>Versprechen.</em></h2>
      <div id="promises-list" class="promises-list"></div>
    </section>

    <section class="section crescendo" id="crescendo">
      <div id="affirmations" class="affirmations"></div>
      <div style="text-align:center; margin-top:15vh;" class="reveal">
        <p class="eyebrow">Und vor allem:</p>
        <h2 class="display">Ich bin unglaublich stolz auf dich.</h2>
      </div>
      
      <button id="final-button" class="final-button reveal" type="button">Noch eine Sache …</button>
      <div id="last-message" class="last-message" aria-live="polite"></div>
    </section>

  </main>
  
  <script>
    {js_content}
    {app_js}
  </script>
</body>
</html>
"""

# Encrypt
salt = os.urandom(16)
iv = os.urandom(12)
iterations = 100000

kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=iterations,
)
key = kdf.derive(PASSWORD)

aesgcm = AESGCM(key)
raw_data = json.dumps({'html': full_html}).encode('utf-8')

ciphertext = aesgcm.encrypt(iv, raw_data, None)
actual_ciphertext = ciphertext[:-16]
tag = ciphertext[-16:]

payload = {
    'salt': base64.b64encode(salt).decode('ascii'),
    'iv': base64.b64encode(iv).decode('ascii'),
    'data': base64.b64encode(actual_ciphertext).decode('ascii'),
    'tag': base64.b64encode(tag).decode('ascii'),
    'iterations': iterations
}

with open("pepsi.enc", "w", encoding="utf-8") as f:
    json.dump(payload, f)

print("Generated and encrypted pepsi.enc successfully!")
