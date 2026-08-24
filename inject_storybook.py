import re

# --- HTML FOR THE MAGICAL STORYBOOK ---
storybook_html = """
    <!-- DAS BUCH UNSERES LEBENS -->
    <section class="section theme-storybook" id="storybook-section" style="position: relative; overflow: hidden; text-align: center;">
      <div class="book-ambient-glow"></div>
      <span class="chapter-tag reveal" style="color: var(--gold); letter-spacing: 4px;">Das ewige Archiv</span>
      <h2 class="title reveal" style="color: #fff; text-shadow: 0 0 25px rgba(229,184,105,0.4);">Das Buch unseres Lebens</h2>
      <p class="section-desc reveal" style="max-width: 650px; margin: 0 auto 30px auto; color: #cbd5e1;">
        Eine handschriftliche Reise durch unsere Gedanken, Träume, geheimen Notizen und das Band zwischen unseren Seelen.
      </p>

      <!-- CLOSED BOOK (COVER) -->
      <div id="book-closed" class="reveal" style="margin: 30px auto; max-width: 440px; cursor: pointer; transition: transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);">
        <div class="book-cover-wrap">
          <div class="book-spine-decor"></div>
          <div class="book-corner tl">⚜️</div>
          <div class="book-corner tr">⚜️</div>
          <div class="book-corner bl">⚜️</div>
          <div class="book-corner br">⚜️</div>
          <div style="font-size: 3.5rem; margin-bottom: 10px; filter: drop-shadow(0 0 15px gold);">📖</div>
          <h3 style="font-family: 'Playfair Display', serif; color: var(--gold); font-size: 1.8rem; letter-spacing: 1px; margin-bottom: 8px;">
            Das Buch unseres Lebens
          </h3>
          <p style="color: var(--rose); font-family: 'DM Serif Display', serif; font-style: italic; font-size: 1.1rem; margin-bottom: 20px;">
            Denis & Selinda
          </p>
          <div class="book-ribbon-tag">
            ✨ Tippe, um das Buch aufzuschlagen ✨
          </div>
        </div>
      </div>

      <!-- OPENED BOOK CONTAINER -->
      <div id="book-opened" style="display: none; opacity: 0; max-width: 860px; margin: 20px auto; position: relative;">
        
        <!-- Book Page Atmosphere Particle Container -->
        <div id="book-particles-container" style="position: absolute; top:0; left:0; width:100%; height:100%; pointer-events: none; overflow: hidden; z-index: 5;"></div>

        <div class="book-folio">
          <div class="book-spine-center"></div>

          <!-- DYNAMIC PAGE CONTENT CONTAINER -->
          <div id="book-page-body" class="book-page-content">
            <!-- Will be populated via JS -->
          </div>
        </div>

        <!-- Book Navigation Bar -->
        <div class="book-controls">
          <button id="book-prev-btn" class="book-nav-btn">❮ Vorherige Seite</button>
          <div id="book-page-indicator" class="book-indicator">Seite 1 von 6</div>
          <button id="book-next-btn" class="book-nav-btn">Nächste Seite ❯</button>
        </div>

        <div style="margin-top: 15px;">
          <button id="book-close-btn" style="background: transparent; border: 1px solid rgba(255,255,255,0.2); color: #a1b0c0; border-radius: 20px; padding: 6px 18px; font-size: 0.85rem; cursor: pointer; transition: all 0.2s;">
            ✕ Buch schließen
          </button>
        </div>
      </div>

    </section>
"""

