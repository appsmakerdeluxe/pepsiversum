import re

with open('build_new_app.py', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Update SOS click handler to handle index 4
sos_old = """      if (index === 0) { playChime(); createRain(); }
      else if (index === 1) { playChime(); }
      else if (index === 2) { playHeartbeat(); createFloatingHearts(); }
      else { playPop(); }"""

sos_new = """      if (index === 0) { playChime(); createRain(); }
      else if (index === 1) { playChime(); }
      else if (index === 2) { playHeartbeat(); createFloatingHearts(); }
      else if (index === 3) { playPop(); }
      else if (index === 4) { playChime(); createConfetti(); }
"""

if sos_old in code:
    code = code.replace(sos_old, sos_new)

# 2. Add createConfetti
confetti_func = """function createFloatingHearts() {"""
confetti_inject = """function createConfetti() {
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

function createFloatingHearts() {"""
if confetti_func in code:
    code = code.replace(confetti_func, confetti_inject)

# 3. Fix Tree SVG centering
tree_svg_old = """          <g transform="translate(65, 120) scale(1.3)">"""
tree_svg_new = """          <g transform="translate(45, 120) scale(1.3)">"""
if tree_svg_old in code:
    code = code.replace(tree_svg_old, tree_svg_new)

# 4. Add Tree description text
tree_desc_old = """      <div class="tree-container reveal" id="tree-trigger" style="position: relative; display: inline-block;">"""
tree_desc_new = """      <div class="tree-container reveal" id="tree-trigger" style="position: relative; display: inline-block;">
        <p class="carve-story" style="font-style:italic; font-size:1.1rem; color:var(--gold); margin-bottom: 20px;">
          "Ich habe deinen Namen in mein Herz geritzt und da bleibt er bis zum Tod."<br>
          <span style="font-size:0.9rem; color:var(--text-muted);">(Denis)</span>
        </p>"""
if tree_desc_old in code:
    code = code.replace(tree_desc_old, tree_desc_new)

with open('build_new_app.py', 'w', encoding='utf-8') as f:
    f.write(code)
