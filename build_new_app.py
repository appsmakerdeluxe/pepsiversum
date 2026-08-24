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
const AudioContext = window.AudioContext || window.webkitAudioContext;
let audioCtx;
try { audioCtx = new AudioContext(); } catch(e) { console.error('AudioContext error', e); }

function safePlay(playFn) {
  try {
    if(!audioCtx) return;
    if(audioCtx.state === 'suspended') audioCtx.resume().then(() => playFn()).catch(e=>console.error(e));
    else playFn();
  } catch(e) { console.error('Play error', e); }
}

function playPop() {
  safePlay(() => {
    const osc = audioCtx.createOscillator();
    const gain = audioCtx.createGain();
    osc.connect(gain); gain.connect(audioCtx.destination);
    osc.type = 'sine'; osc.frequency.setValueAtTime(600, audioCtx.currentTime);
    osc.frequency.exponentialRampToValueAtTime(800, audioCtx.currentTime + 0.1);
    gain.gain.setValueAtTime(0.5, audioCtx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.1);
    osc.start(); osc.stop(audioCtx.currentTime + 0.1);
  });
}

function playPurr() {
  safePlay(() => {
    const bufferSize = audioCtx.sampleRate * 2;
    const buffer = audioCtx.createBuffer(1, bufferSize, audioCtx.sampleRate);
    const data = buffer.getChannelData(0);
    for(let i=0; i<bufferSize; i++) { data[i] = (Math.random() * 2 - 1) * 0.2; }
    const noise = audioCtx.createBufferSource();
    noise.buffer = buffer;
    const filter = audioCtx.createBiquadFilter();
    filter.type = 'lowpass'; filter.frequency.value = 150;
    const gain = audioCtx.createGain();
    noise.connect(filter); filter.connect(gain); gain.connect(audioCtx.destination);
    gain.gain.setValueAtTime(0, audioCtx.currentTime);
    gain.gain.linearRampToValueAtTime(0.5, audioCtx.currentTime + 0.5);
    gain.gain.linearRampToValueAtTime(0, audioCtx.currentTime + 2);
    noise.start();
  });
}

function playMeow() {
  safePlay(() => {
    const osc = audioCtx.createOscillator();
    const gain = audioCtx.createGain();
    osc.connect(gain); gain.connect(audioCtx.destination);
    osc.type = 'triangle'; osc.frequency.setValueAtTime(400, audioCtx.currentTime);
    osc.frequency.exponentialRampToValueAtTime(600, audioCtx.currentTime + 0.3);
    gain.gain.setValueAtTime(0, audioCtx.currentTime);
    gain.gain.linearRampToValueAtTime(0.3, audioCtx.currentTime + 0.1);
    gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.5);
    osc.start(); osc.stop(audioCtx.currentTime + 0.5);
  });
}

function playHeartbeat() {
  safePlay(() => {
    const osc = audioCtx.createOscillator();
    const gain = audioCtx.createGain();
    osc.connect(gain); gain.connect(audioCtx.destination);
    osc.type = 'sine'; osc.frequency.setValueAtTime(50, audioCtx.currentTime);
    gain.gain.setValueAtTime(0, audioCtx.currentTime);
    gain.gain.linearRampToValueAtTime(1, audioCtx.currentTime + 0.1);
    gain.gain.linearRampToValueAtTime(0, audioCtx.currentTime + 0.3);
    gain.gain.linearRampToValueAtTime(1, audioCtx.currentTime + 0.5);
    gain.gain.linearRampToValueAtTime(0, audioCtx.currentTime + 0.8);
    osc.start(); osc.stop(audioCtx.currentTime + 1);
  });
}

function playChime() {
  safePlay(() => {
    const osc = audioCtx.createOscillator();
    const gain = audioCtx.createGain();
    osc.connect(gain); gain.connect(audioCtx.destination);
    osc.type = 'sine'; osc.frequency.setValueAtTime(800, audioCtx.currentTime);
    gain.gain.setValueAtTime(0.5, audioCtx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 2);
    osc.start(); osc.stop(audioCtx.currentTime + 2);
  });
}

