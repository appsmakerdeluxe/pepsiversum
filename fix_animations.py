import re

with open('build_new_app.py', 'r', encoding='utf-8') as f:
    code = f.read()

# Make promises interactive
promises_css_old = """.promise-card:hover { transform: translateY(-10px); box-shadow: 0 10px 30px rgba(229,184,105,0.2); }"""
promises_css_new = """.promise-card:hover { transform: translateY(-10px) scale(1.05); box-shadow: 0 10px 40px rgba(229,184,105,0.4); border-color: rgba(229,184,105,0.8); }
.timeline-item:hover { transform: scale(1.02); background: rgba(255,255,255,0.05); }"""
if promises_css_old in code:
    code = code.replace(promises_css_old, promises_css_new)

# Add Timeline Emoji spawner logic in initObserver()
obs_old = """      if (entry.target.id === 'tree-trigger' && !treeRevealed) {"""
obs_new = """      
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

      if (entry.target.id === 'tree-trigger' && !treeRevealed) {"""
if obs_old in code:
    code = code.replace(obs_old, obs_new)
    
# Add random 5th background color in SOS
sos_color_old = """        'linear-gradient(135deg, rgba(42,26,15,0.95), rgba(154,52,18,0.95))'  // Orange/Anger
      ];"""
sos_color_new = """        'linear-gradient(135deg, rgba(42,26,15,0.95), rgba(154,52,18,0.95))', // Orange/Anger
        'linear-gradient(135deg, rgba(229,184,105,0.95), rgba(15,23,42,0.95))'  // Gold/Final
      ];"""
if sos_color_old in code:
    code = code.replace(sos_color_old, sos_color_new)


with open('build_new_app.py', 'w', encoding='utf-8') as f:
    f.write(code)
