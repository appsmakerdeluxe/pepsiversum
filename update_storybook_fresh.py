import re

with open('build_new_app.py', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. CLEAN HTML (NO YELLOW CROSS, NO CORNER CROSSES)
new_storybook_html = """    <!-- DAS BUCH UNSERES LEBENS (DIRECT OPEN) -->
    <section class="section theme-storybook" id="storybook-section" style="position: relative; overflow: hidden; text-align: center;">
      <div class="book-ambient-glow"></div>
      <span class="chapter-tag reveal" style="color: var(--gold); letter-spacing: 4px;">Das ewige Archiv</span>
      <h2 class="title reveal" style="color: #fff; text-shadow: 0 0 25px rgba(229,184,105,0.4);">Das Buch unseres Lebens</h2>
      <p class="section-desc reveal" style="max-width: 650px; margin: 0 auto 20px auto; color: #cbd5e1;">
        Blättere durch unsere gemeinsame Geschichte – mit handschriftlichen Notizen, Geheimfächern und ewigen Worten.
      </p>

      <!-- SWIPE & INTERACTION HINT -->
      <div class="reveal" style="margin-bottom: 25px;">
        <span class="book-swipe-badge">✨ 👈 Zur Seite wischen oder Buttons nutzen 👉 ✨</span>
      </div>

      <!-- OPENED BOOK CONTAINER -->
      <div id="book-opened" class="reveal" style="max-width: 860px; margin: 0 auto; position: relative; perspective: 1500px;">
        
        <!-- Book Page Atmosphere Particle Container -->
        <div id="book-particles-container" style="position: absolute; top:0; left:0; width:100%; height:100%; pointer-events: none; overflow: hidden; z-index: 10;"></div>

        <!-- MAGICAL BOOK FRAME (CLEAN LUXURY DESIGN WITHOUT CROSS LINES) -->
        <div class="book-folio" id="book-folio-touch-zone">
          <!-- DYNAMIC PAGE CONTENT WITH 3D FLIP CONTAINER -->
          <div id="book-page-body" class="book-page-content">
            <!-- Rendered by JS -->
          </div>
        </div>

        <!-- Book Navigation Bar -->
        <div class="book-controls">
          <button id="book-prev-btn" class="book-nav-btn" aria-label="Vorherige Seite">
            <span class="nav-arrow">❮</span> Vorherige Seite
          </button>
          
          <div class="book-page-status">
            <div id="book-page-indicator" class="book-indicator">Seite 1 von 6</div>
            <div class="book-progress-bar-wrap">
              <div id="book-progress-fill" class="book-progress-fill" style="width: 16.6%;"></div>
            </div>
          </div>

          <button id="book-next-btn" class="book-nav-btn" aria-label="Nächste Seite">
            Nächste Seite <span class="nav-arrow">❯</span>
          </button>
        </div>

      </div>
    </section>"""

# 2. CSS (CLEAN LUXURY PARCHMENT, NO CROSSES, SILENT SMOOTH FLIP)
new_storybook_css = """
/* ==========================================
   STORYBOOK CSS & CLEAN LUXURY AESTHETICS
   ========================================== */
.theme-storybook {
  background: radial-gradient(circle at 50% 20%, rgba(157, 78, 221, 0.15) 0%, rgba(9, 10, 15, 0.98) 75%);
  border-top: 1px solid rgba(229,184,105,0.3);
  position: relative;
  padding: 80px 15px;
}

.book-ambient-glow {
  position: absolute;
  top: 5%;
  left: 50%;
  transform: translateX(-50%);
  width: 550px;
  height: 550px;
  background: radial-gradient(circle, rgba(157, 78, 221, 0.18) 0%, rgba(229,184,105,0.08) 50%, transparent 70%);
  pointer-events: none;
  animation: pulseGlow 6s ease-in-out infinite alternate;
}

.book-swipe-badge {
  display: inline-block;
  background: rgba(229, 184, 105, 0.12);
  border: 1px solid rgba(229, 184, 105, 0.4);
  color: var(--gold);
  padding: 6px 18px;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: bold;
  letter-spacing: 0.5px;
  box-shadow: 0 0 15px rgba(229, 184, 105, 0.15);
}

.book-folio {
  background: linear-gradient(145deg, #1d1526 0%, #120c1a 50%, #1a1324 100%);
  border: 2px solid rgba(229, 184, 105, 0.45);
  border-radius: 24px;
  padding: 40px 32px;
  min-height: 500px;
  position: relative;
  box-shadow: 0 25px 70px rgba(0,0,0,0.9), 0 0 45px rgba(157, 78, 221, 0.25), inset 0 0 35px rgba(0,0,0,0.6);
  backdrop-filter: blur(14px);
  text-align: left;
  user-select: none;
  touch-action: pan-y;
  transform-style: preserve-3d;
}

/* DISNEY 3D PAGE FLIP ANIMATIONS */
.book-page-content {
  position: relative;
  z-index: 2;
  transform-origin: center center;
  transition: transform 0.45s cubic-bezier(0.25, 1, 0.5, 1), opacity 0.45s ease;
}

.book-page-flip-forward {
  animation: disneyFlipForward 0.5s cubic-bezier(0.4, 0, 0.2, 1) forwards;
}

.book-page-flip-backward {
  animation: disneyFlipBackward 0.5s cubic-bezier(0.4, 0, 0.2, 1) forwards;
}

@keyframes disneyFlipForward {
  0% { transform: perspective(1000px) rotateY(0deg) scale(1); opacity: 1; filter: drop-shadow(0 0 0px gold); }
  50% { transform: perspective(1000px) rotateY(-35deg) scale(0.96); opacity: 0.4; filter: drop-shadow(0 0 15px rgba(229,184,105,0.4)); }
  100% { transform: perspective(1000px) rotateY(0deg) scale(1); opacity: 1; filter: drop-shadow(0 0 0px gold); }
}

@keyframes disneyFlipBackward {
  0% { transform: perspective(1000px) rotateY(0deg) scale(1); opacity: 1; filter: drop-shadow(0 0 0px gold); }
  50% { transform: perspective(1000px) rotateY(35deg) scale(0.96); opacity: 0.4; filter: drop-shadow(0 0 15px rgba(229,184,105,0.4)); }
  100% { transform: perspective(1000px) rotateY(0deg) scale(1); opacity: 1; filter: drop-shadow(0 0 0px gold); }
}

.book-page-header {
  border-bottom: 1px solid rgba(229,184,105,0.25);
  padding-bottom: 14px;
  margin-bottom: 22px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.book-page-title {
  font-family: 'Playfair Display', serif;
  color: var(--gold);
  font-size: 1.65rem;
  margin: 0;
  text-shadow: 0 0 12px rgba(229,184,105,0.3);
}

.book-chapter-num {
  font-family: 'DM Mono', monospace;
  font-size: 0.85rem;
  color: var(--rose);
  text-transform: uppercase;
  letter-spacing: 2.5px;
  font-weight: bold;
}

.book-quote-box {
  background: rgba(255,255,255,0.04);
  border-left: 4px solid var(--gold);
  padding: 18px 22px;
  border-radius: 0 14px 14px 0;
  margin: 20px 0;
  font-style: italic;
  font-size: 1.05rem;
  line-height: 1.8;
  color: #f8fafc;
  box-shadow: 0 4px 20px rgba(0,0,0,0.3);
}

/* Secret Note Flap */
.book-secret-flap {
  background: rgba(229, 184, 105, 0.08);
  border: 1px dashed rgba(229, 184, 105, 0.5);
  border-radius: 14px;
  padding: 16px 20px;
  margin-top: 22px;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(0,0,0,0.2);
}

.book-secret-flap:hover {
  background: rgba(229, 184, 105, 0.15);
  border-color: var(--gold);
  transform: translateY(-2px);
  box-shadow: 0 6px 22px rgba(229, 184, 105, 0.2);
}

.book-flap-title {
  color: var(--gold);
  font-weight: bold;
  font-size: 1rem;
  display: flex;
  align-items: center;
  gap: 10px;
}

.book-flap-content {
  margin-top: 14px;
  padding-top: 12px;
  border-top: 1px solid rgba(229,184,105,0.25);
  font-size: 0.98rem;
  line-height: 1.7;
  color: #e2e8f0;
  display: none;
  animation: fadeIn 0.4s ease-out;
}

/* Controls */
.book-controls {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 30px;
  gap: 15px;
  flex-wrap: wrap;
}

.book-nav-btn {
  background: linear-gradient(135deg, rgba(229,184,105,0.25), rgba(255,77,109,0.25));
  border: 1px solid rgba(229,184,105,0.6);
  color: #fff;
  padding: 14px 26px;
  border-radius: 30px;
  cursor: pointer;
  font-weight: bold;
  font-size: 1rem;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  box-shadow: 0 6px 20px rgba(0,0,0,0.4);
}

.book-nav-btn:hover:not(:disabled) {
  background: linear-gradient(135deg, var(--gold), var(--rose));
  color: #000;
  box-shadow: 0 0 25px rgba(229,184,105,0.6);
  transform: translateY(-3px) scale(1.03);
}

.book-nav-btn:disabled {
  opacity: 0.25;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.nav-arrow {
  font-size: 1.2rem;
  line-height: 1;
}

.book-page-status {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
}

.book-indicator {
  font-family: 'DM Mono', monospace;
  color: var(--gold);
  font-size: 1rem;
  font-weight: bold;
  letter-spacing: 1px;
}

.book-progress-bar-wrap {
  width: 140px;
  height: 4px;
  background: rgba(255,255,255,0.1);
  border-radius: 4px;
  overflow: hidden;
}

.book-progress-fill {
  height: 100%;
  background: linear-gradient(90deg, var(--rose), var(--gold));
  border-radius: 4px;
  transition: width 0.4s ease;
}

.book-particle-fly {
  position: absolute;
  pointer-events: none;
  user-select: none;
  animation: bookFly linear forwards;
}

@keyframes bookFly {
  0% { transform: translateY(100%) scale(0.6) rotate(0deg); opacity: 0; }
  20% { opacity: 0.9; }
  80% { opacity: 0.9; }
  100% { transform: translateY(-30%) scale(1.3) rotate(25deg); opacity: 0; }
}
"""

# 3. FRESH JAVASCRIPT: 100% NEW DIALOGS & QUOTES, SILENT PAGE FLIP, MATCHING INTERACTIONS
new_storybook_js = """
      // ==========================================
      // DAS BUCH UNSERES LEBENS (100% FRESH CHAT STORIES & SILENT FLIP)
      // ==========================================

      const bookPages = [
        {
          num: 'Kapitel I',
          title: 'Die 1-Uhr-Nachts Philosophie',
          icon: '🌙 🦉 💭',
          particles: ['🌙', '✨', '⭐', '🦉', '💫'],
          html: `
            <p style="color: #cbd5e1; font-size: 1.02rem; line-height: 1.75;">
              Wahres Glück besteht darin, mitten in der Nacht über die tiefsten Gedanken oder den herrlichsten Blödsinn sprechen zu können, 
              ohne sich auch nur eine Sekunde lang verstellen zu müssen.
            </p>
            <div class="book-quote-box">
              "Liebe ist nicht nur große Gesten und romantische Worte, sondern auch ein Chat voller Blödsinn um 1 Uhr nachts, dumme Insider und das Wissen, dass der andere genauso verrückt ist wie man selbst."<br>
              <span style="color: var(--gold); font-size: 0.9rem; font-weight: bold; display: block; margin-top: 6px;">— Denis (26.03.)</span>
            </div>
            <div class="book-secret-flap" onclick="toggleBookFlap(this)">
              <div class="book-flap-title">🤫 Aufklappbare Geheim-Notiz: Über das Kindisch-Bleiben ▾</div>
              <div class="book-flap-content">
                Denis schrieb dir mal: <em>"Ich finde es schön, wenn man noch kindisch sein kann. Ich tu zu keiner einzigen Sekunde so, als wäre ich jemand anderes vor dir."</em> Genau diese Ehrlichkeit macht uns unzertrennlich.
              </div>
            </div>
            <div style="margin-top: 22px; background: rgba(0,0,0,0.3); padding: 15px; border-radius: 12px; text-align: center;">
              <p style="font-size: 0.88rem; color: #a1b0c0; margin-bottom: 10px;">Lass die Nachtsterne tanzen:</p>
              <button class="action-btn" style="font-size: 0.92rem; padding: 8px 20px;" onclick="spawnBookParticles(['🌙','✨','⭐','💫']);">✨ Nachtlichter entzünden</button>
            </div>
          `
        },
        {
          num: 'Kapitel II',
          title: 'Die Peperoni-Chroniken & Das Teppich-Drama',
          icon: '🌶️ 🛋️ 🤣',
          particles: ['🌶️', '🔥', '🤣', '🛋️', '💖'],
          html: `
            <p style="color: #cbd5e1; font-size: 1.02rem; line-height: 1.75;">
              Unser Humor ist legendär. Vom Kosenamen <em>"Peperoni"</em> bis hin zu Denis' verzweifeltem Versuch, 
              die Wohnung für Selly perfekt einzurichten – nur um sich wieder necken zu lassen.
            </p>
            <div class="book-quote-box">
              "Gute Nacht, du wunderschöne, atemberaubende, unfassbar scharfe Peperoni! Mögest du von den schönsten Dingen träumen..."<br>
              <span style="color: var(--rose); font-size: 0.9rem; font-weight: bold; display: block; margin-top: 6px;">— Denis (05.03.)</span>
            </div>
            <div class="book-secret-flap" onclick="toggleBookFlap(this)">
              <div class="book-flap-title">🛋️ Aufklappbare Geheim-Notiz: Die Sache mit dem Teppich ▾</div>
              <div class="book-flap-content">
                Denis: <em>"Ich hab NUR einen neuen Teppich gekauft, weil du den alten nicht schön fandest. Du meckerst aber schon wieder..."</em> 😂 Egal wie viel gefrotselt wird: Du bist die Einzige, die ihn in 2 Sekunden zum Lachen bringt.
              </div>
            </div>
            <div style="margin-top: 22px; background: rgba(0,0,0,0.3); padding: 15px; border-radius: 12px; text-align: center;">
              <p style="font-size: 0.88rem; color: #a1b0c0; margin-bottom: 10px;">Schärfegrad testen:</p>
              <button class="action-btn" style="font-size: 0.92rem; padding: 8px 20px;" onclick="spawnBookParticles(['🌶️','🔥','💥','💖']);">🌶️ Peperoni-Funken sprühen</button>
            </div>
          `
        },
        {
          num: 'Kapitel III',
          title: 'Die Festung der Ehrlichkeit',
          icon: '🛡️ 🔐 💎',
          particles: ['🛡️', '💎', '✨', '🔐', '💙'],
          html: `
            <p style="color: #cbd5e1; font-size: 1.02rem; line-height: 1.75;">
              In einer oberflächlichen Welt haben wir einen Ort erschaffen, an dem kein Platz für Zweifel, Spiele oder Distanz ist. 
              Hier zählt nur die 100%ige Echtheit unseres Bandes.
            </p>
            <div class="book-quote-box">
              "Frag mich doch einfach. Ich würde dich niemals abwimmeln, egal vor wem. Ich will diese Liebe – ich will es so sehr."<br>
              <span style="color: #60a5fa; font-size: 0.9rem; font-weight: bold; display: block; margin-top: 6px;">— Denis (19.11.)</span>
            </div>
            <div class="book-secret-flap" onclick="toggleBookFlap(this)">
              <div class="book-flap-title">💭 Aufklappbare Geheim-Notiz: Warum es keine Zweifel gibt ▾</div>
              <div class="book-flap-content">
                Denis: <em>"Jedes Foto, alles was du sagst, deine Stimme – alles ist bei mir im Kopf. Und du fragst ernsthaft, ob ich dich noch mag..."</em> Du bist fest in seinem Herzen verankert.
              </div>
            </div>
            <div style="margin-top: 22px; background: rgba(0,0,0,0.3); padding: 15px; border-radius: 12px; text-align: center;">
              <p style="font-size: 0.88rem; color: #a1b0c0; margin-bottom: 10px;">Schutzring aktivieren:</p>
              <button class="action-btn" style="font-size: 0.92rem; padding: 8px 20px;" onclick="spawnBookParticles(['🛡️','💎','✨','💙']);">🛡️ Ewigen Schutzschild stärken</button>
            </div>
          `
        },
        {
          num: 'Kapitel IV',
          title: 'Das Zirbenholz-Gefühl & Die kleinen Rituale',
          icon: '🌲 ☕ 🍃',
          particles: ['🌲', '🍃', '🌿', '✨', '☕'],
          html: `
            <p style="color: #cbd5e1; font-size: 1.02rem; line-height: 1.75;">
              Es sind die gemütlichen, warmen Momente: Der Duft von Zirbenholz im Schlafzimmer, Gedanken an gemeinsames Kochen 
              und das Gefühl, nach einem langen Tag endlich den Kopf an die richtige Schulter zu lehnen.
            </p>
            <div class="book-quote-box">
              "Das ganze Schlafzimmer riecht nach Wald, frischem Holz und Baumharz... genau so fühlt sich vollkommene Ruhe an."<br>
              <span style="color: var(--mint); font-size: 0.9rem; font-weight: bold; display: block; margin-top: 6px;">— Selly (19.01.)</span>
            </div>
            <div class="book-secret-flap" onclick="toggleBookFlap(this)">
              <div class="book-flap-title">🍳 Aufklappbare Geheim-Notiz: Sellys Kochversprechen ▾</div>
              <div class="book-flap-content">
                Selly gestand im Chat: <em>"Wenn ich dich hätte, dann würde ich pausenlos kochen, ich wäre so glücklich..."</em> Die besten Abende werden in unserer gemeinsamen Küche stattfinden!
              </div>
            </div>
            <div style="margin-top: 22px; background: rgba(0,0,0,0.3); padding: 15px; border-radius: 12px; text-align: center;">
              <p style="font-size: 0.88rem; color: #a1b0c0; margin-bottom: 10px;">Waldfrische entfalten:</p>
              <button class="action-btn" style="font-size: 0.92rem; padding: 8px 20px;" onclick="spawnBookParticles(['🌲','🍃','🌿','💚']);">🍃 Zirben-Aroma spüren</button>
            </div>
          `
        },
        {
          num: 'Kapitel V',
          title: 'Eine echte Persönlichkeit',
          icon: '👑 🌸 ☀️',
          particles: ['👑', '🌸', '☀️', '💖', '✨'],
          html: `
            <p style="color: #cbd5e1; font-size: 1.02rem; line-height: 1.75;">
              Was Denis von der ersten Sekunde an fasziniert hat, war nicht nur deine Schönheit, 
              sondern dein unverwechselbarer Charakter – schlagfertig, herzlich und unbezwingbar stark.
            </p>
            <div class="book-quote-box">
              "Selly ist eine echte Persönlichkeit – jemand, der mit Humor, Schlagfertigkeit und einem charmanten Hauch von Frechheit durchs Leben geht."<br>
              <span style="color: var(--purple); font-size: 0.9rem; font-weight: bold; display: block; margin-top: 6px;">— Denis (15.03.)</span>
            </div>
            <div class="book-secret-flap" onclick="toggleBookFlap(this)">
              <div class="book-flap-title">🌸 Aufklappbare Geheim-Notiz: Dein großes Herz ▾</div>
              <div class="book-flap-content">
                Egal wie viele Steine dir das Leben in den Weg gelegt hat: Deine Fähigkeit, für andere da zu sein, zu lieben und zu strahlen, ist das Schönste auf diesem Planeten.
              </div>
            </div>
            <div style="margin-top: 22px; background: rgba(0,0,0,0.3); padding: 15px; border-radius: 12px; text-align: center;">
              <p style="font-size: 0.88rem; color: #a1b0c0; margin-bottom: 10px;">Königinnen-Krone aufsetzen:</p>
              <button class="action-btn" style="font-size: 0.92rem; padding: 8px 20px;" onclick="spawnBookParticles(['👑','🌸','💖','✨']);">👑 Glanz entfachen</button>
            </div>
          `
        },
        {
          num: 'Kapitel VI',
          title: 'Das schönste Geschenk des Lebens',
          icon: '🎁 ♾️ ❤️',
          particles: ['❤️', '💖', '💎', '♾️', '✨'],
          html: `
            <p style="color: #cbd5e1; font-size: 1.02rem; line-height: 1.75;">
              Das Leben schenkt einem viele Tage, aber nur einmal einen Menschen, der das ganze Dasein mit Sinn und Licht erfüllt.
            </p>
            <div class="book-quote-box">
              "Du bist das absolut Schönste, was mir in meinem ganzen Leben passiert ist. Ich danke dem Schicksal für jeden Tag an deiner Seite."<br>
              <span style="color: var(--gold); font-size: 0.9rem; font-weight: bold; display: block; margin-top: 6px;">— Denis & Selly (Für immer)</span>
            </div>
            <div class="book-secret-flap" onclick="toggleBookFlap(this)">
              <div class="book-flap-title">♾️ Aufklappbare Geheim-Notiz: Für alle Zeiten ▾</div>
              <div class="book-flap-content">
                Kein Buch dieser Welt hat genug Seiten, um zu beschreiben, wie sehr du geliebt wirst. Unsere Geschichte hat gerade erst begonnen.
              </div>
            </div>
            <div style="margin-top: 25px; text-align: center;">
              <button class="action-btn" style="font-size: 1.05rem; padding: 12px 30px; background: var(--gradient-brand);" onclick="spawnBookParticles(['❤️','💖','💎','♾️','✨']);">
                ❤️ Herzensband besiegeln
              </button>
            </div>
          `
        }
      ];

      let currentBookPage = 0;
      let bookParticleInterval = null;

      function renderBookPage(index, direction = 'none') {
        currentBookPage = index;
        const page = bookPages[index];
        const container = $('#book-page-body');
        if (!container) return;

        // Apply Disney 3D page flip animation
        container.classList.remove('book-page-flip-forward', 'book-page-flip-backward');
        if (direction === 'forward') {
          container.classList.add('book-page-flip-forward');
        } else if (direction === 'backward') {
          container.classList.add('book-page-flip-backward');
        }

        setTimeout(() => {
          container.innerHTML = `
            <div class="book-page-header">
              <div>
                <span class="book-chapter-num">${page.num}</span>
                <h3 class="book-page-title">${page.title}</h3>
              </div>
              <div style="font-size: 1.8rem; filter: drop-shadow(0 0 10px gold);">${page.icon}</div>
            </div>
            ${page.html}
          `;
          
          $('#book-page-indicator').innerText = `Seite ${index + 1} von ${bookPages.length}`;
          $('#book-progress-fill').style.width = ((index + 1) / bookPages.length * 100) + '%';
          
          $('#book-prev-btn').disabled = (index === 0);
          $('#book-next-btn').disabled = (index === bookPages.length - 1);

          // Restart dynamic page particles
          startBookParticles(page.particles);
        }, 100);
      }

      // SILENT PAGE FLIPS (NO AUDIO AS REQUESTED)
      function flipBookNext() {
        if (currentBookPage < bookPages.length - 1) {
          renderBookPage(currentBookPage + 1, 'forward');
        }
      }

      function flipBookPrev() {
        if (currentBookPage > 0) {
          renderBookPage(currentBookPage - 1, 'backward');
        }
      }

      function toggleBookFlap(el) {
        const content = el.querySelector('.book-flap-content');
        if (!content) return;
        if (content.style.display === 'block') {
          content.style.display = 'none';
        } else {
          content.style.display = 'block';
        }
      }

      function spawnBookParticles(icons) {
        const host = $('#book-particles-container');
        if (!host) return;
        for(let i = 0; i < 6; i++) {
          const p = document.createElement('div');
          p.className = 'book-particle-fly';
          p.innerText = icons[Math.floor(Math.random() * icons.length)];
          p.style.left = (Math.random() * 90 + 5) + '%';
          p.style.fontSize = (Math.random() * 16 + 14) + 'px';
          const dur = Math.random() * 3 + 3;
          p.style.animationDuration = dur + 's';
          host.appendChild(p);
          setTimeout(() => p.remove(), dur * 1000);
        }
      }

      function startBookParticles(icons) {
        if (bookParticleInterval) clearInterval(bookParticleInterval);
        bookParticleInterval = setInterval(() => {
          spawnBookParticles(icons);
        }, 1800);
      }

      // Hook up buttons
      $('#book-prev-btn')?.addEventListener('click', flipBookPrev);
      $('#book-next-btn')?.addEventListener('click', flipBookNext);

      // TOUCH SWIPE SUPPORT FOR MOBILE & TABLETS
      let touchStartX = 0;
      let touchStartY = 0;
      const touchZone = $('#book-folio-touch-zone');

      if (touchZone) {
        touchZone.addEventListener('touchstart', (e) => {
          touchStartX = e.changedTouches[0].screenX;
          touchStartY = e.changedTouches[0].screenY;
        }, { passive: true });

        touchZone.addEventListener('touchend', (e) => {
          const touchEndX = e.changedTouches[0].screenX;
          const touchEndY = e.changedTouches[0].screenY;
          const deltaX = touchEndX - touchStartX;
          const deltaY = touchEndY - touchStartY;

          // Only trigger if horizontal swipe is prominent
          if (Math.abs(deltaX) > 45 && Math.abs(deltaX) > Math.abs(deltaY) * 1.2) {
            if (deltaX < 0) {
              // Swiped left -> Next page
              flipBookNext();
            } else {
              // Swiped right -> Previous page
              flipBookPrev();
            }
          }
        }, { passive: true });
      }

      // Initial direct render on page load
      renderBookPage(0);
"""

# Replace HTML
sb_html_pattern = re.compile(r'<!-- DAS BUCH UNSERES LEBENS.*?<!-- EIN KANAL ZU UNSEREN HERZEN -->', re.DOTALL)
if sb_html_pattern.search(code):
    code = sb_html_pattern.sub(new_storybook_html + '\n\n    <!-- EIN KANAL ZU UNSEREN HERZEN -->', code)
    print("Replaced Storybook HTML successfully!")
else:
    print("HTML pattern not found!")

# Replace CSS
sb_css_pattern = re.compile(r'/\* ==========================================\s*STORYBOOK CSS.*?\*/.*?(?=\.theme-kapelle|</style>)', re.DOTALL)
if sb_css_pattern.search(code):
    code = sb_css_pattern.sub(new_storybook_css + '\n', code)
    print("Replaced Storybook CSS successfully!")
else:
    print("CSS pattern not found!")

# Replace JS
sb_js_pattern = re.compile(r'// ==========================================\s*DAS BUCH UNSERES LEBENS.*?renderBookPage\(0\);?', re.DOTALL)
if sb_js_pattern.search(code):
    code = sb_js_pattern.sub(new_storybook_js, code)
    print("Replaced Storybook JS successfully!")
else:
    print("JS pattern not found!")

with open('build_new_app.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("build_new_app.py updated with fresh content and silent page flips!")