function createRain() {
  const rainContainer = document.createElement('div');
  rainContainer.className = 'rain-container';
  document.body.appendChild(rainContainer);
  for(let i=0; i<50; i++) {
    const drop = document.createElement('div');
    drop.className = 'raindrop';
    drop.style.left = Math.random() * 100 + 'vw';
    drop.style.animationDuration = (Math.random() * 0.5 + 0.5) + 's';
    drop.style.animationDelay = (Math.random() * 1) + 's';
    rainContainer.appendChild(drop);
  }
  setTimeout(() => rainContainer.remove(), 5000);
}

function createConfetti() {
  const c = document.createElement('div');
  c.className = 'rain-container';
  document.body.appendChild(c);
  const colors = ['#e5b869', '#ff4d6d', '#0ecbb5', '#ffffff'];
  for(let i=0; i<60; i++) {
    const p = document.createElement('div');
    p.className = 'confetti';
    p.style.background = colors[Math.floor(Math.random() * colors.length)];
    p.style.left = Math.random() * 100 + 'vw';
    p.style.top = '-10px';
    p.style.animation = `fall ${Math.random() * 2 + 2}s linear forwards`;
    p.style.animationDelay = (Math.random() * 2) + 's';
    c.appendChild(p);
  }
  setTimeout(() => c.remove(), 5000);
}

function createFloatingHearts() {
  const hc = document.createElement('div');
  hc.className = 'rain-container';
  document.body.appendChild(hc);
  for(let i=0; i<20; i++) {
    const h = document.createElement('div');
    h.innerHTML = '❤️';
    h.style.position = 'absolute';
    h.style.left = Math.random() * 100 + 'vw';
    h.style.bottom = '-20px';
    h.style.fontSize = (Math.random() * 2 + 1) + 'rem';
    h.style.animation = `floatHeart ${Math.random() * 2 + 3}s ease-in forwards`;
    h.style.animationDelay = (Math.random() * 0.5) + 's';
    hc.appendChild(h);
  }
  setTimeout(() => hc.remove(), 5000);
}