# --- CSS FOR THE STORYBOOK ---
storybook_css = """
/* ==========================================
   STORYBOOK CSS & AESTHETICS
   ========================================== */
.theme-storybook {
  background: radial-gradient(circle at 50% 20%, rgba(157, 78, 221, 0.1) 0%, rgba(9, 10, 15, 0.98) 75%);
  border-top: 1px solid rgba(229,184,105,0.25);
  position: relative;
}

.book-ambient-glow {
  position: absolute;
  top: 5%;
  left: 50%;
  transform: translateX(-50%);
  width: 500px;
  height: 500px;
  background: radial-gradient(circle, rgba(157, 78, 221, 0.12) 0%, rgba(229,184,105,0.06) 50%, transparent 70%);
  pointer-events: none;
  animation: pulseGlow 6s ease-in-out infinite alternate;
}

.book-cover-wrap {
  background: linear-gradient(135deg, #2b1725 0%, #15091c 60%, #2a1122 100%);
  border: 3px double rgba(229, 184, 105, 0.7);
  border-radius: 18px;
  padding: 40px 25px;
  position: relative;
  box-shadow: 0 15px 45px rgba(0,0,0,0.8), 0 0 35px rgba(157, 78, 221, 0.25), inset 0 0 25px rgba(0,0,0,0.7);
  overflow: hidden;
}

.book-cover-wrap:hover {
  transform: translateY(-6px) scale(1.02);
  box-shadow: 0 20px 55px rgba(0,0,0,0.9), 0 0 45px rgba(229, 184, 105, 0.35);
}

.book-spine-decor {
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 18px;
  background: linear-gradient(90deg, rgba(229,184,105,0.4), rgba(0,0,0,0.6));
  border-right: 1px solid rgba(229,184,105,0.3);
}

.book-corner {
  position: absolute;
  font-size: 1.2rem;
  color: var(--gold);
  opacity: 0.8;
}
.book-corner.tl { top: 10px; left: 25px; }
.book-corner.tr { top: 10px; right: 15px; }
.book-corner.bl { bottom: 10px; left: 25px; }
.book-corner.br { bottom: 10px; right: 15px; }

.book-ribbon-tag {
  display: inline-block;
  background: linear-gradient(90deg, var(--rose), var(--purple));
  color: #fff;
  padding: 8px 22px;
  border-radius: 25px;
  font-size: 0.95rem;
  font-weight: bold;
  box-shadow: 0 4px 15px rgba(255, 77, 109, 0.4);
  animation: pulseCandle 2.5s infinite;
}

/* OPENED BOOK FOLIO */
.book-folio {
  background: linear-gradient(135deg, #1b1622 0%, #110d18 50%, #1b1622 100%);
  border: 2px solid rgba(229, 184, 105, 0.45);
  border-radius: 20px;
  padding: 35px 25px;
  min-height: 480px;
  position: relative;
  box-shadow: 0 20px 60px rgba(0,0,0,0.85), inset 0 0 50px rgba(0,0,0,0.6);
  backdrop-filter: blur(12px);
  text-align: left;
}

.book-spine-center {
  position: absolute;
  top: 0;
  bottom: 0;
  left: 50%;
  width: 2px;
  background: linear-gradient(180deg, transparent, rgba(229,184,105,0.2) 20%, rgba(229,184,105,0.2) 80%, transparent);
  box-shadow: 0 0 15px rgba(0,0,0,0.8);
  pointer-events: none;
}

.book-page-content {
  position: relative;
  z-index: 2;
  transition: opacity 0.3s ease, transform 0.3s ease;
}

.book-page-header {
  border-bottom: 1px solid rgba(229,184,105,0.2);
  padding-bottom: 12px;
  margin-bottom: 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.book-page-title {
  font-family: 'Playfair Display', serif;
  color: var(--gold);
  font-size: 1.6rem;
  margin: 0;
}

.book-chapter-num {
  font-family: 'DM Mono', monospace;
  font-size: 0.85rem;
  color: var(--rose);
  text-transform: uppercase;
  letter-spacing: 2px;
}

.book-quote-box {
  background: rgba(255,255,255,0.03);
  border-left: 3px solid var(--gold);
  padding: 16px 20px;
  border-radius: 0 12px 12px 0;
  margin: 20px 0;
  font-style: italic;
  font-size: 1.05rem;
  line-height: 1.8;
  color: #f1f5f9;
}

/* Secret Note Flap */
.book-secret-flap {
  background: rgba(229, 184, 105, 0.08);
  border: 1px dashed rgba(229, 184, 105, 0.4);
  border-radius: 12px;
  padding: 15px;
  margin-top: 20px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.book-secret-flap:hover {
  background: rgba(229, 184, 105, 0.14);
  border-color: var(--gold);
}

.book-flap-title {
  color: var(--gold);
  font-weight: bold;
  font-size: 0.95rem;
  display: flex;
  align-items: center;
  gap: 8px;
}

.book-flap-content {
  margin-top: 12px;
  padding-top: 10px;
  border-top: 1px solid rgba(229,184,105,0.2);
  font-size: 0.95rem;
  line-height: 1.6;
  color: #cbd5e1;
  display: none;
  animation: fadeIn 0.4s ease-out;
}

/* Controls */
.book-controls {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 25px;
  gap: 10px;
}

.book-nav-btn {
  background: linear-gradient(135deg, rgba(229,184,105,0.2), rgba(255,77,109,0.2));
  border: 1px solid rgba(229,184,105,0.4);
  color: #fff;
  padding: 10px 22px;
  border-radius: 25px;
  cursor: pointer;
  font-weight: bold;
  font-size: 0.95rem;
  transition: all 0.2s ease;
}

.book-nav-btn:hover:not(:disabled) {
  background: linear-gradient(135deg, var(--gold), var(--rose));
  color: #000;
  box-shadow: 0 0 20px rgba(229,184,105,0.4);
  transform: translateY(-2px);
}

.book-nav-btn:disabled {
  opacity: 0.3;
  cursor: not-allowed;
}

.book-indicator {
  font-family: 'DM Mono', monospace;
  color: var(--gold);
  font-size: 0.95rem;
  letter-spacing: 1px;
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

# --- JAVASCRIPT LOGIC FOR THE STORYBOOK ---
storybook_js = """
      // ==========================================
      // DAS BUCH UNSERES LEBENS (STORYBOOK JS)
      // ==========================================

      const bookPages = [
        {
          num: 'Kapitel I',
          title: 'Der erste Funke & Die endlosen Nächte',
          icon: '✨ 🌙 💫',
          particles: ['✨', '🌙', '💫', '⭐', '🌌'],
          html: `
            <p style="color: #cbd5e1; font-size: 1rem; line-height: 1.7;">
              Es begann alles mit einer scheinbar zufälligen Nachricht und wuchs zu etwas heran, das den Schlaf zur Nebensache machte. 
              Wir haben Nächte durchtelefoniert, gelacht bis der Bauch wehtat, und plötzlich war da dieser Mensch, der die Gedanken völlig eingenommen hat.
            </p>
            <div class="book-quote-box">
              "Das heißt ich liebe dich mein Herz, der Kern meiner Gedanken, die Melodie meines Lebens..."<br>
              <span style="color: var(--gold); font-size: 0.9rem; font-weight: bold; display: block; margin-top: 6px;">— Denis</span>
            </div>
            <div class="book-secret-flap" onclick="toggleBookFlap(this)">
              <div class="book-flap-title">💌 Aufklappbare Geheim-Notiz: Warum du mir den Schlaf geraubt hast ▾</div>
              <div class="book-flap-content">
                Du hast mal gesagt: <em>"Wenn du mich arg vermisst und mich hören willst, ruf mich einfach an, der Schlaf ist mir egal..."</em>. 
                Es gab keine einzige Nacht, in der deine Stimme nicht das Schönste am ganzen Tag war.
              </div>
            </div>
            <div style="margin-top: 20px; background: rgba(0,0,0,0.3); padding: 15px; border-radius: 10px; text-align: center;">
              <p style="font-size: 0.85rem; color: #a1b0c0; margin-bottom: 8px;">Spüre die Nachtschwärmer-Magie:</p>
              <button class="action-btn" style="font-size: 0.9rem; padding: 6px 16px;" onclick="playNightSparkle()">✨ Sternschnuppe losschicken</button>
            </div>
          `
        },
        {
          num: 'Kapitel II',
          title: 'Die Sprache unseres Herzens & Der Palast',
          icon: '🐌 🐾 🥣',
          particles: ['🐾', '🐌', '🥒', '🥣', '💖'],
          html: `
            <p style="color: #cbd5e1; font-size: 1rem; line-height: 1.7;">
              Eine Liebe erkennt man nicht nur an großen Worten, sondern an den tausend kleinen Insidern, die nur wir zwei verstehen. 
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
            <div style="margin-top: 20px; background: rgba(0,0,0,0.3); padding: 15px; border-radius: 10px; text-align: center;">
              <p style="font-size: 0.85rem; color: #a1b0c0; margin-bottom: 8px;">Katzengruß aktivieren:</p>
              <button class="action-btn" style="font-size: 0.9rem; padding: 6px 16px;" onclick="playSweetMeow(); spawnBookParticles(['🐾','😻']);">🐾 Suri & Pamuk schnurren lassen</button>
            </div>
          `
        },
        {
          num: 'Kapitel III',
          title: 'Kintsugi: Gold in jeder Narbe',
          icon: '🏺 💛 ✨',
          particles: ['✨', '💛', '🌟', '💫'],
          html: `
            <p style="color: #cbd5e1; font-size: 1rem; line-height: 1.7;">
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
            <div style="margin-top: 20px; background: rgba(0,0,0,0.3); padding: 15px; border-radius: 10px; text-align: center;">
              <p style="font-size: 0.85rem; color: #a1b0c0; margin-bottom: 8px;">Goldschimmer entfachen:</p>
              <button class="action-btn" style="font-size: 0.9rem; padding: 6px 16px;" onclick="playChime(); spawnBookParticles(['💛','✨','🌟']);">✨ Goldnaht berühren</button>
            </div>
          `
        },
        {
          num: 'Kapitel IV',
          title: 'Das Seelenband: Die Waldkapelle',
          icon: '🕊️ 🕯️ 🙏',
          particles: ['🕊️', '✨', '🤍', '🌿'],
          html: `
            <p style="color: #cbd5e1; font-size: 1rem; line-height: 1.7;">
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
            <div style="margin-top: 20px; background: rgba(0,0,0,0.3); padding: 15px; border-radius: 10px; text-align: center;">
              <p style="font-size: 0.85rem; color: #a1b0c0; margin-bottom: 8px;">Schutzsegen aussenden:</p>
              <button class="action-btn" style="font-size: 0.9rem; padding: 6px 16px;" onclick="playChime(); spawnBookParticles(['🕊️','✨','🙏']);">🕊️ Kanal der Herzen öffnen</button>
            </div>
          `
        },
        {
          num: 'Kapitel V',
          title: 'Der Blueprint unserer Zukunft',
          icon: '🏡 🗝️ ☀️',
          particles: ['🏡', '🗝️', '☀️', '🌸', '💖'],
          html: `
            <p style="color: #cbd5e1; font-size: 1rem; line-height: 1.7;">
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
            <div style="margin-top: 20px; background: rgba(0,0,0,0.3); padding: 15px; border-radius: 10px; text-align: center;">
              <p style="font-size: 0.85rem; color: #a1b0c0; margin-bottom: 8px;">Schlüssel umdrehen:</p>
              <button class="action-btn" style="font-size: 0.9rem; padding: 6px 16px;" onclick="playTada(); spawnBookParticles(['🗝️','🏡','✨']);">🗝️ Tür zur Zukunft aufschließen</button>
            </div>
          `
        },
        {
          num: 'Kapitel VI',
          title: 'Das ewige Versprechen (150 Jahre)',
          icon: '♾️ 💍 ❤️',
          particles: ['❤️', '💖', '💎', '♾️', '👑'],
          html: `
            <p style="color: #cbd5e1; font-size: 1rem; line-height: 1.7;">
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
              <button class="action-btn" style="font-size: 1.1rem; padding: 12px 30px; background: var(--gradient-brand);" onclick="playTada(); spawnBookParticles(['❤️','💖','💎','♾️','✨']);">
                💍 Das Siegel der Ewigkeit bestätigen
              </button>
            </div>
          `
        }
      ];

      let currentBookPage = 0;
      let bookParticleInterval = null;

      function renderBookPage(index) {
        currentBookPage = index;
        const page = bookPages[index];
        const container = $('#book-page-body');
        if (!container) return;

        // Fade out slightly
        container.style.opacity = '0';
        container.style.transform = 'translateY(10px)';

        setTimeout(() => {
          container.innerHTML = `
            <div class="book-page-header">
              <div>
                <span class="book-chapter-num">${page.num}</span>
                <h3 class="book-page-title">${page.title}</h3>
              </div>
              <div style="font-size: 1.8rem; filter: drop-shadow(0 0 8px gold);">${page.icon}</div>
            </div>
            ${page.html}
          `;
          container.style.opacity = '1';
          container.style.transform = 'translateY(0)';
          
          $('#book-page-indicator').innerText = `Seite ${index + 1} von ${bookPages.length}`;
          $('#book-prev-btn').disabled = (index === 0);
          $('#book-next-btn').disabled = (index === bookPages.length - 1);

          // Restart dynamic page particles
          startBookParticles(page.particles);
        }, 150);
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
          if ($('#book-opened')?.style.display !== 'none') {
            spawnBookParticles(icons);
          }
        }, 1800);
      }

      function playNightSparkle() {
        playChime();
        spawnBookParticles(['✨', '⭐', '💫', '🌙', '💖']);
      }

      // Book Open / Close & Navigation Event Listeners
      $('#book-closed')?.addEventListener('click', () => {
        $('#book-closed').style.display = 'none';
        const opened = $('#book-opened');
        opened.style.display = 'block';
        opened.style.animation = 'flyIn 1.2s cubic-bezier(0.16, 1, 0.3, 1) forwards';
        playTada();
        renderBookPage(0);
      });

      $('#book-close-btn')?.addEventListener('click', () => {
        $('#book-opened').style.display = 'none';
        $('#book-closed').style.display = 'block';
        if (bookParticleInterval) clearInterval(bookParticleInterval);
        playPop();
      });

      $('#book-prev-btn')?.addEventListener('click', () => {
        if (currentBookPage > 0) {
          playPop();
          renderBookPage(currentBookPage - 1);
        }
      });

      $('#book-next-btn')?.addEventListener('click', () => {
        if (currentBookPage < bookPages.length - 1) {
          playPop();
          renderBookPage(currentBookPage + 1);
        }
      });
"""

with open('build_new_app.py', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Inject HTML before "Ein Kanal zu unseren Herzen"
if 'theme-storybook' not in code:
    if '<!-- EIN KANAL ZU UNSEREN HERZEN -->' in code:
        code = code.replace('<!-- EIN KANAL ZU UNSEREN HERZEN -->', storybook_html + '\n    <!-- EIN KANAL ZU UNSEREN HERZEN -->')
        print("Injected Storybook HTML before Kapelle!")
    elif '<section class="section theme-kapelle"' in code:
        code = code.replace('<section class="section theme-kapelle"', storybook_html + '\n    <section class="section theme-kapelle"')
        print("Injected Storybook HTML before theme-kapelle section!")

# 2. Inject CSS before </style>
if 'STORYBOOK CSS & AESTHETICS' not in code:
    code = code.replace('</style>', storybook_css + '\n</style>')
    print("Injected Storybook CSS!")

# 3. Inject JS before renderApp();
if 'DAS BUCH UNSERES LEBENS' not in code:
    code = code.replace('renderApp();', storybook_js + '\n      renderApp();')
    print("Injected Storybook JS!")

with open('build_new_app.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("Storybook injection complete!")
