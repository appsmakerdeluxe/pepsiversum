import os
import json
import base64
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

PASSWORD = b"suripamuk2026"

with open("data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

js_data = json.dumps(data)

app_js = "const appData = " + js_data + """;
const $ = (selector, scope = document) => scope.querySelector(selector);
const $all = (selector, scope = document) => [...scope.querySelectorAll(selector)];

// Web Audio API for interactive sounds
const audioCtx = new (window.AudioContext || window.webkitAudioContext)();

function playMeow() {
  if(audioCtx.state === 'suspended') audioCtx.resume();
  const osc = audioCtx.createOscillator();
  const gain = audioCtx.createGain();
  osc.connect(gain); gain.connect(audioCtx.destination);
  osc.type = 'sine';
  osc.frequency.setValueAtTime(500, audioCtx.currentTime);
  osc.frequency.exponentialRampToValueAtTime(1200, audioCtx.currentTime + 0.2);
  osc.frequency.exponentialRampToValueAtTime(800, audioCtx.currentTime + 0.5);
  gain.gain.setValueAtTime(0, audioCtx.currentTime);
  gain.gain.linearRampToValueAtTime(0.3, audioCtx.currentTime + 0.1);
  gain.gain.linearRampToValueAtTime(0, audioCtx.currentTime + 0.5);
  osc.start(); osc.stop(audioCtx.currentTime + 0.5);
}

function playPurr() {
  if(audioCtx.state === 'suspended') audioCtx.resume();
  const bufferSize = audioCtx.sampleRate * 2; // 2 seconds
  const buffer = audioCtx.createBuffer(1, bufferSize, audioCtx.sampleRate);
  const data = buffer.getChannelData(0);
  for (let i = 0; i < bufferSize; i++) {
    data[i] = (Math.random() * 2 - 1) * 0.2; // noise
  }
  const noise = audioCtx.createBufferSource();
  noise.buffer = buffer;
  const biquad = audioCtx.createBiquadFilter();
  biquad.type = 'lowpass';
  biquad.frequency.value = 150;
  
  const gain = audioCtx.createGain();
  gain.gain.setValueAtTime(0, audioCtx.currentTime);
  
  // Create a pulsing effect for the purr using an oscillator modulating the gain
  const lfo = audioCtx.createOscillator();
  lfo.type = 'sine';
  lfo.frequency.value = 25; // 25 Hz rumble
  
  const lfoGain = audioCtx.createGain();
  lfoGain.gain.value = 0.5;
  lfo.connect(lfoGain);
  lfoGain.connect(gain.gain);
  
  noise.connect(biquad);
  biquad.connect(gain);
  gain.connect(audioCtx.destination);
  
  gain.gain.linearRampToValueAtTime(0.6, audioCtx.currentTime + 0.2);
  gain.gain.linearRampToValueAtTime(0, audioCtx.currentTime + 1.8);
  
  noise.start(); lfo.start();
  noise.stop(audioCtx.currentTime + 2); lfo.stop(audioCtx.currentTime + 2);
}

function playPop() {
  if(audioCtx.state === 'suspended') audioCtx.resume();
  const osc = audioCtx.createOscillator();
  const gain = audioCtx.createGain();
  osc.connect(gain); gain.connect(audioCtx.destination);
  osc.type = 'sine';
  osc.frequency.setValueAtTime(400, audioCtx.currentTime);
  osc.frequency.exponentialRampToValueAtTime(100, audioCtx.currentTime + 0.1);
  gain.gain.setValueAtTime(0.3, audioCtx.currentTime);
  gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.1);
  osc.start(); osc.stop(audioCtx.currentTime + 0.1);
}

function renderApp() {
  // 1. Late Night
  const romanticMsgs = appData.lateNight.romantic.slice(0, 10).map((m, i) => `
    <div class="chat-bubble ${m.sender === 'Denis' ? 'right' : 'left'} reveal" style="transition-delay: ${i * 0.1}s">
      <div class="chat-meta">${m.date} • ${m.time}</div>
      <div class="chat-text">${m.text}</div>
    </div>
  `).join('');
  $('#latenight-container').innerHTML = romanticMsgs;

  // 2. Spotify
  const tracks = appData.spotify.slice(0, 15).map(s => `
    <div class="spotify-card reveal">
      <iframe src="${s.embedUrl}" width="100%" height="152" frameBorder="0" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe>
      <p class="track-quote">"${s.msg}"</p>
      <span class="track-sender">— ${s.sender}</span>
    </div>
  `).join('');
  $('#spotify-container').innerHTML = tracks;

  // 3. Kintsugi
  const kintsugi = appData.kintsugi.map(k => `
    <div class="kintsugi-card reveal">
      <h3>✨ ${k.title}</h3>
      <div class="meta">${k.date}</div>
      <blockquote>"${k.quote}"</blockquote>
      <p class="lesson">${k.lesson}</p>
    </div>
  `).join('');
  $('#kintsugi-container').innerHTML = kintsugi;

  // 4. Cats
  // Add listeners to cat buttons
  $all('.cat-sound').forEach(btn => {
    btn.addEventListener('click', (e) => {
      if(e.target.dataset.type === 'meow') playMeow();
      else playPurr();
      
      // Floating heart effect
      const heart = document.createElement('div');
      heart.innerHTML = '❤️';
      heart.className = 'floating-heart';
      heart.style.left = e.clientX + 'px';
      heart.style.top = e.clientY + 'px';
      document.body.appendChild(heart);
      setTimeout(() => heart.remove(), 2000);
    });
  });

  // 5. Eislabor & Date Roulette
  const btnRoulette = $('#btn-roulette');
  const rouletteResult = $('#roulette-result');
  btnRoulette.addEventListener('click', () => {
    playPop();
    rouletteResult.classList.remove('show');
    btnRoulette.disabled = true;
    btnRoulette.textContent = 'Mische Ideen...';
    
    let ticks = 0;
    const interval = setInterval(() => {
      const randomDate = appData.iceCreamLab.dates[Math.floor(Math.random() * appData.iceCreamLab.dates.length)];
      rouletteResult.innerHTML = `<h4>${randomDate.title}</h4><p>${randomDate.desc}</p>`;
      rouletteResult.classList.add('show');
      ticks++;
      if (ticks > 10) {
        clearInterval(interval);
        btnRoulette.disabled = false;
        btnRoulette.textContent = 'Neues Date ziehen 🎲';
        // Confetti
        createConfetti(btnRoulette.getBoundingClientRect());
      }
    }, 100);
  });

  // 6. Blueprint
  const rooms = appData.blueprint.map(r => `
    <div class="room-card reveal">
      <div class="room-icon">${r.icon}</div>
      <h3>${r.name}</h3>
      <ul>
        ${r.items.map(item => `<li><strong>${item.name}:</strong> ${item.desc} <br><small><i>${item.quote}</i></small></li>`).join('')}
      </ul>
    </div>
  `).join('');
  $('#blueprint-container').innerHTML = rooms;

  // 7. Safe Harbor SOS
  const sosContainer = $('#sos-buttons');
  const modal = $('#sos-modal');
  appData.safeHarbor.forEach(s => {
    const btn = document.createElement('button');
    btn.className = 'sos-btn reveal';
    btn.innerHTML = `<span class="icon">${s.icon}</span> <span class="title">${s.title}</span>`;
    btn.addEventListener('click', () => {
      playPop();
      $('#modal-title').textContent = s.title;
      $('#modal-advice').textContent = s.advice;
      $('#modal-quote').textContent = s.quote;
      $('#modal-action').textContent = s.actionText;
      $('#modal-bonus').textContent = "🎁 " + s.bonus;
      modal.classList.add('active');
    });
    sosContainer.appendChild(btn);
  });

  $('#modal-close').addEventListener('click', () => {
    modal.classList.remove('active');
  });

  // 8. Promises
  const promises = appData.promises.map(p => `
    <div class="promise-card reveal">
      <div class="seal">${p.seal}</div>
      <h3>${p.title}</h3>
      <p>${p.text}</p>
      <div class="status">${p.status}</div>
    </div>
  `).join('');
  $('#promises-container').innerHTML = promises;

  // 9. Timeline
  const timeline = appData.timeline.map((t, i) => `
    <div class="timeline-item ${i % 2 === 0 ? 'left' : 'right'} reveal">
      <div class="content">
        <span class="year">${t.year}</span>
        <h3>${t.title}</h3>
        <p>${t.desc}</p>
      </div>
    </div>
  `).join('');
  $('#timeline-container').innerHTML = timeline;

  // 10. Quiz Logic
  let currentQ = 0;
  let score = 0;
  const questions = appData.quiz.slice(0, 5); // 5 questions for brevity
  const renderQuiz = () => {
    if(currentQ >= questions.length) {
      $('#quiz-container').innerHTML = `
        <div class="quiz-result reveal">
          <h3>Quiz Beendet! 🎉</h3>
          <p>Du hast ${score} von ${questions.length} richtig!</p>
          <div class="secret-message">
            ${score === questions.length ? "Perfekt! Du bist mein absoluter Lieblingsmensch. ♥" : "Fast perfekt! Ich liebe dich trotzdem unendlich. ♥"}
          </div>
          <button id="btn-restart-quiz" class="action-btn">Nochmal spielen</button>
        </div>
      `;
      $('#btn-restart-quiz').addEventListener('click', () => { currentQ = 0; score = 0; renderQuiz(); playPop(); });
      return;
    }
    
    const q = questions[currentQ];
    $('#quiz-container').innerHTML = `
      <div class="quiz-card reveal">
        <span class="step">Frage ${currentQ + 1} von ${questions.length}</span>
        <h3 class="question">${q.q}</h3>
        <div class="options">
          ${q.options.map((opt, i) => `<button class="quiz-opt" data-idx="${i}">${opt}</button>`).join('')}
        </div>
      </div>
    `;
    
    $all('.quiz-opt').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const chosen = parseInt(e.target.dataset.idx);
        if(chosen === q.answer) {
          e.target.classList.add('correct');
          score++;
          playPop();
        } else {
          e.target.classList.add('wrong');
          $all('.quiz-opt')[q.answer].classList.add('correct');
        }
        $all('.quiz-opt').forEach(b => b.disabled = true);
        
        setTimeout(() => {
          currentQ++;
          renderQuiz();
        }, 1500);
      });
    });
  };
  renderQuiz();

}

function createConfetti(rect) {
  for(let i=0; i<30; i++) {
    const c = document.createElement('div');
    c.className = 'confetti';
    c.style.left = rect.left + (Math.random() * rect.width) + 'px';
    c.style.top = rect.top + 'px';
    c.style.backgroundColor = ['#e5b869', '#ff4d6d', '#9d4edd', '#0ecbb5'][Math.floor(Math.random()*4)];
    document.body.appendChild(c);
    
    const angle = Math.random() * Math.PI * 2;
    const velocity = 50 + Math.random() * 50;
    const tx = Math.cos(angle) * velocity;
    const ty = Math.sin(angle) * velocity - 50;
    
    c.animate([
      { transform: 'translate(0,0) rotate(0)', opacity: 1 },
      { transform: `translate(${tx}px, ${ty}px) rotate(${Math.random()*360}deg)`, opacity: 0 }
    ], { duration: 1000, easing: 'cubic-bezier(0,0,0.2,1)' });
    
    setTimeout(() => c.remove(), 1000);
  }
}

function initObserver() {
  const observer = new IntersectionObserver(entries => entries.forEach(entry => {
    if (entry.isIntersecting) { 
      entry.target.classList.add('is-visible'); 
      observer.unobserve(entry.target); 
    }
  }), { threshold: 0.1, rootMargin: '0px 0px -50px 0px' });
  
  $all('.reveal').forEach(el => observer.observe(el));
}

renderApp();
initObserver();
"""

app_css = """
:root {
  --bg: #090a0f;
  --panel-bg: rgba(20, 24, 35, 0.6);
  --text: #f0f4f8;
  --text-muted: #a1b0c0;
  --gold: #e5b869;
  --rose: #ff4d6d;
  --purple: #9d4edd;
  --mint: #0ecbb5;
  --denis: #1d3557;
  --pepsi: #4a1c40;
}

* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  background: var(--bg);
  color: var(--text);
  font-family: 'DM Sans', sans-serif;
  line-height: 1.6;
  overflow-x: hidden;
}

.particles {
  position: fixed; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: -1;
  background-image: radial-gradient(circle at 50% 50%, rgba(229,184,105,0.05) 0%, transparent 60%);
}

.container { max-width: 900px; margin: 0 auto; padding: 20px; }
.section { padding: 10vh 0; min-height: 50vh; border-bottom: 1px solid rgba(255,255,255,0.05); }
.section:last-child { border-bottom: none; }

.chapter-tag { font-family: 'DM Mono', monospace; color: var(--gold); text-transform: uppercase; letter-spacing: 2px; font-size: 0.9rem; margin-bottom: 10px; display: block; }
h2.title { font-family: 'Playfair Display', serif; font-size: 3.5rem; line-height: 1.1; margin-bottom: 20px; }
h2.title em { color: var(--rose); font-style: italic; }
.section-desc { font-size: 1.2rem; color: var(--text-muted); margin-bottom: 40px; max-width: 600px; }

.reveal { opacity: 0; transform: translateY(30px); transition: all 0.8s cubic-bezier(0.16, 1, 0.3, 1); }
.reveal.is-visible { opacity: 1; transform: translateY(0); }

/* 1. Late Night */
.chat-container { display: flex; flex-direction: column; gap: 15px; }
.chat-bubble { max-width: 80%; padding: 15px 20px; border-radius: 20px; position: relative; }
.chat-bubble.left { align-self: flex-start; background: var(--pepsi); border-bottom-left-radius: 5px; }
.chat-bubble.right { align-self: flex-end; background: var(--denis); border-bottom-right-radius: 5px; }
.chat-meta { font-size: 0.75rem; color: rgba(255,255,255,0.5); margin-bottom: 5px; }
.chat-text { font-size: 1.1rem; }

/* 2. Spotify */
.spotify-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px; }
.spotify-card { background: var(--panel-bg); padding: 15px; border-radius: 16px; border: 1px solid rgba(255,255,255,0.08); }
.track-quote { font-style: italic; margin: 15px 0 5px; color: var(--text-muted); }
.track-sender { font-size: 0.8rem; color: var(--gold); text-transform: uppercase; }

/* 3. Kintsugi */
.kintsugi-grid { display: grid; gap: 20px; }
.kintsugi-card { background: linear-gradient(145deg, rgba(30,30,40,0.8), rgba(15,15,20,0.9)); border-left: 3px solid var(--gold); padding: 25px; border-radius: 12px; }
.kintsugi-card h3 { color: var(--gold); margin-bottom: 5px; }
.kintsugi-card .meta { font-size: 0.8rem; opacity: 0.6; margin-bottom: 15px; }
.kintsugi-card blockquote { font-size: 1.2rem; font-style: italic; margin-bottom: 15px; }

/* 4. Cats */
.cats-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 30px; }
@media(max-width: 600px) { .cats-grid { grid-template-columns: 1fr; } }
.cat-card { background: var(--panel-bg); border-radius: 24px; overflow: hidden; text-align: center; border: 1px solid rgba(255,255,255,0.1); }
.cat-img { width: 100%; height: 250px; object-fit: cover; }
.cat-info { padding: 20px; }
.cat-info h3 { font-size: 2rem; font-family: 'Playfair Display'; margin-bottom: 15px; }
.cat-sound { background: var(--bg); border: 1px solid var(--gold); color: var(--gold); padding: 10px 20px; border-radius: 30px; cursor: pointer; margin: 5px; transition: 0.3s; }
.cat-sound:hover { background: var(--gold); color: #000; }

/* 5. Date Roulette */
.roulette-box { text-align: center; padding: 40px; background: var(--panel-bg); border-radius: 24px; border: 1px dashed var(--rose); }
.action-btn { background: linear-gradient(135deg, var(--rose), var(--purple)); color: #fff; border: none; padding: 15px 35px; border-radius: 30px; font-size: 1.2rem; font-weight: bold; cursor: pointer; transition: 0.3s; box-shadow: 0 10px 20px rgba(255,77,109,0.3); }
.action-btn:hover { transform: translateY(-3px); box-shadow: 0 15px 25px rgba(255,77,109,0.5); }
#roulette-result { margin-top: 30px; padding: 20px; background: rgba(0,0,0,0.5); border-radius: 12px; display: none; }
#roulette-result.show { display: block; animation: popIn 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275); }
@keyframes popIn { 0% { transform: scale(0.8); opacity: 0; } 100% { transform: scale(1); opacity: 1; } }

/* 6. Blueprint */
.blueprint-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; }
.room-card { background: var(--panel-bg); padding: 25px; border-radius: 16px; border: 1px solid rgba(255,255,255,0.05); }
.room-icon { font-size: 3rem; margin-bottom: 15px; }
.room-card ul { list-style: none; margin-top: 15px; display: flex; flex-direction: column; gap: 15px; }
.room-card li { font-size: 0.95rem; }

/* 7. Safe Harbor */
.sos-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
@media(max-width: 600px) { .sos-grid { grid-template-columns: 1fr; } }
.sos-btn { background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.2); padding: 30px 20px; border-radius: 20px; color: #fff; cursor: pointer; display: flex; flex-direction: column; align-items: center; gap: 15px; transition: 0.3s; }
.sos-btn:hover { background: rgba(255,255,255,0.1); transform: scale(1.05); border-color: var(--mint); }
.sos-btn .icon { font-size: 2.5rem; }
.sos-btn .title { font-size: 1.1rem; font-weight: bold; }

/* Modal */
.modal { position: fixed; inset: 0; background: rgba(0,0,0,0.8); backdrop-filter: blur(10px); z-index: 100; display: flex; align-items: center; justify-content: center; opacity: 0; pointer-events: none; transition: 0.4s; }
.modal.active { opacity: 1; pointer-events: all; }
.modal-content { background: var(--bg); padding: 40px; border-radius: 24px; max-width: 500px; width: 90%; text-align: center; border: 1px solid var(--mint); box-shadow: 0 0 40px rgba(14,203,181,0.2); transform: translateY(50px); transition: 0.4s; }
.modal.active .modal-content { transform: translateY(0); }
.modal-content h3 { font-size: 2rem; color: var(--mint); margin-bottom: 20px; }
.modal-content p { font-size: 1.2rem; margin-bottom: 20px; }
.modal-content blockquote { font-style: italic; color: var(--gold); margin-bottom: 20px; font-size: 1.1rem; }
.bonus { display: inline-block; background: rgba(255,255,255,0.1); padding: 10px 20px; border-radius: 30px; font-size: 0.9rem; margin-bottom: 30px; }

/* 8. Promises */
.promises-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px; }
.promise-card { background: linear-gradient(135deg, rgba(229,184,105,0.1), transparent); border: 1px solid rgba(229,184,105,0.3); padding: 30px; border-radius: 20px; text-align: center; }
.promise-card .seal { font-size: 3rem; margin-bottom: 15px; }
.promise-card h3 { font-family: 'Playfair Display'; font-size: 1.5rem; margin-bottom: 15px; }
.promise-card .status { margin-top: 15px; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 2px; color: var(--gold); }

/* 9. Timeline */
.timeline { position: relative; max-width: 800px; margin: 0 auto; }
.timeline::after { content: ''; position: absolute; width: 2px; background: rgba(255,255,255,0.1); top: 0; bottom: 0; left: 50%; margin-left: -1px; }
.timeline-item { padding: 10px 40px; position: relative; background: inherit; width: 50%; }
.timeline-item.left { left: 0; text-align: right; }
.timeline-item.right { left: 50%; }
.timeline-item::after { content: ''; position: absolute; width: 16px; height: 16px; right: -8px; background: var(--bg); border: 4px solid var(--rose); top: 15px; border-radius: 50%; z-index: 1; }
.timeline-item.right::after { left: -8px; }
.timeline-item .content { padding: 20px; background: var(--panel-bg); border-radius: 16px; display: inline-block; width: 100%; text-align: left; }
.timeline-item .year { color: var(--rose); font-weight: bold; margin-bottom: 10px; display: block; font-family: 'DM Mono'; }
@media (max-width: 600px) {
  .timeline::after { left: 31px; }
  .timeline-item { width: 100%; padding-left: 70px; padding-right: 25px; }
  .timeline-item.left, .timeline-item.right { left: 0; text-align: left; }
  .timeline-item.left::after, .timeline-item.right::after { left: 23px; }
}

/* 10. Quiz */
.quiz-box { max-width: 600px; margin: 0 auto; text-align: center; }
.quiz-card { background: var(--panel-bg); padding: 40px 20px; border-radius: 24px; border: 1px solid rgba(255,255,255,0.1); }
.quiz-card .step { font-size: 0.85rem; color: var(--gold); text-transform: uppercase; letter-spacing: 2px; margin-bottom: 20px; display: block; }
.quiz-card .question { font-size: 1.5rem; margin-bottom: 30px; font-family: 'Playfair Display'; }
.options { display: flex; flex-direction: column; gap: 15px; }
.quiz-opt { background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.2); color: #fff; padding: 15px; border-radius: 12px; font-size: 1.1rem; cursor: pointer; transition: 0.3s; }
.quiz-opt:hover { background: rgba(255,255,255,0.1); }
.quiz-opt.correct { background: #2a9d8f; border-color: #2a9d8f; }
.quiz-opt.wrong { background: #e76f51; border-color: #e76f51; }
.quiz-result h3 { font-size: 2.5rem; color: var(--gold); margin-bottom: 20px; font-family: 'Playfair Display'; }
.secret-message { margin: 30px 0; padding: 20px; border: 1px dashed var(--rose); border-radius: 12px; font-style: italic; font-size: 1.2rem; }

.floating-heart { position: fixed; font-size: 2rem; pointer-events: none; animation: floatHeart 2s ease-out forwards; z-index: 1000; }
@keyframes floatHeart { 0% { transform: translateY(0) scale(1); opacity: 1; } 100% { transform: translateY(-100px) scale(2); opacity: 0; } }
.confetti { position: fixed; width: 10px; height: 10px; pointer-events: none; z-index: 1000; }

"""

full_html = """
<!doctype html>
<html lang="de">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Pepsiversum</title>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=DM+Mono&family=DM+Sans:wght@400;500;700&family=Playfair+Display:ital,wght@0,500;0,700;1,500;1,700&display=swap" rel="stylesheet" />
  <style>""" + app_css + """</style>
</head>
<body>
  <div class="particles"></div>
  
  <main class="container">
    
    <!-- HEADER -->
    <header class="section" style="text-align: center; display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 80vh;">
      <span class="chapter-tag reveal">Das Pepsiversum</span>
      <h1 class="title reveal" style="font-size: 5rem;">Für <em>Pepsi.</em></h1>
      <p class="section-desc reveal" style="text-align: center; margin: 20px auto 0;">Willkommen in unserer Welt. 10 Kapitel, unzählige Erinnerungen und 150 Jahre Zukunft.</p>
    </header>

    <!-- 1. LATE NIGHT -->
    <section class="section">
      <span class="chapter-tag reveal">Kapitel 01</span>
      <h2 class="title reveal">Late Night<br><em>Whispers</em></h2>
      <p class="section-desc reveal">Zwischen 2 und 5 Uhr morgens. Wenn die Welt schlief, wurden wir wach, ehrlich und verrückt.</p>
      <div id="latenight-container" class="chat-container"></div>
    </section>

    <!-- 2. SPOTIFY -->
    <section class="section">
      <span class="chapter-tag reveal">Kapitel 02</span>
      <h2 class="title reveal">Midnight<br><em>FM</em></h2>
      <p class="section-desc reveal">Der Soundtrack unserer Chat-Historie. Jedes Lied mit seiner eigenen Erinnerung.</p>
      <div id="spotify-container" class="spotify-grid"></div>
    </section>

    <!-- 3. KINTSUGI -->
    <section class="section">
      <span class="chapter-tag reveal">Kapitel 03</span>
      <h2 class="title reveal">Aus Scherben<br><em>wird Gold</em></h2>
      <p class="section-desc reveal">In Japan repariert man Zerbrochenes mit Gold (Kintsugi). Wahre Liebe zeigt sich darin, wie man Fehler vergibt und stärker zusammenwächst.</p>
      <div id="kintsugi-container" class="kintsugi-grid"></div>
    </section>

    <!-- 4. CATS -->
    <section class="section">
      <span class="chapter-tag reveal">Kapitel 04</span>
      <h2 class="title reveal">Suri & Pamuk<br><em>Palast</em></h2>
      <p class="section-desc reveal">Die wahren Herrscherinnen. Klicke auf die Buttons für Streicheleinheiten (Sound an!).</p>
      <div class="cats-grid reveal">
        <div class="cat-card">
          <img src="https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?auto=format&fit=crop&w=600&q=80" alt="Suri" class="cat-img">
          <div class="cat-info">
            <h3>Suri</h3>
            <p style="margin-bottom: 15px; color: var(--text-muted);">Die Bett-Blockiererin & Chefin</p>
            <button class="cat-sound" data-type="meow">Süßes Miau</button>
            <button class="cat-sound" data-type="purr">Schnurren</button>
          </div>
        </div>
        <div class="cat-card">
          <img src="https://images.unsplash.com/photo-1513360371669-4adf3dd7dff8?auto=format&fit=crop&w=600&q=80" alt="Pamuk" class="cat-img">
          <div class="cat-info">
            <h3>Pamuk</h3>
            <p style="margin-bottom: 15px; color: var(--text-muted);">Der Baum-Kletterer & Chaot</p>
            <button class="cat-sound" data-type="meow">Freches Miau</button>
            <button class="cat-sound" data-type="purr">Schnurren</button>
          </div>
        </div>
      </div>
    </section>

    <!-- 5. ICE CREAM & DATES -->
    <section class="section">
      <span class="chapter-tag reveal">Kapitel 05</span>
      <h2 class="title reveal">Eislabor &<br><em>Date Roulette</em></h2>
      <p class="section-desc reveal">Über 2.400 mal Eis im Chat. Weißt du nicht, was wir als nächstes machen sollen? Dreh das Rad!</p>
      <div class="roulette-box reveal">
        <button id="btn-roulette" class="action-btn">Date-Roulette starten 🎲</button>
        <div id="roulette-result"></div>
      </div>
    </section>

    <!-- 6. BLUEPRINT -->
    <section class="section">
      <span class="chapter-tag reveal">Kapitel 06</span>
      <h2 class="title reveal">Blueprint<br><em>150 Jahre</em></h2>
      <p class="section-desc reveal">Der Bauplan für unser gemeinsames Königreich.</p>
      <div id="blueprint-container" class="blueprint-grid"></div>
    </section>

    <!-- 7. SAFE HARBOR SOS -->
    <section class="section">
      <span class="chapter-tag reveal">Kapitel 07</span>
      <h2 class="title reveal">Safe Harbor<br><em>SOS</em></h2>
      <p class="section-desc reveal">Klicke auf einen Button, wenn es dir mal nicht so gut geht.</p>
      <div id="sos-buttons" class="sos-grid"></div>
    </section>

    <!-- 8. PROMISES -->
    <section class="section">
      <span class="chapter-tag reveal">Kapitel 08</span>
      <h2 class="title reveal">Schrein der<br><em>Versprechen</em></h2>
      <p class="section-desc reveal">Dinge, die für die Ewigkeit in Stein und Herz gemeißelt sind.</p>
      <div id="promises-container" class="promises-grid"></div>
    </section>

    <!-- 9. TIMELINE -->
    <section class="section">
      <span class="chapter-tag reveal">Kapitel 09</span>
      <h2 class="title reveal">Unsere<br><em>Zeitreise</em></h2>
      <p class="section-desc reveal">Von der ersten Nachricht 2024 bis zur Parkbank im Jahr 2074.</p>
      <div class="timeline" id="timeline-container"></div>
    </section>

    <!-- 10. QUIZ -->
    <section class="section" style="min-height: 80vh;">
      <span class="chapter-tag reveal">Kapitel 10</span>
      <h2 class="title reveal">Memory<br><em>Side Quest</em></h2>
      <p class="section-desc reveal">Beweise, wie gut du das Pepsiversum kennst!</p>
      <div class="quiz-box" id="quiz-container"></div>
    </section>

    <!-- OUTRO -->
    <section class="section" style="text-align: center; min-height: 50vh;">
      <h2 class="title reveal" style="font-size: 4rem;">Ich liebe dich, <em>Selly.</em></h2>
      <p class="reveal" style="font-size: 1.2rem; color: var(--gold); margin-top: 20px;">Dein Pepe.</p>
    </section>

  </main>

  <!-- SOS MODAL -->
  <div class="modal" id="sos-modal">
    <div class="modal-content">
      <h3 id="modal-title">Titel</h3>
      <p id="modal-advice">Advice</p>
      <blockquote id="modal-quote">Quote</blockquote>
      <div class="bonus" id="modal-bonus">Bonus</div>
      <br>
      <button id="modal-close" class="action-btn" style="padding: 10px 25px; font-size: 1rem;">Danke ❤️</button>
    </div>
  </div>

  <script>""" + app_js + """</script>
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

print("Generated and encrypted FULL 10-chapter pepsi.enc successfully!")