function renderApp() {
  // 1. Late Night
  const lateNightDialogues = appData.lateNight.romantic.slice(0, 15).map((dialogue, dIndex) => {
    const bubbles = dialogue.map((m, i) => `
      <div class="chat-bubble ${m.sender === 'Denis' ? 'right' : 'left'}">
        <div class="chat-meta">${m.date} • ${m.time}</div>
        <div class="chat-text">${m.text}</div>
      </div>
    `).join('');
    return `<div class="dialogue-block reveal" style="margin-bottom: 50px; border-left: 2px solid var(--gold); padding-left: 20px;">
              <span class="dialogue-title" style="color: var(--gold); font-family: 'DM Mono'; font-size: 0.8rem; letter-spacing: 1px; text-transform: uppercase;">Erinnerung ${dIndex + 1}</span>
              <div class="chat-group" style="display: flex; flex-direction: column; gap: 10px; margin-top: 15px;">
                ${bubbles}
              </div>
            </div>`;
  }).join('');
  $('#latenight-container').innerHTML = lateNightDialogues;

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
  $all('.cat-sound').forEach(btn => {
    btn.addEventListener('click', (e) => {
      if(e.target.dataset.type === 'meow') playMeow();
      else playPurr();
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

  // 7. Safe Harbor SOS (Highly Interactive)
  const sosContainer = $('#sos-buttons');
  const modal = $('#sos-modal');
  appData.safeHarbor.forEach((s, index) => {
    const btn = document.createElement('button');
    btn.className = 'sos-btn reveal';
    btn.innerHTML = `<span class="icon">${s.icon}</span> <span class="title">${s.title}</span>`;
    btn.addEventListener('click', () => {
      // Dynamic effects based on which button was clicked
      const colors = [
        'linear-gradient(135deg, rgba(15,23,42,0.95), rgba(30,58,138,0.95))', // Blue/Rain
        'linear-gradient(135deg, rgba(23,15,42,0.95), rgba(76,29,149,0.95))', // Purple/Breathe
        'linear-gradient(135deg, rgba(42,15,23,0.95), rgba(190,18,60,0.95))', // Rose/Heart
        'linear-gradient(135deg, rgba(42,26,15,0.95), rgba(154,52,18,0.95))', // Orange/Anger
        'linear-gradient(135deg, rgba(229,184,105,0.95), rgba(15,23,42,0.95))'  // Gold/Final
      ];
      
      modal.style.background = colors[index % colors.length];
      $('#modal-title').textContent = s.title;
      $('#modal-advice').textContent = s.advice;
      $('#modal-quote').textContent = s.quote;
      $('#modal-action').textContent = s.actionText;
      $('#modal-bonus').textContent = "🎁 " + s.bonus;
      
      if (index === 0) { playChime(); createRain(); }
      else if (index === 1) { playChime(); }
      else if (index === 2) { playHeartbeat(); createFloatingHearts(); }
      else if (index === 3) { playPop(); }
      else if (index === 4) { playChime(); createConfetti(); }

      
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
  const questions = appData.quiz; // 20 questions
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
    // Shuffle options
    const options = q.options.map((text, idx) => ({ text, isCorrect: idx === q.answer }));
    options.sort(() => Math.random() - 0.5);
    
    $('#quiz-container').innerHTML = `
      <div class="quiz-card reveal">
        <span class="step">Frage ${currentQ + 1} von ${questions.length}</span>
        <h3 class="question">${q.q}</h3>
        <div class="options">
          ${options.map((opt, i) => `<button class="quiz-opt" data-correct="${opt.isCorrect}">${opt.text}</button>`).join('')}
        </div>
      </div>
    `;
    
    $all('.quiz-opt').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const isCorrect = e.target.dataset.correct === 'true';
        if(isCorrect) {
          e.target.classList.add('correct');
          score++;
          playPop();
        } else {
          e.target.classList.add('wrong');
          $all('.quiz-opt').find(b => b.dataset.correct === 'true').classList.add('correct');
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
  let treeRevealed = false;
  const observer = new IntersectionObserver(entries => entries.forEach(entry => {
    if (entry.isIntersecting) { 
      entry.target.classList.add('is-visible'); 
      
      // Floating emojis for timeline
      if (entry.target.classList.contains('timeline-item')) {
        const text = entry.target.innerText.toLowerCase();
        let emoji = '';
        if(text.includes('eis')) emoji = '🍦';
        else if(text.includes('katze') || text.includes('suri') || text.includes('pamuk')) emoji = '🐾';
        else if(text.includes('liebe') || text.includes('herz')) emoji = '❤️';
        else if(text.includes('hochzeit') || text.includes('ring')) emoji = '💍';
        else if(text.includes('zukunft')) emoji = '✨';
        
        if (emoji) {
          const l = document.createElement('div');
          l.innerHTML = emoji;
          l.className = 'falling-leaf'; // reuse animation
          l.style.left = (Math.random() * 80 + 10) + '%';
          l.style.animationDuration = '4s';
          entry.target.appendChild(l);
          setTimeout(() => l.remove(), 4000);
        }
      }

      if (entry.target.id === 'tree-trigger' && !treeRevealed) {
        treeRevealed = true;
        const c = $('.tree-section');
        for(let i=0; i<35; i++) {
          setTimeout(() => {
            const l = document.createElement('div');
            l.innerHTML = ['🍂', '🍁', '🍃'][Math.floor(Math.random()*3)];
            l.className = 'falling-leaf';
            l.style.left = (Math.random() * 100) + '%';
            l.style.animationDuration = (Math.random() * 3 + 4) + 's';
            c.appendChild(l);
            setTimeout(() => l.remove(), 7000);
          }, i * 200);
        }
      }
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

/* Dynamic SOS Modal Animations */
.rain-container { position: fixed; inset: 0; pointer-events: none; z-index: 99; overflow: hidden; }
.raindrop { position: absolute; top: -50px; width: 2px; height: 30px; background: linear-gradient(to bottom, transparent, rgba(255,255,255,0.6)); animation: fall linear forwards; }
@keyframes fall { to { transform: translateY(110vh); opacity: 0; } }
@keyframes floatHeart { 0% { transform: translateY(0) scale(1); opacity: 1; } 100% { transform: translateY(-100vh) scale(2); opacity: 0; } }

/* 8.5. Tree */
.carve-path { stroke-dasharray: 200; stroke-dashoffset: 200; transition: stroke-dashoffset 4s cubic-bezier(0.4, 0, 0.2, 1); }
.tree-container.is-visible .carve-path { stroke-dashoffset: 0; }
.carve-text { opacity: 0; transition: opacity 2s ease-in; transition-delay: 2s; }
.tree-container.is-visible .carve-text { opacity: 1; }
.falling-leaf { position: absolute; font-size: 1.5rem; animation: leafFall linear forwards; z-index: 10; pointer-events: none; }
@keyframes leafFall { 0% { transform: translate(0, -50px) rotate(0deg); opacity: 0; } 10% { opacity: 1; } 100% { transform: translate(150px, 110vh) rotate(720deg); opacity: 0; } }

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

/* Thematic Backgrounds */
.theme-latenight { background: radial-gradient(circle at top right, rgba(29,53,87,0.3), transparent 70%); }
.theme-spotify { background: linear-gradient(180deg, transparent, rgba(157,78,221,0.1)); }
.theme-kintsugi { background-image: radial-gradient(rgba(229,184,105,0.2) 1px, transparent 1px); background-size: 30px 30px; }
.theme-cats { background: radial-gradient(circle at bottom left, rgba(255,77,109,0.15), transparent 50%); }
.theme-icecream { background-image: repeating-linear-gradient(45deg, transparent, transparent 10px, rgba(14,203,181,0.05) 10px, rgba(14,203,181,0.05) 20px); }
.theme-blueprint { background-image: linear-gradient(rgba(255,255,255,0.03) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.03) 1px, transparent 1px); background-size: 40px 40px; }
.theme-sos { background: radial-gradient(circle at center, rgba(14,203,181,0.1) 0%, transparent 70%); }
.theme-promises { background: radial-gradient(ellipse at top, rgba(229,184,105,0.15), transparent 60%); }
.theme-tree { background: linear-gradient(to bottom, transparent, rgba(62,39,35,0.2)); }
.theme-timeline { background-image: linear-gradient(0deg, transparent 24%, rgba(255,255,255,0.03) 25%, rgba(255,255,255,0.03) 26%, transparent 27%, transparent 74%, rgba(255,255,255,0.03) 75%, rgba(255,255,255,0.03) 76%, transparent 77%, transparent), linear-gradient(90deg, transparent 24%, rgba(255,255,255,0.03) 25%, rgba(255,255,255,0.03) 26%, transparent 27%, transparent 74%, rgba(255,255,255,0.03) 75%, rgba(255,255,255,0.03) 76%, transparent 77%, transparent); background-size: 50px 50px; }
.theme-quiz { background: linear-gradient(180deg, transparent, rgba(255,77,109,0.15)); border-top: 1px solid rgba(255,77,109,0.3); }

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
    <section class="section theme-latenight">
      <span class="chapter-tag reveal">Kapitel 01</span>
      <h2 class="title reveal">Late Night<br><em>Whispers</em></h2>
      <p class="section-desc reveal">Zwischen 2 und 5 Uhr morgens. Wenn die Welt schlief, wurden wir wach, ehrlich und verrückt.</p>
      <div id="latenight-container" class="chat-container"></div>
    </section>

    <!-- 2. SPOTIFY -->
    <section class="section theme-spotify">
      <span class="chapter-tag reveal">Kapitel 02</span>
      <h2 class="title reveal">Midnight<br><em>FM</em></h2>
      <p class="section-desc reveal">Der Soundtrack unserer Chat-Historie. Jedes Lied mit seiner eigenen Erinnerung.</p>
      <div id="spotify-container" class="spotify-grid"></div>
    </section>

    <!-- 3. KINTSUGI -->
    <section class="section theme-kintsugi">
      <span class="chapter-tag reveal">Kapitel 03</span>
      <h2 class="title reveal">Aus Scherben<br><em>wird Gold</em></h2>
      <p class="section-desc reveal">In Japan repariert man Zerbrochenes mit Gold (Kintsugi). Wahre Liebe zeigt sich darin, wie man Fehler vergibt und stärker zusammenwächst.</p>
      <div id="kintsugi-container" class="kintsugi-grid"></div>
    </section>

    <!-- 4. CATS -->
    <section class="section theme-cats">
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
    <section class="section theme-icecream">
      <span class="chapter-tag reveal">Kapitel 05</span>
      <h2 class="title reveal">Eislabor &<br><em>Date Roulette</em></h2>
      <p class="section-desc reveal">Über 2.400 mal Eis im Chat. Weißt du nicht, was wir als nächstes machen sollen? Dreh das Rad!</p>
      <div class="roulette-box reveal">
        <button id="btn-roulette" class="action-btn">Date-Roulette starten 🎲</button>
        <div id="roulette-result"></div>
      </div>
    </section>

    <!-- 6. BLUEPRINT -->
    <section class="section theme-blueprint">
      <span class="chapter-tag reveal">Kapitel 06</span>
      <h2 class="title reveal">Blueprint<br><em>150 Jahre</em></h2>
      <p class="section-desc reveal">Der Bauplan für unser gemeinsames Königreich.</p>
      <div id="blueprint-container" class="blueprint-grid"></div>
    </section>

    <!-- 7. SAFE HARBOR SOS -->
    <section class="section theme-sos">
      <span class="chapter-tag reveal">Kapitel 07</span>
      <h2 class="title reveal">Safe Harbor<br><em>SOS</em></h2>
      <p class="section-desc reveal">Klicke auf einen Button, wenn es dir mal nicht so gut geht.</p>
      <div id="sos-buttons" class="sos-grid"></div>
    </section>

    <!-- 8. PROMISES -->
    <section class="section theme-promises">
      <span class="chapter-tag reveal">Kapitel 08</span>
      <h2 class="title reveal">Schrein der<br><em>Versprechen</em></h2>
      <p class="section-desc reveal">Dinge, die für die Ewigkeit in Stein und Herz gemeißelt sind.</p>
      <div id="promises-container" class="promises-grid"></div>
    </section>

    <!-- 8.5. CARVED TREE -->
    <section class="section tree-section theme-tree" style="text-align: center; overflow: hidden; position: relative;">
      <span class="chapter-tag reveal">Kapitel 08.5</span>
      <h2 class="title reveal">In die Ewigkeit<br><em>geritzt</em></h2>
      <p class="section-desc reveal" style="margin: 0 auto 40px;">Ein Schwur, der niemals verblasst.</p>
      
      <div class="tree-container reveal" id="tree-trigger" style="position: relative; display: inline-block;">
        <p class="carve-story" style="font-style:italic; font-size:1.1rem; color:var(--gold); margin-bottom: 20px;">
          "Ich habe deinen Namen in mein Herz geritzt und da bleibt er bis zum Tod."<br>
          <span style="font-size:0.9rem; color:var(--text-muted);">(Denis)</span>
        </p>
        <svg width="250" height="400" viewBox="0 0 200 400" class="tree-svg">
          <!-- Tree trunk -->
          <path d="M50,400 Q80,200 60,0 L140,0 Q120,200 150,400 Z" fill="#3E2723" />
          <path d="M70,400 Q90,200 80,0" stroke="#1b100e" stroke-width="3" fill="none" />
          <path d="M130,400 Q110,200 120,0" stroke="#1b100e" stroke-width="2" fill="none" />
          <!-- Carved heart -->
          <g transform="translate(35, 120) scale(1.3)">
             <path d="M25,25 A12,12 0,0,1 50,25 A12,12 0,0,1 75,25 Q75,45 50,70 Q25,45 25,25 Z" fill="none" stroke="#ffe0b2" stroke-width="2" class="carve-path"/>
             <text x="50" y="47" font-family="'Playfair Display'" font-size="16" fill="#ffe0b2" text-anchor="middle" font-style="italic" class="carve-text">S N</text>
          </g>
        </svg>
      </div>
    </section>

    <!-- 9. TIMELINE -->
    <section class="section theme-timeline">
      <span class="chapter-tag reveal">Kapitel 09</span>
      <h2 class="title reveal">Unsere<br><em>Zeitreise</em></h2>
      <p class="section-desc reveal">Von der ersten Nachricht 2024 bis zur Parkbank im Jahr 2074.</p>
      <div class="timeline" id="timeline-container"></div>
    </section>

    <!-- 10. QUIZ -->
    <section class="section theme-quiz" style="min-height: 80vh;">
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
      <p id="modal-action" style="font-weight:bold; color:var(--mint); margin-bottom: 20px;"></p>
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
