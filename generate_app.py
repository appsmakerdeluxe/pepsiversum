import os
import json
import base64
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

PASSWORD = b"suripamuk2026"

with open("data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Build the decrypted HTML, CSS, and JS components
app_html = f"""
<div id="pepsi-app" class="pepsi-root">
  <!-- AMBIENT AUDIO PLAYER (Web Audio API driven) -->
  <header class="app-header">
    <div class="header-brand">
      <span class="brand-badge">✨ Pepsiversum</span>
      <h1 class="brand-title">Unsere kleine Welt</h1>
      <p class="brand-sub">Für immer Denis & Selly • Über 215.000 Momente • 586 Tage</p>
    </div>
    <div class="header-controls">
      <button id="btn-theme" class="ctrl-btn" title="Theme wechseln">🌗</button>
      <button id="btn-ambient" class="ctrl-btn" title="Sanfte Musik / Schnurren">🎵 Lo-Fi Ambient</button>
      <button id="btn-lock" class="ctrl-btn" title="Sperren">🔒</button>
    </div>
  </header>

  <!-- NAVIGATION TABS -->
  <nav class="hub-nav">
    <div class="nav-scroll">
      <button class="tab-btn active" data-tab="tab-midnight">📻 Midnight FM</button>
      <button class="tab-btn" data-tab="tab-latenight">🌙 02-05 Uhr Whispers</button>
      <button class="tab-btn" data-tab="tab-kintsugi">🏺 Kintsugi: Goldene Nähte</button>
      <button class="tab-btn" data-tab="tab-cats">🐾 Suri & Pamuk Palast</button>
      <button class="tab-btn" data-tab="tab-icecream">🍦 Eislabor & Date-O-Mat</button>
      <button class="tab-btn" data-tab="tab-blueprint">🏡 Blueprint 150 Jahre</button>
      <button class="tab-btn" data-tab="tab-safeharbor">🛟 Safe Harbor SOS</button>
      <button class="tab-btn" data-tab="tab-promises">📖 Schrein der Versprechen</button>
      <button class="tab-btn" data-tab="tab-timeline">⏳ 2024–2074 Zeitreise</button>
      <button class="tab-btn" data-tab="tab-arcade">🕹️ Memory Quiz & Arcade</button>
    </div>
  </nav>

  <!-- MAIN VIEW CONTAINER -->
  <main class="hub-content">
    
    <!-- 1. MIDNIGHT FM & SPOTIFY JUKEBOX -->
    <section id="tab-midnight" class="tab-panel active">
      <div class="panel-header">
        <span class="panel-tag">Hub 1 • Jukebox</span>
        <h2>📻 Pepsi & Denis Midnight FM</h2>
        <p>Alle 167 einzigartigen Songs aus unserem Chat. Klicke auf ein Lied, um es direkt abzuspielen oder die Chat-Erinnerung dazu zu lesen.</p>
        <div class="search-filter-bar">
          <input type="text" id="spotify-search" class="search-input" placeholder="🔍 Song, Künstler oder Zitat suchen...">
          <div class="filter-pills" id="spotify-filters">
            <button class="pill active" data-filter="all">Alle ({len(data['spotify'])})</button>
            <button class="pill" data-filter="Denis">Denis</button>
            <button class="pill" data-filter="Pepsi">Pepsi</button>
            <button class="pill" data-filter="Deep Romance">Romantik</button>
            <button class="pill" data-filter="Late Night Chill">Late Night</button>
          </div>
        </div>
      </div>

      <!-- EMBEDDED PLAYER CONTAINER -->
      <div class="player-container" id="player-box" style="display:none;">
        <div class="player-header">
          <span id="player-title">Aktueller Song</span>
          <button id="player-close" class="small-btn">✕ Schließen</button>
        </div>
        <iframe id="spotify-iframe" style="border-radius:12px" src="" width="100%" height="152" frameBorder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe>
      </div>

      <div class="tracks-grid" id="tracks-grid">
        <!-- Rendered dynamically -->
      </div>
    </section>

    <!-- 2. LATE NIGHT ARCHIVE (00:00 - 05:59) -->
    <section id="tab-latenight" class="tab-panel">
      <div class="panel-header">
        <span class="panel-tag">Hub 2 • Nacht-Archiv</span>
        <h2>🌙 02:00 – 05:00 Uhr Late-Night Whispers</h2>
        <p>Über 5.500 Nachrichten, wenn die Welt schlief. Hier sind unsere echten, ungefilterten Highlights: Romantik, Flirt & Erotik, Deep Talk und Insomnia-Comedy.</p>
        
        <div class="category-tabs">
          <button class="cat-btn active" data-cat="romantic">💖 Tiefste Romantik</button>
          <button class="cat-btn" data-cat="flirty">🔥 Flirt, Kribbeln & Bett</button>
          <button class="cat-btn" data-cat="deeptalk">🌌 3-Uhr-Morgens Seelentröster</button>
          <button class="cat-btn" data-cat="funny">😂 Insomnia-Comedy & Snacks</button>
        </div>
        
        <div class="latenight-actions">
          <input type="text" id="latenight-search" class="search-input" placeholder="🔍 In den Nacht-Nachrichten stöbern...">
          <button id="btn-random-whisper" class="action-btn">✨ Zufälliges Nacht-Geheimnis</button>
        </div>
      </div>

      <div class="chat-bubbles-stream" id="latenight-stream">
        <!-- Rendered dynamically -->
      </div>
    </section>

    <!-- 3. KINTSUGI: AUS SCHERBEN WIRD GOLD -->
    <section id="tab-kintsugi" class="tab-panel">
      <div class="panel-header">
        <span class="panel-tag">Hub 3 • Heilung & Versöhnung</span>
        <h2>🏺 Kintsugi: Aus Scherben wird Gold</h2>
        <p>In Japan repariert man Zerbrochenes mit Gold, weil Narben uns wertvoller und unzertrennlicher machen. Klicke auf die goldenen Bruchstellen unseres Herzens.</p>
      </div>

      <div class="kintsugi-container">
        <div class="kintsugi-visual">
          <div class="golden-heart-interactive" id="kintsugi-heart">
            <div class="gold-seam seam-1" data-idx="0">✨</div>
            <div class="gold-seam seam-2" data-idx="1">✨</div>
            <div class="gold-seam seam-3" data-idx="2">✨</div>
            <div class="gold-seam seam-4" data-idx="3">✨</div>
            <div class="gold-seam seam-5" data-idx="4">✨</div>
          </div>
          <div class="kintsugi-pact-box">
            <button id="btn-seal-peace" class="glow-btn">🤝 Friedens-Schwur erneuern</button>
            <p class="small-hint">Halte geklickt, um die goldenen Adern pulsieren zu lassen</p>
          </div>
        </div>

        <div class="kintsugi-details" id="kintsugi-story-display">
          <div class="story-card active">
            <span class="story-date">07.08.2025 • Ewige Verbundenheit</span>
            <h3 class="story-title">Der Schwur im Herzen</h3>
            <blockquote class="story-quote">„Ich weiß nicht ob das eine Herausforderung ist der wir ausgesetzt sind oder was es ist, aber eines ist sicher: Ich habe deinen Namen in mein Herz geritzt und da bleibt er bis zum Tod.“</blockquote>
            <div class="story-author">— Denis</div>
            <p class="story-lesson">Egal wie viele Stürme oder Zweifel aufziehen – was Denis für Selly empfindet, ist für immer in Stein und Herz gemeißelt. Kein Streit kann das je auflösen.</p>
          </div>
        </div>
      </div>
    </section>

    <!-- 4. SURI & PAMUK PALAST -->
    <section id="tab-cats" class="tab-panel">
      <div class="panel-header">
        <span class="panel-tag">Hub 4 • Unsere Babys</span>
        <h2>🐾 Suri & Pamuk Palast</h2>
        <p>Die beiden wahren Herrscher über unser Leben! Soundboard, Kletterbäume und die legendärsten Katzen-Anekdoten aus dem Chat.</p>
      </div>

      <div class="cats-grid">
        <div class="cat-card suri-card">
          <div class="cat-avatar">🐱</div>
          <h3>Suri</h3>
          <p class="cat-title">Die Bett-Blockiererin & Chefin</p>
          <button class="sound-btn" data-sound="purr">🐾 Schnurren abspielen</button>
          <button class="sound-btn" data-sound="meow">🐾 Süßes Miau</button>
          <div class="cat-fact">Spezialfähigkeit: Legt sich auf Selly, sodass Selly 4 Stunden nicht aufstehen kann.</div>
        </div>

        <div class="cat-card pamuk-card">
          <div class="cat-avatar">🐈</div>
          <h3>Pamuk</h3>
          <p class="cat-title">Der Baum-Kletterer & Chaot</p>
          <button class="sound-btn" data-sound="purr">🐾 Zufriedenes Schnurren</button>
          <button class="sound-btn" data-sound="meow">🐾 Freches Miau</button>
          <div class="cat-fact">Spezialfähigkeit: Rennt 10 Minuten nach dem Wischen durch nassen Dreck.</div>
        </div>
      </div>

      <div class="cat-stories-section">
        <h3>📖 Die Akten von Suri & Pamuk</h3>
        <div class="cat-stories-list" id="cat-stories-list">
          <!-- Rendered dynamically -->
        </div>
      </div>
    </section>

    <!-- 5. DAS EISLABOR & DATE-ROULETTE -->
    <section id="tab-icecream" class="tab-panel">
      <div class="panel-header">
        <span class="panel-tag">Hub 5 • Genuss & Dates</span>
        <h2>🍦 Das Große Eislabor & Date-O-Mat</h2>
        <p>Über 2.460 Mal Eis im Chat! Staple dein persönliches Traum-Eis mit Liebesbotschaften oder lass das Date-Roulette entscheiden.</p>
      </div>

      <div class="ice-workspace">
        <div class="ice-builder">
          <h3>Kugel-Stapler (Klicke auf Sorten)</h3>
          <div class="flavor-palette" id="flavor-palette">
            <!-- Rendered dynamically -->
          </div>
          <div class="cone-stage">
            <div class="scoop-stack" id="scoop-stack">
              <!-- Scoops injected here -->
            </div>
            <div class="ice-waffle">🧇</div>
          </div>
          <button id="btn-reset-ice" class="small-btn">Eis aufessen & neu bauen 😋</button>
        </div>

        <div class="date-roulette-box">
          <h3>🎲 Date-O-Mat: Was machen wir heute?</h3>
          <p>Keine Ideen für das nächste Treffen? Dreh das Rad!</p>
          <div class="roulette-display" id="roulette-card">
            <span class="roulette-tag">Bereit?</span>
            <h4 id="roulette-title">Klicke auf Drehen!</h4>
            <p id="roulette-desc">Lass das Schicksal unser nächstes Abenteuer bestimmen.</p>
          </div>
          <button id="btn-spin-roulette" class="action-btn-large">🎡 Rad drehen!</button>
        </div>
      </div>
    </section>

    <!-- 6. BLUEPRINT 150 JAHRE -->
    <section id="tab-blueprint" class="tab-panel">
      <div class="panel-header">
        <span class="panel-tag">Hub 6 • Unser Reich</span>
        <h2>🏡 Blueprint: Unser 150-Jahre-Zuhause</h2>
        <p>„Heirate mich und du wirst 150 Jahre alt werden“ (Selly) • „Wenn wir zusammenziehen, haben wir alles doppelt!“ (Denis). Erkunde unsere Räume.</p>
      </div>

      <div class="rooms-nav" id="rooms-nav">
        <!-- Rendered dynamically -->
      </div>

      <div class="room-details-card" id="room-details-card">
        <!-- Rendered dynamically -->
      </div>
    </section>

    <!-- 7. SAFE HARBOR SOS -->
    <section id="tab-safeharbor" class="tab-panel">
      <div class="panel-header">
        <span class="panel-tag">Hub 7 • Digitaler Schutzraum</span>
        <h2>🛟 Safe Harbor & SOS-Trost-Kit</h2>
        <p>Für Tage, an denen einer von uns gestresst, traurig, sauer ist oder den anderen unendlich vermisst. Wähle deinen Zustand:</p>
      </div>

      <div class="sos-buttons-grid">
        <button class="sos-card" data-sos="stress">
          <span class="sos-icon">🍃</span>
          <span class="sos-title">Ich bin gestresst von Arbeit & Welt</span>
        </button>
        <button class="sos-card" data-sos="mad">
          <span class="sos-icon">❤️‍🩹</span>
          <span class="sos-title">Ich bin sauer oder enttäuscht</span>
        </button>
        <button class="sos-card" data-sos="miss">
          <span class="sos-icon">🌌</span>
          <span class="sos-title">Ich vermisse dich gerade unendlich</span>
        </button>
        <button class="sos-card" data-sos="hug">
          <span class="sos-icon">💖</span>
          <span class="sos-title">Ich brauche Liebe & Geborgenheit</span>
        </button>
      </div>

      <div class="sos-modal-content" id="sos-modal-content" style="display:none;">
        <div class="sos-box">
          <div class="breathing-circle" id="breath-circle">Atme ein...</div>
          <h3 id="sos-advice-title">Titel</h3>
          <blockquote id="sos-advice-quote">Zitat</blockquote>
          <div id="sos-bonus-badge" class="bonus-badge">Gutschein</div>
          <button id="sos-close" class="action-btn">Danke, mir geht's schon besser ❤️</button>
        </div>
      </div>
    </section>

    <!-- 8. PROMISE VAULT -->
    <section id="tab-promises" class="tab-panel">
      <div class="panel-header">
        <span class="panel-tag">Hub 8 • Schrein der Gelübde</span>
        <h2>📖 Der Schrein der ewigen Versprechen</h2>
        <p>Klicke auf die Siegel, um unsere unzerbrechlichen Gelübde aus dem Chat zu öffnen.</p>
      </div>

      <div class="promises-grid" id="promises-grid">
        <!-- Rendered dynamically -->
      </div>
    </section>

    <!-- 9. TIMELINE 2024-2074 -->
    <section id="tab-timeline" class="tab-panel">
      <div class="panel-header">
        <span class="panel-tag">Hub 9 • Unsere Zeitreise</span>
        <h2>⏳ 2024 ➔ 2074: Unsere gemeinsame Roadmap</h2>
        <p>Von der allerersten Nachricht bis zum 80. Lebensjahr auf der Parkbank.</p>
      </div>

      <div class="timeline-tree" id="timeline-tree">
        <!-- Rendered dynamically -->
      </div>

      <div class="timecapsule-section">
        <h3>💌 Verschlüsseltes Zukunfts-Tagebuch</h3>
        <p>Schreibe einen geheimen Wunsch für unsere Zukunft. Er wird sicher in deinem Browser gespeichert.</p>
        <textarea id="capsule-input" class="capsule-text" rows="3" placeholder="Unser nächster großer Traum..."></textarea>
        <button id="btn-save-capsule" class="glow-btn">✨ In Zeitkapsel versiegeln</button>
        <div id="capsule-list" class="capsule-entries"></div>
      </div>
    </section>

    <!-- 10. ARCADE & QUIZ -->
    <section id="tab-arcade" class="tab-panel">
      <div class="panel-header">
        <span class="panel-tag">Hub 10 • Challenge</span>
        <h2>🕹️ Pepsi & Denis Memory Quiz</h2>
        <p>10 Fragen aus über 215.000 Nachrichten! Wie gut kennst du unsere Geschichte?</p>
      </div>

      <div class="quiz-container" id="quiz-container">
        <div class="quiz-progress-bar"><div class="quiz-fill" id="quiz-fill"></div></div>
        <div class="quiz-question-card">
          <span class="quiz-step" id="quiz-step">Frage 1 von 10</span>
          <h3 class="quiz-q-text" id="quiz-q-text">Fragetext lädt...</h3>
          <div class="quiz-options" id="quiz-options"></div>
          <div class="quiz-feedback" id="quiz-feedback" style="display:none;"></div>
        </div>
      </div>

      <div class="quiz-finished-card" id="quiz-finished" style="display:none;">
        <h3>🎉 Glückwunsch, mein Engel!</h3>
        <p id="quiz-score-text">Du hast 10 von 10 Fragen richtig!</p>
        <div class="secret-love-letter">
          <h4>💌 Denis' geheimer Brief an Selly:</h4>
          <p>„Danke, dass du mein Leben bereicherst, mich zum Lachen bringst, mit mir bis 4 Uhr morgens wachbleibst und meine beste Freundin und größte Liebe in einem bist. Auf die nächsten 150 Jahre!“</p>
        </div>
        <button id="btn-restart-quiz" class="action-btn">Quiz noch einmal spielen</button>
      </div>
    </section>

  </main>
</div>
"""

# Full styles
app_css = """
:root {
  --bg-main: #0a0e17;
  --bg-card: rgba(20, 27, 45, 0.75);
  --bg-card-hover: rgba(30, 40, 65, 0.85);
  --border-color: rgba(255, 255, 255, 0.12);
  --primary-gold: #e5b869;
  --primary-rose: #ff4d6d;
  --primary-mint: #0ecbb5;
  --primary-purple: #9d4edd;
  --text-main: #f0f4f8;
  --text-muted: #94a3b8;
  --bubble-denis: #1d3557;
  --bubble-pepsi: #4a1c40;
  --glow-gold: 0 0 25px rgba(229, 184, 105, 0.4);
  --radius-lg: 20px;
  --radius-md: 14px;
  --radius-sm: 8px;
}

[data-theme="light"] {
  --bg-main: #f8fafc;
  --bg-card: rgba(255, 255, 255, 0.85);
  --bg-card-hover: rgba(241, 245, 249, 0.95);
  --border-color: rgba(0, 0, 0, 0.08);
  --text-main: #0f172a;
  --text-muted: #64748b;
  --bubble-denis: #dbeafe;
  --bubble-pepsi: #fce7f3;
  --glow-gold: 0 0 20px rgba(229, 184, 105, 0.25);
}

.pepsi-root {
  min-height: 100vh;
  background: var(--bg-main);
  color: var(--text-main);
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  padding-bottom: 60px;
  line-height: 1.5;
}

.app-header {
  padding: 30px 24px 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 16px;
  max-width: 1300px;
  margin: 0 auto;
  border-bottom: 1px solid var(--border-color);
}

.brand-badge {
  font-size: 0.8rem;
  text-transform: uppercase;
  letter-spacing: 2px;
  color: var(--primary-gold);
  font-weight: 700;
}

.brand-title {
  margin: 4px 0;
  font-size: 2rem;
  font-weight: 800;
  background: linear-gradient(135deg, var(--primary-gold), var(--primary-rose));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.brand-sub {
  margin: 0;
  font-size: 0.9rem;
  color: var(--text-muted);
}

.header-controls {
  display: flex;
  gap: 10px;
}

.ctrl-btn {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  color: var(--text-main);
  padding: 8px 14px;
  border-radius: var(--radius-md);
  cursor: pointer;
  font-weight: 600;
  font-size: 0.9rem;
  transition: all 0.2s ease;
  backdrop-filter: blur(10px);
}

.ctrl-btn:hover {
  background: var(--bg-card-hover);
  border-color: var(--primary-gold);
  transform: translateY(-2px);
}

/* HUB NAVIGATION */
.hub-nav {
  position: sticky;
  top: 0;
  z-index: 100;
  background: rgba(10, 14, 23, 0.85);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid var(--border-color);
  padding: 12px 16px;
}

[data-theme="light"] .hub-nav {
  background: rgba(248, 250, 252, 0.85);
}

.nav-scroll {
  display: flex;
  gap: 10px;
  overflow-x: auto;
  max-width: 1300px;
  margin: 0 auto;
  padding-bottom: 4px;
  scrollbar-width: thin;
}

.tab-btn {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  color: var(--text-muted);
  padding: 8px 16px;
  border-radius: 30px;
  cursor: pointer;
  white-space: nowrap;
  font-size: 0.9rem;
  font-weight: 600;
  transition: all 0.2s ease;
}

.tab-btn.active, .tab-btn:hover {
  background: linear-gradient(135deg, var(--primary-gold), var(--primary-rose));
  color: #000;
  border-color: transparent;
  box-shadow: 0 4px 15px rgba(229, 184, 105, 0.3);
}

/* CONTENT PANELS */
.hub-content {
  max-width: 1300px;
  margin: 24px auto;
  padding: 0 16px;
}

.tab-panel {
  display: none;
  animation: fadeIn 0.3s ease;
}

.tab-panel.active {
  display: block;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(8px); }
  to { opacity: 1; transform: translateY(0); }
}

.panel-header {
  margin-bottom: 24px;
}

.panel-tag {
  font-size: 0.75rem;
  font-weight: 700;
  color: var(--primary-mint);
  text-transform: uppercase;
  letter-spacing: 1px;
}

.panel-header h2 {
  margin: 4px 0 8px;
  font-size: 1.8rem;
  font-weight: 800;
}

.panel-header p {
  color: var(--text-muted);
  margin: 0 0 16px;
  font-size: 0.95rem;
}

/* SEARCH & FILTERS */
.search-filter-bar, .latenight-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  align-items: center;
  margin-top: 12px;
}

.search-input {
  flex: 1;
  min-width: 260px;
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  color: var(--text-main);
  padding: 10px 16px;
  border-radius: var(--radius-md);
  font-size: 0.95rem;
  outline: none;
}

.search-input:focus {
  border-color: var(--primary-gold);
}

.filter-pills, .category-tabs {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.pill, .cat-btn {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  color: var(--text-muted);
  padding: 6px 14px;
  border-radius: 20px;
  cursor: pointer;
  font-size: 0.85rem;
  font-weight: 600;
  transition: all 0.2s ease;
}

.pill.active, .cat-btn.active {
  background: var(--primary-gold);
  color: #000;
  border-color: var(--primary-gold);
}

/* SPOTIFY TRACKS GRID */
.tracks-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 16px;
  margin-top: 20px;
}

.track-card {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  padding: 16px;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.track-card:hover {
  background: var(--bg-card-hover);
  border-color: var(--primary-gold);
  transform: translateY(-3px);
  box-shadow: var(--glow-gold);
}

.track-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.8rem;
  color: var(--text-muted);
  margin-bottom: 8px;
}

.track-sender {
  font-weight: 700;
  color: var(--primary-mint);
}

.track-quote {
  font-size: 0.9rem;
  font-style: italic;
  margin: 8px 0;
  color: var(--text-main);
}

.track-btn {
  background: #1db954;
  color: #000;
  font-weight: 700;
  border: none;
  padding: 8px 12px;
  border-radius: var(--radius-sm);
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 0.85rem;
  align-self: flex-start;
  margin-top: 8px;
}

/* LATE NIGHT BUBBLES */
.chat-bubbles-stream {
  display: flex;
  flex-direction: column;
  gap: 16px;
  max-width: 800px;
  margin: 20px auto;
}

.chat-bubble-card {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-lg);
  padding: 18px 22px;
  position: relative;
  transition: transform 0.2s ease;
}

.chat-bubble-card:hover {
  transform: scale(1.01);
}

.chat-bubble-card.denis {
  border-left: 4px solid #3a86ff;
  align-self: flex-start;
  width: 90%;
}

.chat-bubble-card.pepsi {
  border-left: 4px solid var(--primary-rose);
  align-self: flex-end;
  width: 90%;
}

.bubble-meta {
  display: flex;
  justify-content: space-between;
  font-size: 0.8rem;
  color: var(--text-muted);
  margin-bottom: 8px;
}

.bubble-text {
  font-size: 1rem;
  white-space: pre-wrap;
}

/* KINTSUGI SECTION */
.kintsugi-container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 30px;
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-lg);
  padding: 30px;
  align-items: center;
}

@media (max-width: 800px) {
  .kintsugi-container { grid-template-columns: 1fr; }
}

.golden-heart-interactive {
  width: 240px;
  height: 240px;
  margin: 0 auto;
  position: relative;
  background: radial-gradient(circle, #ff4d6d, #b5179e);
  clip-path: path("M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z");
  transform: scale(10);
  transform-origin: 12px 12px;
  cursor: pointer;
  transition: transform 0.3s ease;
}

.gold-seam {
  position: absolute;
  font-size: 2px;
  color: #ffd700;
  cursor: pointer;
  animation: pulseGold 2s infinite;
}

.seam-1 { top: 6px; left: 8px; }
.seam-2 { top: 12px; left: 14px; }
.seam-3 { top: 16px; left: 10px; }
.seam-4 { top: 8px; left: 16px; }
.seam-5 { top: 14px; left: 6px; }

@keyframes pulseGold {
  0%, 100% { filter: drop-shadow(0 0 1px #ffd700); transform: scale(1); }
  50% { filter: drop-shadow(0 0 4px #ffd700); transform: scale(1.3); }
}

.story-card {
  background: rgba(0, 0, 0, 0.2);
  border: 1px solid var(--primary-gold);
  border-radius: var(--radius-md);
  padding: 24px;
}

.story-date {
  font-size: 0.8rem;
  color: var(--primary-gold);
  font-weight: 700;
}

.story-quote {
  font-size: 1.1rem;
  font-style: italic;
  margin: 16px 0;
  color: var(--text-main);
  border-left: 3px solid var(--primary-gold);
  padding-left: 14px;
}

.story-lesson {
  font-size: 0.95rem;
  color: var(--text-muted);
}

/* CATS SECTION */
.cats-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-bottom: 24px;
}

@media (max-width: 650px) {
  .cats-grid { grid-template-columns: 1fr; }
}

.cat-card {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-lg);
  padding: 24px;
  text-align: center;
}

.cat-avatar {
  font-size: 3.5rem;
  margin-bottom: 10px;
}

.sound-btn {
  background: var(--bg-card-hover);
  border: 1px solid var(--border-color);
  color: var(--text-main);
  padding: 8px 16px;
  border-radius: 20px;
  margin: 6px 4px;
  cursor: pointer;
  font-size: 0.85rem;
  font-weight: 600;
}

.sound-btn:hover {
  background: var(--primary-mint);
  color: #000;
}

.cat-fact {
  margin-top: 14px;
  font-size: 0.85rem;
  color: var(--text-muted);
  font-style: italic;
}

/* EISLABOR */
.ice-workspace {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
}

@media (max-width: 800px) {
  .ice-workspace { grid-template-columns: 1fr; }
}

.flavor-palette {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 16px;
}

.flavor-btn {
  border: none;
  color: #fff;
  padding: 8px 14px;
  border-radius: 20px;
  font-weight: 700;
  cursor: pointer;
  font-size: 0.85rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.2);
}

.cone-stage {
  min-height: 200px;
  display: flex;
  flex-direction: column-reverse;
  align-items: center;
  margin: 20px 0;
}

.ice-waffle {
  font-size: 3rem;
}

.ice-scoop {
  width: 90px;
  height: 60px;
  border-radius: 50% 50% 30% 30%;
  margin-bottom: -15px;
  box-shadow: inset 0 -6px 12px rgba(0,0,0,0.3);
  animation: dropScoop 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

@keyframes dropScoop {
  from { transform: translateY(-40px) scale(0.6); opacity: 0; }
  to { transform: translateY(0) scale(1); opacity: 1; }
}

.date-roulette-box {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-lg);
  padding: 24px;
  text-align: center;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.roulette-display {
  background: rgba(0,0,0,0.2);
  border: 1px dashed var(--primary-gold);
  border-radius: var(--radius-md);
  padding: 20px;
  margin: 20px 0;
}

.action-btn-large, .glow-btn {
  background: linear-gradient(135deg, var(--primary-gold), var(--primary-rose));
  color: #000;
  font-weight: 800;
  font-size: 1.1rem;
  padding: 14px 28px;
  border: none;
  border-radius: 30px;
  cursor: pointer;
  box-shadow: 0 4px 20px rgba(229, 184, 105, 0.4);
  transition: transform 0.2s ease;
}

.action-btn-large:hover, .glow-btn:hover {
  transform: scale(1.04);
}

/* QUIZ */
.quiz-container {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-lg);
  padding: 30px;
  max-width: 700px;
  margin: 0 auto;
}

.quiz-progress-bar {
  height: 8px;
  background: rgba(255,255,255,0.1);
  border-radius: 4px;
  margin-bottom: 20px;
  overflow: hidden;
}

.quiz-fill {
  height: 100%;
  width: 10%;
  background: linear-gradient(90deg, var(--primary-gold), var(--primary-mint));
  transition: width 0.3s ease;
}

.quiz-options {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin: 20px 0;
}

.quiz-opt-btn {
  background: var(--bg-card-hover);
  border: 1px solid var(--border-color);
  color: var(--text-main);
  padding: 14px 20px;
  border-radius: var(--radius-md);
  font-size: 1rem;
  font-weight: 600;
  text-align: left;
  cursor: pointer;
  transition: all 0.2s ease;
}

.quiz-opt-btn:hover {
  border-color: var(--primary-gold);
  background: rgba(229, 184, 105, 0.1);
}

.quiz-opt-btn.correct {
  background: rgba(14, 203, 181, 0.3);
  border-color: var(--primary-mint);
}

.quiz-opt-btn.wrong {
  background: rgba(255, 77, 109, 0.3);
  border-color: var(--primary-rose);
}

/* SOS MODAL */
.sos-buttons-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 16px;
  margin-top: 20px;
}

.sos-card {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-lg);
  padding: 24px;
  text-align: center;
  cursor: pointer;
  transition: all 0.2s ease;
}

.sos-card:hover {
  border-color: var(--primary-mint);
  transform: translateY(-4px);
}

.sos-icon {
  font-size: 2.5rem;
  display: block;
  margin-bottom: 10px;
}

.breathing-circle {
  width: 140px;
  height: 140px;
  border-radius: 50%;
  background: radial-gradient(circle, var(--primary-mint), var(--primary-purple));
  margin: 20px auto;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  color: #fff;
  animation: breathe 8s infinite ease-in-out;
}

@keyframes breathe {
  0%, 100% { transform: scale(0.8); opacity: 0.6; }
  50% { transform: scale(1.3); opacity: 1; }
}

.bonus-badge {
  background: var(--primary-gold);
  color: #000;
  font-weight: 800;
  padding: 10px 18px;
  border-radius: 20px;
  display: inline-block;
  margin: 16px 0;
}
"""

# App interactive JS
app_js = """
(function() {
  const DATA = window.__PEPSI_DATA__;
  if (!DATA) return;

  // 1. TABS SWITCHING
  const tabs = document.querySelectorAll('.tab-btn');
  const panels = document.querySelectorAll('.tab-panel');
  tabs.forEach(btn => {
    btn.addEventListener('click', () => {
      tabs.forEach(t => t.classList.remove('active'));
      panels.forEach(p => p.classList.remove('active'));
      btn.classList.add('active');
      const target = document.getElementById(btn.dataset.tab);
      if (target) target.classList.add('active');
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  });

  // 2. THEME SWITCHING
  const themeBtn = document.getElementById('btn-theme');
  let isDark = true;
  themeBtn.addEventListener('click', () => {
    isDark = !isDark;
    document.documentElement.setAttribute('data-theme', isDark ? 'dark' : 'light');
  });

  // 3. LO-FI / AMBIENT AUDIO SYNTHESIZER (Web Audio API)
  let audioCtx = null;
  let isPlayingAudio = false;
  const ambientBtn = document.getElementById('btn-ambient');
  
  function toggleAmbient() {
    if (!audioCtx) {
      audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    }
    if (isPlayingAudio) {
      audioCtx.suspend();
      isPlayingAudio = false;
      ambientBtn.textContent = '🎵 Lo-Fi Ambient';
    } else {
      audioCtx.resume();
      playChords();
      isPlayingAudio = true;
      ambientBtn.textContent = '⏸ Pause Ambient';
    }
  }
  ambientBtn.addEventListener('click', toggleAmbient);

  function playChords() {
    if (!audioCtx) return;
    const osc = audioCtx.createOscillator();
    const gain = audioCtx.createGain();
    osc.type = 'sine';
    osc.frequency.setValueAtTime(220, audioCtx.currentTime); // A3
    gain.gain.setValueAtTime(0.05, audioCtx.currentTime);
    osc.connect(gain);
    gain.connect(audioCtx.destination);
    osc.start();
  }

  // 4. SPOTIFY JUKEBOX RENDERING & SEARCH
  const tracksGrid = document.getElementById('tracks-grid');
  const spotifySearch = document.getElementById('spotify-search');
  const spotifyFilters = document.querySelectorAll('#spotify-filters .pill');
  const playerBox = document.getElementById('player-box');
  const spotifyIframe = document.getElementById('spotify-iframe');
  const playerTitle = document.getElementById('player-title');
  const playerClose = document.getElementById('player-close');

  playerClose.addEventListener('click', () => { playerBox.style.display = 'none'; });

  function renderTracks(query = '', filter = 'all') {
    tracksGrid.innerHTML = '';
    const q = query.toLowerCase();
    const filtered = DATA.spotify.filter(t => {
      const matchQ = !q || t.msg.toLowerCase().includes(q) || t.sender.toLowerCase().includes(q) || t.mood.toLowerCase().includes(q);
      const matchF = filter === 'all' || t.sender === filter || t.mood === filter;
      return matchQ && matchF;
    });

    filtered.forEach(t => {
      const card = document.createElement('div');
      card.className = 'track-card';
      card.innerHTML = `
        <div>
          <div class="track-top">
            <span class="track-sender">${t.sender}</span>
            <span>${t.date} • ${t.time}</span>
          </div>
          <div class="track-quote">„${t.msg}“</div>
          <div style="font-size:0.75rem; color:var(--primary-gold); font-weight:700;">${t.mood}</div>
        </div>
        <button class="track-btn">▶ In Spotify öffnen</button>
      `;
      card.addEventListener('click', () => {
        playerBox.style.display = 'block';
        playerTitle.textContent = `${t.sender} (${t.date}): ${t.msg}`;
        spotifyIframe.src = t.embedUrl;
        playerBox.scrollIntoView({ behavior: 'smooth' });
      });
      tracksGrid.appendChild(card);
    });
  }
  renderTracks();

  spotifySearch.addEventListener('input', (e) => {
    const activeFilter = document.querySelector('#spotify-filters .pill.active').dataset.filter;
    renderTracks(e.target.value, activeFilter);
  });

  spotifyFilters.forEach(pill => {
    pill.addEventListener('click', () => {
      spotifyFilters.forEach(p => p.classList.remove('active'));
      pill.classList.add('active');
      renderTracks(spotifySearch.value, pill.dataset.filter);
    });
  });

  // 5. LATE NIGHT ARCHIVE
  const latenightStream = document.getElementById('latenight-stream');
  const catBtns = document.querySelectorAll('.cat-btn');
  const latenightSearch = document.getElementById('latenight-search');
  const randomWhisperBtn = document.getElementById('btn-random-whisper');

  let currentCat = 'romantic';
  function renderLateNight(cat = 'romantic', query = '') {
    latenightStream.innerHTML = '';
    const q = query.toLowerCase();
    const list = DATA.lateNight[cat] || [];
    const filtered = list.filter(m => !q || m.text.toLowerCase().includes(q) || m.sender.toLowerCase().includes(q));

    filtered.forEach(m => {
      const isDenis = m.sender.toLowerCase().includes('denis');
      const b = document.createElement('div');
      b.className = `chat-bubble-card ${isDenis ? 'denis' : 'pepsi'}`;
      b.innerHTML = `
        <div class="bubble-meta">
          <strong>${m.sender}</strong>
          <span>${m.date} • ${m.time} Uhr</span>
        </div>
        <div class="bubble-text">${m.text}</div>
      `;
      latenightStream.appendChild(b);
    });
  }
  renderLateNight('romantic');

  catBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      catBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      currentCat = btn.dataset.cat;
      renderLateNight(currentCat, latenightSearch.value);
    });
  });

  latenightSearch.addEventListener('input', (e) => {
    renderLateNight(currentCat, e.target.value);
  });

  randomWhisperBtn.addEventListener('click', () => {
    const allMsgs = [...DATA.lateNight.romantic, ...DATA.lateNight.flirty, ...DATA.lateNight.deeptalk, ...DATA.lateNight.funny];
    const rand = allMsgs[Math.floor(Math.random() * allMsgs.length)];
    alert(`🌙 Zufälliges Nacht-Geheimnis (${rand.date} um ${rand.time} von ${rand.sender}):\n\n„${rand.text}“`);
  });

  // 6. KINTSUGI HEART
  const kintsugiSeams = document.querySelectorAll('.gold-seam');
  const storyDisplay = document.getElementById('kintsugi-story-display');
  kintsugiSeams.forEach(s => {
    s.addEventListener('click', () => {
      const idx = parseInt(s.dataset.idx);
      const story = DATA.kintsugi[idx];
      if (!story) return;
      storyDisplay.innerHTML = `
        <div class="story-card active">
          <span class="story-date">${story.date} • ${story.category}</span>
          <h3 class="story-title">${story.title}</h3>
          <blockquote class="story-quote">${story.quote}</blockquote>
          <div class="story-author">— ${story.author}</div>
          <p class="story-lesson">${story.lesson}</p>
        </div>
      `;
    });
  });

  document.getElementById('btn-seal-peace').addEventListener('click', () => {
    alert('✨ Friedens-Schwur besiegelt: Unsere Liebe heilt jeden Riss und macht uns unbesiegbar!');
  });

  // 7. SURI & PAMUK SOUNDS & STORIES
  const catStoriesList = document.getElementById('cat-stories-list');
  DATA.catsData.forEach(c => {
    const item = document.createElement('div');
    item.className = 'chat-bubble-card';
    item.style.marginBottom = '12px';
    item.innerHTML = `
      <div class="bubble-meta">
        <strong>${c.title}</strong>
        <span>${c.date}</span>
      </div>
      <p style="margin:0">${c.text}</p>
    `;
    catStoriesList.appendChild(item);
  });

  document.querySelectorAll('.sound-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const sound = btn.dataset.sound;
      alert(`🐾 *${sound === 'purr' ? 'Suri & Pamuk schnurren friedlich... *purrrrrr*' : 'Miau! Leckerli her, sonst wird weiter Dreck gemacht!'}*`);
    });
  });

  // 8. EISLABOR & DATE-ROULETTE
  const flavorPalette = document.getElementById('flavor-palette');
  const scoopStack = document.getElementById('scoop-stack');
  const resetIceBtn = document.getElementById('btn-reset-ice');
  
  DATA.iceCreamLab.flavors.forEach(f => {
    const btn = document.createElement('button');
    btn.className = 'flavor-btn';
    btn.style.backgroundColor = f.color;
    btn.textContent = `+ ${f.name}`;
    btn.addEventListener('click', () => {
      if (scoopStack.children.length >= 8) {
        alert('🍦 Dein Eisbecher ist schon riesig! Zeit zum Genießen!');
        return;
      }
      const scoop = document.createElement('div');
      scoop.className = 'ice-scoop';
      scoop.style.backgroundColor = f.color;
      scoop.title = f.note;
      scoopStack.appendChild(scoop);
    });
    flavorPalette.appendChild(btn);
  });

  resetIceBtn.addEventListener('click', () => { scoopStack.innerHTML = ''; });

  const rouletteTitle = document.getElementById('roulette-title');
  const rouletteDesc = document.getElementById('roulette-desc');
  const spinBtn = document.getElementById('btn-spin-roulette');
  spinBtn.addEventListener('click', () => {
    const dates = DATA.iceCreamLab.dates;
    const picked = dates[Math.floor(Math.random() * dates.length)];
    rouletteTitle.textContent = picked.title;
    rouletteDesc.textContent = picked.desc;
  });

  // 9. BLUEPRINT ROOMS
  const roomsNav = document.getElementById('rooms-nav');
  const roomCard = document.getElementById('room-details-card');

  function renderRoom(room) {
    roomCard.innerHTML = `
      <div style="background:var(--bg-card); border:1px solid var(--border-color); border-radius:var(--radius-lg); padding:24px; margin-top:16px;">
        <h3>${room.icon} ${room.name}</h3>
        <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(240px, 1fr)); gap:16px; margin-top:16px;">
          ${room.items.map(it => `
            <div style="background:var(--bg-card-hover); padding:16px; border-radius:var(--radius-md); border:1px solid var(--border-color);">
              <h4 style="margin:0 0 6px; color:var(--primary-gold)">${it.name}</h4>
              <p style="margin:0 0 8px; font-size:0.9rem">${it.desc}</p>
              <div style="font-size:0.8rem; color:var(--primary-mint); font-style:italic">„${it.quote}“</div>
            </div>
          `).join('')}
        </div>
      </div>
    `;
  }

  DATA.blueprint.forEach((r, idx) => {
    const btn = document.createElement('button');
    btn.className = `tab-btn ${idx === 0 ? 'active' : ''}`;
    btn.textContent = `${r.icon} ${r.name}`;
    btn.addEventListener('click', () => {
      document.querySelectorAll('#rooms-nav .tab-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      renderRoom(r);
    });
    roomsNav.appendChild(btn);
  });
  if (DATA.blueprint.length > 0) renderRoom(DATA.blueprint[0]);

  // 10. SAFE HARBOR SOS
  const sosModal = document.getElementById('sos-modal-content');
  const sosTitle = document.getElementById('sos-advice-title');
  const sosQuote = document.getElementById('sos-advice-quote');
  const sosBonus = document.getElementById('sos-bonus-badge');
  const sosClose = document.getElementById('sos-close');

  document.querySelectorAll('.sos-card').forEach(c => {
    c.addEventListener('click', () => {
      const type = c.dataset.sos;
      const entry = DATA.safeHarbor.find(s => s.id === type);
      if (entry) {
        sosTitle.textContent = entry.title;
        sosQuote.textContent = entry.quote;
        sosBonus.textContent = entry.bonus;
        sosModal.style.display = 'block';
        sosModal.scrollIntoView({ behavior: 'smooth' });
      }
    });
  });
  sosClose.addEventListener('click', () => { sosModal.style.display = 'none'; });

  // 11. PROMISES GRID
  const promisesGrid = document.getElementById('promises-grid');
  DATA.promises.forEach(p => {
    const card = document.createElement('div');
    card.className = 'chat-bubble-card';
    card.innerHTML = `
      <div class="bubble-meta">
        <span style="font-size:1.5rem">${p.seal}</span>
        <span>${p.date} • <strong>${p.status}</strong></span>
      </div>
      <h3 style="margin:4px 0 8px; color:var(--primary-gold)">${p.title}</h3>
      <p style="font-size:1rem; margin:0">${p.text}</p>
    `;
    promisesGrid.appendChild(card);
  });

  // 12. TIMELINE ROADMAP
  const timelineTree = document.getElementById('timeline-tree');
  DATA.timeline.forEach(m => {
    const el = document.createElement('div');
    el.className = 'chat-bubble-card';
    el.style.marginBottom = '16px';
    el.innerHTML = `
      <div class="bubble-meta">
        <strong style="color:var(--primary-gold); font-size:1.1rem">${m.year}</strong>
        <span>Meilenstein</span>
      </div>
      <h4 style="margin:4px 0">${m.title}</h4>
      <p style="margin:0; color:var(--text-muted)">${m.desc}</p>
    `;
    timelineTree.appendChild(el);
  });

  // Local storage timecapsule
  const capsuleInput = document.getElementById('capsule-input');
  const saveCapsuleBtn = document.getElementById('btn-save-capsule');
  const capsuleList = document.getElementById('capsule-list');

  function loadCapsules() {
    capsuleList.innerHTML = '';
    const stored = JSON.parse(localStorage.getItem('pepsi_capsules') || '[]');
    stored.forEach(text => {
      const d = document.createElement('div');
      d.className = 'chat-bubble-card';
      d.style.marginTop = '8px';
      d.textContent = `✨ ${text}`;
      capsuleList.appendChild(d);
    });
  }
  loadCapsules();

  saveCapsuleBtn.addEventListener('click', () => {
    const text = capsuleInput.value.trim();
    if (!text) return;
    const stored = JSON.parse(localStorage.getItem('pepsi_capsules') || '[]');
    stored.push(text);
    localStorage.setItem('pepsi_capsules', JSON.stringify(stored));
    capsuleInput.value = '';
    loadCapsules();
    alert('💌 Wunsch sicher in der Zeitkapsel versiegelt!');
  });

  // 13. TRIVIA QUIZ
  const quiz = DATA.quiz;
  let qIdx = 0;
  let qScore = 0;

  const quizStep = document.getElementById('quiz-step');
  const quizQText = document.getElementById('quiz-q-text');
  const quizOptions = document.getElementById('quiz-options');
  const quizFeedback = document.getElementById('quiz-feedback');
  const quizFill = document.getElementById('quiz-fill');
  const quizFinished = document.getElementById('quiz-finished');
  const quizContainer = document.getElementById('quiz-container');
  const quizScoreText = document.getElementById('quiz-score-text');

  function renderQuestion() {
    const q = quiz[qIdx];
    quizStep.textContent = `Frage ${qIdx + 1} von ${quiz.length}`;
    quizQText.textContent = q.q;
    quizFill.style.width = `${((qIdx + 1) / quiz.length) * 100}%`;
    quizFeedback.style.display = 'none';
    quizOptions.innerHTML = '';

    q.options.forEach((opt, idx) => {
      const btn = document.createElement('button');
      btn.className = 'quiz-opt-btn';
      btn.textContent = opt;
      btn.addEventListener('click', () => {
        const isCorrect = idx === q.answer;
        if (isCorrect) qScore++;
        
        btn.classList.add(isCorrect ? 'correct' : 'wrong');
        quizFeedback.style.display = 'block';
        quizFeedback.innerHTML = `<strong>${isCorrect ? 'Richtig! 🎉' : 'Nicht ganz! 😜'}</strong> ${q.explanation}`;
        
        setTimeout(() => {
          qIdx++;
          if (qIdx < quiz.length) {
            renderQuestion();
          } else {
            quizContainer.style.display = 'none';
            quizFinished.style.display = 'block';
            quizScoreText.textContent = `Du hast ${qScore} von ${quiz.length} Fragen richtig beantwortet! ❤️`;
          }
        }, 2200);
      });
      quizOptions.appendChild(btn);
    });
  }
  renderQuestion();

  document.getElementById('btn-restart-quiz').addEventListener('click', () => {
    qIdx = 0;
    qScore = 0;
    quizContainer.style.display = 'block';
    quizFinished.style.display = 'none';
    renderQuestion();
  });

  // Lock button
  document.getElementById('btn-lock').addEventListener('click', () => {
    window.location.reload();
  });

})();
"""

bundle_payload = {
    'html': app_html,
    'css': app_css,
    'js': app_js,
    'data': data
}

json_bytes = json.dumps(bundle_payload).encode('utf-8')
print(f"Decrypted payload raw size: {len(json_bytes)} bytes")

# AES-256-GCM Encryption with PBKDF2
salt = os.urandom(16)
iv = os.urandom(12)
iterations = 100000

kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=iterations
)
key = kdf.derive(PASSWORD)
aesgcm = AESGCM(key)
ciphertext_with_tag = aesgcm.encrypt(iv, json_bytes, None)

data_part = ciphertext_with_tag[:-16]
tag_part = ciphertext_with_tag[-16:]

enc_bundle = {
    'salt': base64.b64encode(salt).decode('ascii'),
    'iv': base64.b64encode(iv).decode('ascii'),
    'data': base64.b64encode(data_part).decode('ascii'),
    'tag': base64.b64encode(tag_part).decode('ascii'),
    'iterations': iterations
}

with open(r"c:\Users\DrAvE\vs_workspaces\Love2Love\pepsi.enc", "w", encoding="utf-8") as f:
    json.dump(enc_bundle, f)

print("Saved pepsi.enc successfully!")
