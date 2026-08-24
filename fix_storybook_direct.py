import re

with open('build_new_app.py', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. NEW HTML (OPEN BY DEFAULT, SWIPE HINT, GORGEOUS CONTROLS)
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

        <!-- MAGICAL BOOK FRAME -->
        <div class="book-folio" id="book-folio-touch-zone">
          <div class="book-spine-center"></div>
          <div class="book-corner-gold tl">⚜️</div>
          <div class="book-corner-gold tr">⚜️</div>
          <div class="book-corner-gold bl">⚜️</div>
          <div class="book-corner-gold br">⚜️</div>

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

# 2. NEW CSS (DISNEY-LIKE PAGE FLIP, GLOWING BORDERS, TOUCH GESTURES)
new_storybook_css = """
/* ==========================================
   STORYBOOK CSS & DISNEY-LIKE MAGIC
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
  background: linear-gradient(135deg, #1f1728 0%, #120c19 50%, #1f1728 100%);
  border: 3px double rgba(229, 184, 105, 0.6);
  border-radius: 22px;
  padding: 40px 30px;
  min-height: 520px;
  position: relative;
  box-shadow: 0 25px 70px rgba(0,0,0,0.9), 0 0 45px rgba(157, 78, 221, 0.2), inset 0 0 40px rgba(0,0,0,0.7);
  backdrop-filter: blur(14px);
  text-align: left;
  user-select: none;
  touch-action: pan-y;
  transform-style: preserve-3d;
}

.book-corner-gold {
  position: absolute;
  font-size: 1.3rem;
  color: var(--gold);
  opacity: 0.85;
  filter: drop-shadow(0 0 8px gold);
  pointer-events: none;
}
.book-corner-gold.tl { top: 12px; left: 15px; }
.book-corner-gold.tr { top: 12px; right: 15px; }
.book-corner-gold.bl { bottom: 12px; left: 15px; }
.book-corner-gold.br { bottom: 12px; right: 15px; }

.book-spine-center {
  position: absolute;
  top: 0;
  bottom: 0;
  left: 50%;
  width: 3px;
  background: linear-gradient(180deg, transparent, rgba(229,184,105,0.3) 20%, rgba(229,184,105,0.3) 80%, transparent);
  box-shadow: 0 0 20px rgba(0,0,0,0.9);
  pointer-events: none;
}

/* DISNEY 3D PAGE FLIP ANIMATIONS */
.book-page-content {
  position: relative;
  z-index: 2;
  transform-origin: center center;
  transition: transform 0.5s cubic-bezier(0.25, 1, 0.5, 1), opacity 0.5s ease;
}

.book-page-flip-forward {
  animation: disneyFlipForward 0.55s cubic-bezier(0.4, 0, 0.2, 1) forwards;
}

.book-page-flip-backward {
  animation: disneyFlipBackward 0.55s cubic-bezier(0.4, 0, 0.2, 1) forwards;
}

@keyframes disneyFlipForward {
  0% { transform: perspective(1000px) rotateY(0deg) scale(1); opacity: 1; filter: drop-shadow(0 0 0px gold); }
  50% { transform: perspective(1000px) rotateY(-40deg) scale(0.95); opacity: 0.4; filter: drop-shadow(0 0 20px gold); }
  100% { transform: perspective(1000px) rotateY(0deg) scale(1); opacity: 1; filter: drop-shadow(0 0 0px gold); }
}

@keyframes disneyFlipBackward {
  0% { transform: perspective(1000px) rotateY(0deg) scale(1); opacity: 1; filter: drop-shadow(0 0 0px gold); }
  50% { transform: perspective(1000px) rotateY(40deg) scale(0.95); opacity: 0.4; filter: drop-shadow(0 0 20px gold); }
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
  background: rgba(255,255,255,0.035);
  border-left: 4px solid var(--gold);
  padding: 18px 22px;
  border-radius: 0 14px 14px 0;
  margin: 20px 0;
  font-style: italic;
  font-size: 1.08rem;
  line-height: 1.8;
  color: #f8fafc;
  box-shadow: 0 4px 20px rgba(0,0,0,0.3);
}

/* Secret Note Flap */
.book-secret-flap {
  background: rgba(229, 184, 105, 0.09);
  border: 1px dashed rgba(229, 184, 105, 0.5);
  border-radius: 14px;
  padding: 16px 20px;
  margin-top: 22px;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(0,0,0,0.2);
}

.book-secret-flap:hover {
  background: rgba(229, 184, 105, 0.16);
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

# 3. NEW JS (TOUCH SWIPE, DIRECT INITIALIZATION, SOUNDS, DISNEY FLIP)
new_storybook_js = """
      // ==========================================
      // DAS BUCH UNSERES LEBENS (DISNEY FLIP & TOUCH SWIPE)
      // ==========================================

      const bookPages = [
        {
          num: 'Kapitel I',
          title: 'Der erste Funke & Die endlosen Nächte',
          icon: '✨ 🌙 💫',
          particles: ['✨', '🌙', '💫', '⭐', '🌌'],
          html: `
            <p style="color: #cbd5e1; font-size: 1.02rem; line-height: 1.75;">
              Es begann alles mit einer scheinbar zufälligen Nachricht und wuchs zu etwas heran, das jeden Gedanken erfüllte. 
              Wir haben Nächte durchtelefoniert, gelacht bis der Bauch wehtat, und plötzlich war Schlaf völlig zweitrangig.
            </p>
            <div class="book-quote-box">
              "Das heißt ich liebe dich mein Herz, der Kern meiner Gedanken, die Melodie meines Lebens..."<br>
              <span style="color: var(--gold); font-size: 0.9rem; font-weight: bold; display: block; margin-top: 6px;">— Denis</span>
            </div>
            <div class="book-secret-flap" onclick="toggleBookFlap(this)">
              <div class="book-flap-title">💌 Aufklappbare Geheim-Notiz: Warum du mir den Schlaf geraubt hast ▾</div>
              <div class="book-flap-content">
                Du hast mal gesagt: <em>"Wenn du mich arg vermisst und mich hören willst, ruf mich einfach an, der Schlaf ist mir egal..."</em>. 
                Es gab keine einzige Nacht, in der deine Stimme nicht das Allerschönste am gesamten Tag war.
              </div>
            </div>
            <div style="margin-top: 22px; background: rgba(0,0,0,0.3); padding: 15px; border-radius: 12px; text-align: center;">
              <p style="font-size: 0.88rem; color: #a1b0c0; margin-bottom: 10px;">Spüre den Nachtschwärmer-Zauber:</p>
              <button class="action-btn" style="font-size: 0.92rem; padding: 8px 20px;" onclick="playNightSparkle()">✨ Sternschnuppe losschicken</button>
            </div>
          `
        },
        {
          num: 'Kapitel II',
          title: 'Die Sprache unseres Herzens & Der Palast',
          icon: '🐌 🐾 🥣',
          particles: ['🐾', '🐌', '🥒', '🥣', '💖'],
          html: `
            <p style="color: #cbd5e1; font-size: 1.02rem; line-height: 1.75;">
              Eine Liebe erkennt man an den tausend kleinen Insidern, die nur wir zwei verstehen. 
              Vom Rekord-Kosenamen <em>"Schnecke"</em> über die legendäre Gurken-Joghurt-Diät bis hin zur absoluten Herrschaft von Suri und Pamuk.
            </p>
            <div class="book-quote-box">
              "Suri ist die unangefochtene Bett-Blockiererin und Chefin, während Pamuk lieber auf Bäume klettert und das Chaos regiert."<br>
              <span style="color: var(--mint); font-size: 0.9rem; font-weight: bold; display: block; margin-top: 6px;">— Das Hofprotokoll des Palastes</span>
            </div>
            <div class="book-secret-flap" onclick="toggleBookFlap(this)">
              <div class="book-flap-title">🐾 Aufklappbare Geheim-Notiz: Die Wahrheit über 'Schnecke' ▾</div>
              <div class="book-flap-content">
                Über 1.198 Mal habe ich dich so genannt. Egal wie verrückt die Welt war – wenn ich 'Schnecke' gesagt habe, wussten wir beide genau, wo unser Zuhause ist.
              </div>
            </div>
            <div style="margin-top: 22px; background: rgba(0,0,0,0.3); padding: 15px; border-radius: 12px; text-align: center;">
              <p style="font-size: 0.88rem; color: #a1b0c0; margin-bottom: 10px;">Katzengruß aktivieren:</p>
              <button class="action-btn" style="font-size: 0.92rem; padding: 8px 20px;" onclick="playSweetMeow(); spawnBookParticles(['🐾','😻','💖']);">🐾 Suri & Pamuk schnurren lassen</button>
            </div>
          `
        },
        {
          num: 'Kapitel III',
          title: 'Kintsugi: Gold in jeder Narbe',
          icon: '🏺 💛 ✨',
          particles: ['✨', '💛', '🌟', '💫'],
          html: `
            <p style="color: #cbd5e1; font-size: 1.02rem; line-height: 1.75;">
              Wir haben beide unsere Rucksäcke und Wunden aus der Vergangenheit mitgebracht. Doch anstatt davor wegzulaufen, 
              haben wir gelernt, sie wie im japanischen Kintsugi mit flüssigem Gold zu verbinden.
            </p>
            <div class="book-quote-box">
              "Wir müssen mehr Liebe füreinander zeigen, nicht streiten, Geduld zeigen, wir müssen füreinander da sein. Wenn einer von uns im Stress steht, ist der andere der sichere Fels in der Brandung."<br>
              <span style="color: var(--gold); font-size: 0.9rem; font-weight: bold; display: block; margin-top: 6px;">— Unser gemeinsamer Felsen-Schwur</span>
            </div>
            <div class="book-secret-flap" onclick="toggleBookFlap(this)">
              <div class="book-flap-title">🛡️ Aufklappbare Geheim-Notiz: Der sichere Hafen ▾</div>
              <div class="book-flap-content">
                Egal wie sehr die Wellen draußen toben: Bei mir darfst du die Rüstung ablegen. Du musst nicht stark sein, du musst nur du selbst sein.
              </div>
            </div>
            <div style="margin-top: 22px; background: rgba(0,0,0,0.3); padding: 15px; border-radius: 12px; text-align: center;">
              <p style="font-size: 0.88rem; color: #a1b0c0; margin-bottom: 10px;">Goldschimmer entfachen:</p>
              <button class="action-btn" style="font-size: 0.92rem; padding: 8px 20px;" onclick="playChime(); spawnBookParticles(['💛','✨','🌟']);">✨ Goldnaht berühren</button>
            </div>
          `
        },
        {
          num: 'Kapitel IV',
          title: 'Das Seelenband: Die Waldkapelle',
          icon: '🕊️ 🕯️ 🙏',
          particles: ['🕊️', '✨', '🤍', '🌿'],
          html: `
            <p style="color: #cbd5e1; font-size: 1.02rem; line-height: 1.75;">
              Der 24. August 2026 bewies endgültig, dass wir über ein unsichtbares, göttliches Band verbunden sind. 
              Vormittags der Gedanke durch die Nonne – nachmittags deine plötzliche Eingebung zur Waldkapelle.
            </p>
            <div class="book-quote-box">
              "Bitte hilf seinem Vater wieder gesund zu werden. Auf dass seiner Familie nie etwas zustoßen wird und er sein großes Glück finden wird. Bitte beschütze ihn für immer! 24.8.26 D.S.N"<br>
              <span style="color: var(--rose); font-size: 0.9rem; font-weight: bold; display: block; margin-top: 6px;">— Selly im Gästebuch der Kapelle</span>
            </div>
            <div class="book-secret-flap" onclick="toggleBookFlap(this)">
              <div class="book-flap-title">🕊️ Aufklappbare Geheim-Notiz: Was D.S.N wirklich bedeutet ▾</div>
              <div class="book-flap-content">
                Denis Saatloo & Selinda Nöckler. Nicht zwei getrennte Lebenswege, sondern eine gemeinsame Seele, die füreinander bittet und wacht.
              </div>
            </div>
            <div style="margin-top: 22px; background: rgba(0,0,0,0.3); padding: 15px; border-radius: 12px; text-align: center;">
              <p style="font-size: 0.88rem; color: #a1b0c0; margin-bottom: 10px;">Schutzsegen aussenden:</p>
              <button class="action-btn" style="font-size: 0.92rem; padding: 8px 20px;" onclick="playChime(); spawnBookParticles(['🕊️','✨','🙏','🤍']);">🕊️ Kanal der Herzen öffnen</button>
            </div>
          `
        },
        {
          num: 'Kapitel V',
          title: 'Der Blueprint unserer Zukunft',
          icon: '🏡 🗝️ ☀️',
          particles: ['🏡', '🗝️', '☀️', '🌸', '💖'],
          html: `
            <p style="color: #cbd5e1; font-size: 1.02rem; line-height: 1.75;">
              Vom ersten gemeinsamen Traumhaus mit Garten für die Katzen bis hin zu Kinderlachen und endlosen Sommern. 
              Unsere Zukunft ist kein loser Gedanke, sondern ein festes Fundament, das wir Stein für Stein bauen.
            </p>
            <div class="book-quote-box">
              "Gute Nacht mein größter Schatz, ich werde von dir und unseren Kindern träumen mein Herz, ich liebe dich..."<br>
              <span style="color: var(--purple); font-size: 0.9rem; font-weight: bold; display: block; margin-top: 6px;">— Selly</span>
            </div>
            <div class="book-secret-flap" onclick="toggleBookFlap(this)">
              <div class="book-flap-title">🗝️ Aufklappbare Geheim-Notiz: Der Schlüssel zur Zukunft ▾</div>
              <div class="book-flap-content">
                Ein Zuhause ist kein Gebäude mit vier Wänden – ein Zuhause ist der Ort, an dem du mir in die Augen schaust und sagst: 'Ich bin angekommen'.
              </div>
            </div>
            <div style="margin-top: 22px; background: rgba(0,0,0,0.3); padding: 15px; border-radius: 12px; text-align: center;">
              <p style="font-size: 0.88rem; color: #a1b0c0; margin-bottom: 10px;">Schlüssel umdrehen:</p>
              <button class="action-btn" style="font-size: 0.92rem; padding: 8px 20px;" onclick="playTada(); spawnBookParticles(['🗝️','🏡','✨','💖']);">🗝️ Tür zur Zukunft aufschließen</button>
            </div>
          `
        },
        {
          num: 'Kapitel VI',
          title: 'Das ewige Versprechen (150 Jahre)',
          icon: '♾️ 💍 ❤️',
          particles: ['❤️', '💖', '💎', '♾️', '👑'],
          html: `
            <p style="color: #cbd5e1; font-size: 1.02rem; line-height: 1.75;">
              Wir haben uns 150 Jahre und länger versprochen. Keine Laune der Natur, keine Distanz und keine Zeit kann jemals löschen, 
              was wir im tiefsten Kern füreinander empfinden.
            </p>
            <div class="book-quote-box">
              "Ich liebe dich dafür, dass ich dich kennen darf. Du hast ein so unfassbar gutes Herz... Ich liebe dich über alles auf dieser Welt."<br>
              <span style="color: var(--rose); font-size: 0.9rem; font-weight: bold; display: block; margin-top: 6px;">— Denis (Für immer)</span>
            </div>
            <div class="book-secret-flap" onclick="toggleBookFlap(this)">
              <div class="book-flap-title">♾️ Aufklappbare Geheim-Notiz: Das Siegel der Ewigkeit ▾</div>
              <div class="book-flap-content">
                Du bist mein Fels, meine Ruhe, mein größtes Glück und mein ganzes Leben. 150 Jahre reichen nicht aus – ich wähle dich für die Ewigkeit.
              </div>
            </div>
            <div style="margin-top: 25px; text-align: center;">
              <button class="action-btn" style="font-size: 1.1rem; padding: 14px 32px; background: var(--gradient-brand);" onclick="playTada(); spawnBookParticles(['❤️','💖','💎','♾️','✨']);">
                💍 Das Siegel der Ewigkeit bestätigen
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
        }, 120);
      }

      function flipBookNext() {
        if (currentBookPage < bookPages.length - 1) {
          playChime();
          renderBookPage(currentBookPage + 1, 'forward');
        }
      }

      function flipBookPrev() {
        if (currentBookPage > 0) {
          playChime();
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
          playChime();
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

      function playNightSparkle() {
        playChime();
        spawnBookParticles(['✨', '⭐', '💫', '🌙', '💖']);
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

          // Only trigger if horizontal swipe is prominent (not vertical scroll)
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

# Replace old storybook HTML block
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
    # Also check if it ends before renderApp
    sb_js_pattern2 = re.compile(r'// ==========================================\s*DAS BUCH UNSERES LEBENS.*?(?=renderApp\(\);)', re.DOTALL)
    if sb_js_pattern2.search(code):
        code = sb_js_pattern2.sub(new_storybook_js + '\n\n      ', code)
        print("Replaced Storybook JS via pattern 2!")

with open('build_new_app.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("build_new_app.py updated successfully!")
