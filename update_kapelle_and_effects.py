import re

# Read base64
with open(r'b64_kapelle.txt', 'r') as f:
    b64_img = f.read().strip()

with open('build_new_app.py', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. UPDATE KAPELLE HTML & REMOVE KAPITEL 11
new_kapelle_html = f'''    <!-- EIN KANAL ZU UNSEREN HERZEN -->
    <section class="section theme-kapelle" id="kapelle-section" style="position: relative; overflow: hidden;">
      <div class="candle-ambient-glow"></div>
      <span class="chapter-tag reveal" style="color: var(--gold); letter-spacing: 3px;">Seelenverbindung & Schutz</span>
      <h2 class="title reveal" style="color: #fff; text-shadow: 0 0 20px rgba(229,184,105,0.4);">Ein Kanal zu unseren Herzen</h2>
      <p class="section-desc reveal" style="max-width: 680px; margin: 0 auto 30px auto; color: #d0d7de;">
        Es gibt Momente im Leben, in denen zwei Seelen über jede Entfernung hinweg im selben Takt schlagen – geführt von etwas Größerem, das uns beschützt.
      </p>
      
      <!-- Interactive Candle Box -->
      <div id="kapelle-interact" class="reveal" style="margin: 30px auto; padding: 25px 20px; background: radial-gradient(circle at center, rgba(229,184,105,0.18) 0%, rgba(20,24,35,0.85) 100%); border: 1px solid rgba(229,184,105,0.6); border-radius: 25px; cursor: pointer; transition: all 0.4s ease; max-width: 480px; box-shadow: 0 10px 30px rgba(0,0,0,0.5), 0 0 25px rgba(229,184,105,0.25);">
        <div class="candle-flame-icon" style="font-size: 3.8rem; animation: pulseCandle 2s ease-in-out infinite;">🕯️</div>
        <h3 style="color: var(--gold); font-size: 1.5rem; margin-top: 10px; font-family: 'Playfair Display', serif;">Zünde eine Kerze für uns an</h3>
        <p style="font-size: 0.95rem; color: #a1b0c0; margin-top: 5px;">(Hier berühren für das Wunder der Waldkapelle)</p>
      </div>

      <!-- Revealed Content after clicking candle -->
      <div id="kapelle-content" style="display: none; opacity: 0;">
        <div class="kapelle-card" style="background: rgba(15, 18, 28, 0.88); border: 1px solid rgba(229,184,105,0.45); border-radius: 20px; padding: 30px 20px; max-width: 720px; margin: 0 auto; box-shadow: 0 15px 40px rgba(0,0,0,0.6), 0 0 35px rgba(229,184,105,0.2); backdrop-filter: blur(10px);">
          
          <div style="text-align: center; margin-bottom: 25px;">
            <span style="font-size: 2.2rem; filter: drop-shadow(0 0 10px gold);">✨ 🙏 ✨</span>
            <h3 style="color: var(--gold); font-family: 'Playfair Display', serif; font-size: 1.8rem; margin-top: 5px;">Das Versprechen der Waldkapelle</h3>
            <p style="color: var(--text-muted); font-size: 0.9rem;">24. August 2026</p>
          </div>

          <!-- Story Narrative Box: Denis am Vormittag -->
          <div style="background: rgba(29, 53, 87, 0.3); border-left: 3px solid #64b5f6; padding: 18px; border-radius: 0 12px 12px 0; margin-bottom: 20px; text-align: left;">
            <div style="font-weight: bold; color: #90caf9; margin-bottom: 6px; font-size: 1rem;">🕊️ Vormittags – Denis' Gedanken:</div>
            <p style="font-size: 0.95rem; line-height: 1.7; color: #e0e0e0;">
              Beim Einkaufen saß draußen eine Nonne und schaute Denis zwei Minuten lang intensiv an. In diesem Augenblick überkam ihn ein tiefer Herzenswunsch: Er wollte Selly bitten, in die Kirche zu gehen und eine Kerze anzuzünden – damit all ihre Sorgen, Ängste und Schmerzen verfliegen und sie von Gott & Maria beschützt wird. Er ahnte nicht, was wenig später am selben Tag geschehen würde...
            </p>
          </div>

          <!-- Story Narrative Box: Selly am Nachmittag -->
          <div style="background: rgba(74, 28, 64, 0.35); border-left: 3px solid var(--rose); padding: 18px; border-radius: 0 12px 12px 0; margin-bottom: 25px; text-align: left;">
            <div style="font-weight: bold; color: #ff8fa3; margin-bottom: 6px; font-size: 1rem;">🌿 Nachmittags – Sellys Eingebung:</div>
            <p style="font-size: 0.95rem; line-height: 1.7; color: #e0e0e0;">
              Ohne von Denis' Gedanken zu wissen, lag Selly nach dem Abschminken auf der Couch. Plötzlich hatte sie aus dem Nichts eine unwiderstehliche Eingebung, stand schnurstracks auf und fuhr zu einer abgelegenen Waldkapelle. Dort entzündete sie eine Kerze und schrieb diese unendlich berührenden Zeilen in das Gästebuch:
            </p>
          </div>

          <!-- Guestbook Photo -->
          <div style="position: relative; margin: 25px auto; text-align: center;">
            <img src="data:image/jpeg;base64,{b64_img}" style="width: 100%; max-width: 440px; border-radius: 15px; border: 2px solid rgba(229,184,105,0.6); box-shadow: 0 10px 30px rgba(0,0,0,0.7), 0 0 25px rgba(229,184,105,0.3); transition: transform 0.3s;" onmouseover="this.style.transform='scale(1.02)'" onmouseout="this.style.transform='scale(1)'">
          </div>

          <!-- Quote & Meaning -->
          <div style="background: rgba(229,184,105,0.08); border: 1px solid rgba(229,184,105,0.3); border-radius: 15px; padding: 20px; margin: 25px 0; text-align: left;">
            <blockquote style="font-family: 'Playfair Display', serif; font-style: italic; font-size: 1.15rem; color: var(--gold); line-height: 1.7; margin-bottom: 12px;">
              "Bitte hilf seinem Vater wieder gesund zu werden. Auf dass seiner Familie nie etwas zustoßen wird und er sein großes Glück finden wird. Bitte beschütze ihn für immer! 24.8.26 D.S.N"
            </blockquote>
            <p style="color: #cbd5e1; font-size: 0.9rem; border-top: 1px solid rgba(229,184,105,0.2); padding-top: 10px;">
              <strong style="color: var(--rose);">D.S.N</strong> = <em>Denis Saatloo & Selinda Nöckler</em> — "Wir teilen uns das ❤️"
            </p>
          </div>

          <!-- Eternal Promise Box -->
          <div style="text-align: left; background: rgba(0,0,0,0.4); padding: 20px; border-radius: 12px; border-left: 3px solid var(--mint);">
            <p style="font-style: italic; color: #f1f5f9; font-size: 1.05rem; line-height: 1.8; margin-bottom: 10px;">
              "Möge Maria dich auf all deinen Wegen begleiten und immer beschützen... Sie wird dich immer begleiten und wir werden durch sie einen Kanal zu unseren Herzen haben, wann immer einer von uns ruft. Wenn einer von uns im Stress steht, ist der andere der sichere Fels in der Brandung."
            </p>
            <p style="color: var(--mint); font-weight: bold; font-size: 0.95rem;">- Denis' ewiges Schutzversprechen</p>
          </div>

        </div>
      </div>
    </section>'''

# Replace the existing Kapelle section
kapelle_regex = re.compile(r'<!-- KAPITEL 11 -->.*?</section>', re.DOTALL)
if kapelle_regex.search(code):
    code = kapelle_regex.sub(new_kapelle_html, code)
    print("Replaced Kapelle HTML successfully!")
else:
    # Also check if it starts with <!-- EIN KANAL ZU UNSEREN HERZEN -->
    kapelle_regex2 = re.compile(r'<!-- EIN KANAL ZU UNSEREN HERZEN -->.*?</section>', re.DOTALL)
    if kapelle_regex2.search(code):
        code = kapelle_regex2.sub(new_kapelle_html, code)
        print("Replaced Kapelle HTML via regex2!")

# 2. UPDATE SCHNECKEN-ZÄHLER CARD IN SPIELZIMMER
old_schnecke_card = """        <!-- 1. Schnecke -->
        <div class="mg-card" id="card-schnecke">
          <div class="mg-title">Der Schnecken-Zähler</div>
          <div id="schnecke-emoji" style="font-size: 4rem; cursor: pointer; transition: transform 0.1s;">🐌</div>
          <div id="schnecke-count" style="font-size: 2rem; font-weight: bold; color: var(--brand); margin-top: 10px;">0</div>
          <p style="font-size: 0.8rem; margin-top:5px;">(Tippen!)</p>
        </div>"""

new_schnecke_card = """        <!-- 1. Schnecke -->
        <div class="mg-card" id="card-schnecke">
          <div class="mg-title">🐌 Der Schnecken-Zähler</div>
          <p style="font-size: 0.85rem; color: #cbd5e1; line-height: 1.4; margin-bottom: 12px; max-width: 260px;">
            Euer absoluter Rekord-Kosename! Über <strong style="color: var(--gold);">1.198 Mal</strong> hast du sie im Chat liebevoll <em>"Schnecke"</em> genannt.
          </p>
          <div id="schnecke-emoji" style="font-size: 4.2rem; cursor: pointer; transition: transform 0.15s cubic-bezier(0.175, 0.885, 0.32, 1.275); display: inline-block;">🐌</div>
          <div id="schnecke-count" style="font-size: 2.2rem; font-weight: 800; font-family: 'DM Mono', monospace; color: var(--rose); text-shadow: 0 0 15px rgba(255,77,109,0.5); margin: 8px 0;">0</div>
          <p style="font-size: 0.8rem; color: var(--gold); font-weight: bold;">(Tippe auf die Schnecke!)</p>
        </div>"""

code = code.replace(old_schnecke_card, new_schnecke_card)
print("Updated Schnecken-Zähler card HTML!")

# 3. ADD VIBRANT CSS, AMBIENT PARTICLES, GLOWS & ANIMATIONS
extra_css = """
/* AMBIENT & LIVELY VISUAL ENHANCEMENTS */
.theme-kapelle {
  background: radial-gradient(circle at 50% 30%, rgba(229,184,105,0.12) 0%, rgba(9,10,15,0.95) 75%);
  border-top: 1px solid rgba(229,184,105,0.3);
}

.candle-ambient-glow {
  position: absolute;
  top: 10%;
  left: 50%;
  transform: translateX(-50%);
  width: 300px;
  height: 300px;
  background: radial-gradient(circle, rgba(229,184,105,0.15) 0%, transparent 70%);
  pointer-events: none;
  animation: pulseGlow 4s ease-in-out infinite alternate;
}

@keyframes pulseCandle {
  0% { transform: scale(1); filter: drop-shadow(0 0 8px rgba(229,184,105,0.5)); }
  50% { transform: scale(1.1); filter: drop-shadow(0 0 20px rgba(255,215,0,0.8)); }
  100% { transform: scale(1); filter: drop-shadow(0 0 8px rgba(229,184,105,0.5)); }
}

@keyframes pulseGlow {
  0% { opacity: 0.4; transform: translateX(-50%) scale(0.9); }
  100% { opacity: 0.8; transform: translateX(-50%) scale(1.15); }
}

/* Card shimmer & lively gradients */
.mg-card {
  background: linear-gradient(135deg, rgba(255,255,255,0.05) 0%, rgba(255,255,255,0.01) 100%);
  border: 1px solid rgba(255,215,0,0.3);
  border-radius: 18px;
  padding: 24px 20px;
  text-align: center;
  overflow: hidden;
  position: relative;
  min-height: 270px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  box-shadow: 0 8px 25px rgba(0,0,0,0.3);
  transition: transform 0.3s ease, border-color 0.3s ease, box-shadow 0.3s ease;
}

.mg-card:hover {
  transform: translateY(-5px);
  border-color: var(--gold);
  box-shadow: 0 12px 35px rgba(229,184,105,0.25);
}

.mg-title {
  font-family: var(--font-title);
  color: var(--gold);
  margin-bottom: 10px;
  font-size: 1.35rem;
  text-shadow: 0 0 10px rgba(229,184,105,0.3);
}

/* Global Ambient floating particles */
.ambient-particle {
  position: fixed;
  pointer-events: none;
  z-index: 10;
  user-select: none;
  animation: floatAmbient linear forwards;
}

@keyframes floatAmbient {
  0% { transform: translateY(105vh) scale(0.5) rotate(0deg); opacity: 0; }
  15% { opacity: 0.8; }
  85% { opacity: 0.8; }
  100% { transform: translateY(-10vh) scale(1.2) rotate(360deg); opacity: 0; }
}

/* Click burst particles */
.burst-particle {
  position: fixed;
  pointer-events: none;
  z-index: 9999;
  user-select: none;
  animation: burstFade 1.2s cubic-bezier(0.25, 1, 0.5, 1) forwards;
}

@keyframes burstFade {
  0% { transform: translate(0, 0) scale(0.6); opacity: 1; }
  100% { transform: translate(var(--dx), var(--dy)) scale(1.4); opacity: 0; }
}
"""

if 'AMBIENT & LIVELY VISUAL ENHANCEMENTS' not in code:
    code = code.replace('</style>', extra_css + '\n</style>')
    print("Added vibrant CSS enhancements!")

# 4. ADD GLOBAL AMBIENT PARTICLES AND CLICK BURST JS
extra_js = """
      // ==========================================
      // GLOBAL LIVELY PARTICLES & CLICK BURST
      // ==========================================
      
      // Continuous ambient floating hearts and stars
      const ambientIcons = ['✨', '💖', '⭐', '🌸', '💫', '❤️', '🕊️'];
      function spawnAmbientParticle() {
        const p = document.createElement('div');
        p.className = 'ambient-particle';
        p.innerText = ambientIcons[Math.floor(Math.random() * ambientIcons.length)];
        p.style.left = (Math.random() * 95) + 'vw';
        p.style.fontSize = (Math.random() * 16 + 12) + 'px';
        const duration = Math.random() * 8 + 7; // 7-15s
        p.style.animationDuration = duration + 's';
        document.body.appendChild(p);
        setTimeout(() => p.remove(), duration * 1000);
      }
      setInterval(spawnAmbientParticle, 1200);

      // Interactive Click Sparkles everywhere
      document.addEventListener('click', (e) => {
        // Don't burst on heavy drag
        const icons = ['✨', '💖', '❤️', '💫', '🌸'];
        for(let i = 0; i < 4; i++) {
          const p = document.createElement('div');
          p.className = 'burst-particle';
          p.innerText = icons[Math.floor(Math.random() * icons.length)];
          p.style.left = e.clientX + 'px';
          p.style.top = e.clientY + 'px';
          p.style.fontSize = (Math.random() * 14 + 14) + 'px';
          
          const angle = Math.random() * Math.PI * 2;
          const distance = Math.random() * 60 + 30;
          const dx = Math.cos(angle) * distance + 'px';
          const dy = (Math.sin(angle) * distance - 20) + 'px';
          p.style.setProperty('--dx', dx);
          p.style.setProperty('--dy', dy);
          
          document.body.appendChild(p);
          setTimeout(() => p.remove(), 1200);
        }
      });
"""

if 'GLOBAL LIVELY PARTICLES & CLICK BURST' not in code:
    code = code.replace('renderApp();', extra_js + '\n      renderApp();')
    print("Added lively particles & click burst JS!")

with open('build_new_app.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("Saved updated build_new_app.py successfully!")
