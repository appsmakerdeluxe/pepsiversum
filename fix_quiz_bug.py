import re

with open('build_new_app.py', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Remove 'reveal' class from Quiz dynamically rendered elements
if '<div class="quiz-result reveal">' in code:
    code = code.replace('<div class="quiz-result reveal">', '<div class="quiz-result" style="animation: fadeIn 0.5s forwards;">')

if '<div class="quiz-card reveal">' in code:
    code = code.replace('<div class="quiz-card reveal">', '<div class="quiz-card" style="animation: fadeIn 0.5s forwards;">')

# 2. Add playTada() and createFireworks()
new_funcs = """function playTada() {
  safePlay(() => {
    [523.25, 659.25, 783.99].forEach(freq => {
      const osc = audioCtx.createOscillator();
      const gain = audioCtx.createGain();
      osc.connect(gain); gain.connect(audioCtx.destination);
      osc.type = 'triangle'; osc.frequency.value = freq;
      gain.gain.setValueAtTime(0.3, audioCtx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 1.5);
      osc.start(); osc.stop(audioCtx.currentTime + 1.5);
    });
  });
}

function createFireworks() {
  const c = document.createElement('div');
  c.className = 'rain-container';
  document.body.appendChild(c);
  const colors = ['#ff4d6d', '#e5b869', '#0ecbb5', '#ffffff'];
  for(let j=0; j<3; j++) {
    setTimeout(() => {
      const cx = Math.random() * 60 + 20;
      const cy = Math.random() * 60 + 20;
      for(let i=0; i<40; i++) {
        const p = document.createElement('div');
        p.style.position = 'absolute';
        p.style.width = '6px'; p.style.height = '6px';
        p.style.borderRadius = '50%';
        p.style.background = colors[Math.floor(Math.random() * colors.length)];
        p.style.left = cx + 'vw';
        p.style.top = cy + 'vh';
        const angle = Math.random() * Math.PI * 2;
        const dist = Math.random() * 150 + 50;
        p.animate([
          { transform: `translate(0,0) scale(1.5)`, opacity: 1 },
          { transform: `translate(${Math.cos(angle)*dist}px, ${Math.sin(angle)*dist}px) scale(0)`, opacity: 0 }
        ], { duration: 800 + Math.random()*400, easing: 'cubic-bezier(0,0,0.2,1)', fill: 'forwards' });
        c.appendChild(p);
      }
    }, j*300);
  }
  setTimeout(() => c.remove(), 3000);
}

function createRain() {"""

if 'function createRain() {' in code:
    code = code.replace('function createRain() {', new_funcs)

# 3. Trigger Fireworks on Quiz Success
quiz_logic_old = """        if(isCorrect) {
          e.target.classList.add('correct');
          score++;
          playPop();
        } else {"""
quiz_logic_new = """        if(isCorrect) {
          e.target.classList.add('correct');
          score++;
          playTada();
          createFireworks();
        } else {"""
if quiz_logic_old in code:
    code = code.replace(quiz_logic_old, quiz_logic_new)

# Make sure CSS has fadeIn
css_fadein = """@keyframes fall { to { transform: translateY(110vh); opacity: 0; } }"""
css_fadein_new = """@keyframes fall { to { transform: translateY(110vh); opacity: 0; } }
@keyframes fadeIn { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }"""
if css_fadein in code:
    code = code.replace(css_fadein, css_fadein_new)


with open('build_new_app.py', 'w', encoding='utf-8') as f:
    f.write(code)
