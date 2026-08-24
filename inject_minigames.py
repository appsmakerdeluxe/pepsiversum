import re

# --- HTML PAYLOAD ---
minigames_html = """
    <!-- KAPITEL 10.5 (SPIELZIMMER) -->
    <section class="section" id="spielzimmer">
      <h2 class="title reveal">Das Pepsiversum Spielzimmer</h2>
      <p class="reveal">Weil Erinnerungen nicht nur zum Lesen, sondern zum Erleben da sind. ❤️</p>
      
      <div class="mg-grid reveal">
        
        <!-- 1. Schnecke -->
        <div class="mg-card" id="card-schnecke">
          <div class="mg-title">Der Schnecken-Zähler</div>
          <div id="schnecke-emoji" style="font-size: 4rem; cursor: pointer; transition: transform 0.1s;">🐌</div>
          <div id="schnecke-count" style="font-size: 2rem; font-weight: bold; color: var(--brand); margin-top: 10px;">0</div>
          <p style="font-size: 0.8rem; margin-top:5px;">(Tippen!)</p>
        </div>

        <!-- 2. Gurken-Joghurt -->
        <div class="mg-card" id="card-gurke">
          <div class="mg-title">Cheat-Meal Maschine</div>
          <div id="mixer-container" style="font-size: 3rem; margin-bottom: 10px;">🌪️</div>
          <div id="mixer-items">
            <button id="btn-gurke" class="action-btn" style="font-size:1.5rem; padding: 5px 10px; margin: 5px;">🥒</button>
            <button id="btn-joghurt" class="action-btn" style="font-size:1.5rem; padding: 5px 10px; margin: 5px;">🥣</button>
          </div>
          <button id="btn-mix" class="action-btn" style="margin-top:15px; display:none;">MIXEN!</button>
          <div id="mixer-cert" style="display:none; color: var(--mint); font-weight: bold; margin-top: 10px; line-height:1.2;">🏆<br>Zertifikat:<br>Das traurigste Cheat-Meal der Welt</div>
        </div>

        <!-- 3. Day/Night Simulator -->
        <div class="mg-card" id="card-daynight" style="transition: background 1s;">
          <div class="mg-title" id="dn-title" style="transition: color 1s;">Gute Nacht, Herz</div>
          <div style="font-size: 3rem; transition: transform 0.5s;" id="dn-emoji">🌙</div>
          <input type="range" id="dn-slider" min="0" max="100" value="0" style="width: 80%; margin-top: 20px;">
          <div id="dn-text" style="margin-top: 15px; font-style: italic; transition: color 1s;">"Ich liebe dich, schlaf gut..."</div>
        </div>

        <!-- 4. Disney Roulette -->
        <div class="mg-card" id="card-disney">
          <div class="mg-title">Ticket-Roulette</div>
          <div id="ticket-slot" style="font-size: 1.2rem; font-weight:bold; background: #222; border-radius:10px; padding: 15px; min-width: 200px; margin: 10px auto; color: white;">🎰 Zieh den Hebel</div>
          <button id="btn-ticket" class="action-btn">Ticket ziehen</button>
        </div>

        <!-- 5. Pamuks Pfote -->
        <div class="mg-card" id="card-pamuk">
          <div class="mg-title">Nicht drücken!</div>
          <div id="pamuk-tower" style="font-size: 2.5rem; display:flex; flex-direction:column; align-items:center; gap:5px; transition: transform 0.5s ease-in;">
            <div>📦</div><div>🧸</div><div>🪴</div>
          </div>
          <button id="btn-pamuk" class="action-btn" style="margin-top:15px; background: #444;">Drücken</button>
          <div id="pamuk-paw" style="position: absolute; right: -100px; top: 30%; font-size: 5rem; transition: right 0.3s; z-index: 10;">🐾</div>
        </div>

        <!-- 6. Traum-Fänger -->
        <div class="mg-card" id="card-dream">
          <div class="mg-title">Seelen-Verbindung</div>
          <div style="position:relative; width: 100%; height: 100px; background: rgba(0,0,0,0.3); border-radius:10px;">
             <div class="orb" id="orb1" style="left: 10%; top: 20%;">✨</div>
             <div class="orb" id="orb2" style="left: 45%; top: 50%;">✨</div>
             <div class="orb" id="orb3" style="left: 75%; top: 10%;">✨</div>
          </div>
          <div id="dream-text" style="opacity: 0; font-style:italic; transition: opacity 1s; color: var(--gold); font-size: 0.9rem; margin-top:10px;">"Es hat uns etwas zusammen gebracht für einen Zweck..."</div>
        </div>

        <!-- 7. Massagekissen -->
        <div class="mg-card" id="card-massage">
          <div class="mg-title">Entspannung Pur</div>
          <div id="massage-device" style="font-size: 4rem; margin-bottom:10px; transition: transform 0.1s;">💆‍♀️</div>
          <button id="btn-massage" class="action-btn">Einschalten</button>
        </div>

        <!-- 8. Deckenburg -->
        <div class="mg-card" id="card-fort">
          <div class="mg-title">12h Film-Marathon</div>
          <div id="fort-items" style="font-size: 3rem; cursor:pointer;">🛏️ 🛏️ 🛏️</div>
          <div id="fort-result" style="display:none; font-size: 4rem;">🏰</div>
          <div id="fort-popcorn" style="display:none; font-size: 2rem;">🍿🍿🍿</div>
          <p style="font-size: 0.8rem; margin-top:10px;" id="fort-hint">(Tippe auf die Kissen)</p>
        </div>

        <!-- 9. Wut-Waschanlage -->
        <div class="mg-card" id="card-wut" style="background: rgba(255,0,0,0.2);">
          <div class="mg-title">Wut-Waschanlage</div>
          <button id="btn-wut" class="action-btn" style="background: red; border: 2px solid darkred;">Ich bin sauer!</button>
          <div id="wut-water" style="position:absolute; top:0; left:0; width:100%; height:0%; background: rgba(0, 150, 255, 0.9); transition: height 1s; display:flex; justify-content:center; align-items:center; overflow:hidden;">
             <span style="font-size:2rem; opacity:0; transition: opacity 1s; color:white; font-weight:bold; padding:20px;" id="wut-peace">🏳️<br>Frieden!<br>Wir ärgern die Welt einfach zusammen.</span>
          </div>
        </div>

        <!-- 10. Telepathie -->
        <div class="mg-card" id="card-tele">
          <div class="mg-title">Telepathie-Scanner</div>
          <div id="scanner" style="font-size: 4rem; opacity:0.7; cursor:pointer; transition: transform 0.1s; user-select:none;">👆</div>
          <p id="scanner-text" style="font-size:0.8rem; margin-top:10px;">Halte gedrückt und denke an uns...</p>
        </div>

      </div>
    </section>
"""

# --- CSS PAYLOAD ---
minigames_css = """
/* SPIELZIMMER CSS */
.mg-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px; margin-top: 40px; }
.mg-card { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,215,0,0.3); border-radius: 15px; padding: 20px; text-align: center; overflow: hidden; position: relative; min-height: 250px; display: flex; flex-direction: column; justify-content: center; align-items: center; box-shadow: 0 4px 15px rgba(0,0,0,0.2); }
.mg-title { font-family: var(--font-title); color: var(--gold); margin-bottom: 15px; font-size: 1.3rem; }
.orb { position: absolute; font-size: 2rem; cursor: pointer; transition: transform 0.3s, opacity 0.3s; animation: float 3s ease-in-out infinite alternate; }
.orb:hover { transform: scale(1.2); }
@keyframes shakeMg { 0% { transform: translate(1px, 1px) rotate(0deg); } 10% { transform: translate(-1px, -2px) rotate(-1deg); } 20% { transform: translate(-3px, 0px) rotate(1deg); } 30% { transform: translate(3px, 2px) rotate(0deg); } 40% { transform: translate(1px, -1px) rotate(1deg); } 50% { transform: translate(-1px, 2px) rotate(-1deg); } 60% { transform: translate(-3px, 1px) rotate(0deg); } 70% { transform: translate(3px, 1px) rotate(-1deg); } 80% { transform: translate(-1px, -1px) rotate(1deg); } 90% { transform: translate(1px, 2px) rotate(0deg); } 100% { transform: translate(1px, -2px) rotate(-1deg); } }
"""

# --- JS PAYLOAD ---
minigames_js = """
      // --- SPIELZIMMER JS ---
      
      // 1. Schnecke
      let schneckeCount = 0;
      const maxSchnecke = 1198;
      let schneckeInterval = null;
      $('#schnecke-emoji')?.addEventListener('click', () => {
         if(schneckeInterval) return;
         schneckeInterval = setInterval(() => {
            schneckeCount += 13;
            if(schneckeCount >= maxSchnecke) {
               schneckeCount = maxSchnecke;
               clearInterval(schneckeInterval);
               $('#schnecke-emoji').style.transform = 'scale(1.5)';
               playTada();
            } else {
               if(schneckeCount % 39 === 0) playPop();
            }
            $('#schnecke-count').innerText = schneckeCount;
         }, 20);
      });

      // 2. Mixer
      let mixerState = 0;
      const checkMixer = () => { if(mixerState===2) $('#btn-mix').style.display='inline-block'; };
      $('#btn-gurke')?.addEventListener('click', (e) => { e.target.style.display='none'; mixerState++; playPop(); checkMixer(); });
      $('#btn-joghurt')?.addEventListener('click', (e) => { e.target.style.display='none'; mixerState++; playPop(); checkMixer(); });
      $('#btn-mix')?.addEventListener('click', () => {
        $('#btn-mix').style.display='none';
        const m = $('#mixer-container');
        m.style.animation = 'shakeMg 0.5s infinite';
        setTimeout(()=>{
           m.style.animation = '';
           m.innerHTML = '🥒🥣💥';
           $('#mixer-cert').style.display = 'block';
           playTada();
        }, 1500);
      });

      // 3. Daynight
      $('#dn-slider')?.addEventListener('input', (e) => {
         const val = e.target.value;
         const card = $('#card-daynight');
         if(val > 50) {
            card.style.background = 'rgba(135, 206, 235, 0.2)';
            $('#dn-emoji').innerText = '☀️';
            $('#dn-title').innerText = 'Guten Morgen, Schnecke';
            $('#dn-title').style.color = '#fff';
            $('#dn-text').innerText = '"Guten Morgen mein Herz... wünsche dir einen wunderschönen Tag!"';
            $('#dn-text').style.color = '#fff';
         } else {
            card.style.background = 'rgba(0, 0, 50, 0.4)';
            $('#dn-emoji').innerText = '🌙';
            $('#dn-title').innerText = 'Gute Nacht, Herz';
            $('#dn-title').style.color = 'var(--gold)';
            $('#dn-text').innerText = '"Ich liebe dich, schlaf gut und träum süß..."';
            $('#dn-text').style.color = '#ddd';
         }
      });

      // 4. Disney
      const tickets = ['🍿 Horrorfilm', '🎬 Titanic', '😎 Avatar', '💀 12€ Disney Ticket'];
      $('#btn-ticket')?.addEventListener('click', () => {
        let ticks = 0;
        const slot = $('#ticket-slot');
        $('#btn-ticket').disabled = true;
        playPop();
        const intv = setInterval(()=>{
           slot.innerText = tickets[ticks % tickets.length];
           ticks++;
           if(ticks > 15 && (ticks % tickets.length) === 3) {
              clearInterval(intv);
              slot.style.color = 'red';
              slot.style.textShadow = '0 0 10px red';
              slot.innerText = '🔥 ' + slot.innerText + ' 🔥';
              playPop();
              setTimeout(()=> { $('#btn-ticket').disabled = false; slot.style.color=''; slot.style.textShadow=''; slot.innerText='🎰 Zieh den Hebel'; }, 3000);
           }
        }, 100);
      });

      // 5. Pamuk
      $('#btn-pamuk')?.addEventListener('click', () => {
         $('#pamuk-paw').style.right = '50px';
         playSassyMeow();
         setTimeout(()=>{
            const tower = $('#pamuk-tower');
            tower.style.transform = 'translateY(150px) rotate(90deg)';
            setTimeout(()=>{ $('#pamuk-paw').style.right = '-150px'; }, 500);
         }, 300);
      });

      // 6. Dream
      let orbsPop = 0;
      $all('.orb')?.forEach(o => {
         const popOrb = () => {
             if(o.style.opacity === '0') return;
             o.style.opacity = '0';
             orbsPop++;
             playChime();
             if(orbsPop === 3) {
                $('#dream-text').style.opacity = '1';
             }
         };
         o.addEventListener('mouseenter', popOrb);
         o.addEventListener('touchstart', (e)=> { e.preventDefault(); popOrb(); });
      });

      // 7. Massage
      $('#btn-massage')?.addEventListener('click', () => {
         if(navigator.vibrate) { try { navigator.vibrate([100,50,100,50,500]); } catch(e){} }
         const card = $('#card-massage');
         const dev = $('#massage-device');
         dev.style.animation = 'shakeMg 0.1s infinite';
         playPop();
         setTimeout(()=>{
            dev.style.animation = '';
            $('#btn-massage').style.transform = 'translateY(50px) rotate(25deg)';
            $('#btn-massage').innerText = 'Kaputt...';
         }, 1000);
      });

      // 8. Fort
      let fortClicks = 0;
      $('#fort-items')?.addEventListener('click', () => {
         fortClicks++;
         playPop();
         if(fortClicks >= 3) {
            $('#fort-items').style.display = 'none';
            $('#fort-hint').style.display = 'none';
            $('#fort-result').style.display = 'block';
            $('#fort-popcorn').style.display = 'block';
            $('#fort-result').style.animation = 'fadeIn 1s forwards';
            playTada();
         }
      });

      // 9. Wut
      $('#btn-wut')?.addEventListener('click', () => {
         $('#wut-water').style.height = '100%';
         playPop();
         setTimeout(()=>{
            $('#wut-peace').style.opacity = '1';
            playChime();
         }, 800);
      });

      // 10. Telepathie
      let teleTimeout;
      const scanner = $('#scanner');
      const startScan = (e) => {
         e.preventDefault();
         scanner.style.transform = 'scale(1.2)';
         playHeartbeat();
         teleTimeout = setTimeout(()=>{
            $('#scanner-text').innerText = 'Ich weiß nicht genau an welchen Moment du gedacht hast... aber ich weiß, dass du gerade gelächelt hast. Ich liebe dich. ❤️';
            $('#scanner-text').style.color = 'var(--gold)';
            scanner.innerText = '❤️';
            playTada();
         }, 3000);
      };
      const stopScan = (e) => {
         e.preventDefault();
         scanner.style.transform = 'scale(1)';
         clearTimeout(teleTimeout);
      };
      if(scanner) {
          scanner.addEventListener('mousedown', startScan);
          scanner.addEventListener('touchstart', startScan);
          scanner.addEventListener('mouseup', stopScan);
          scanner.addEventListener('touchend', stopScan);
          scanner.addEventListener('mouseleave', stopScan);
      }
"""

with open('build_new_app.py', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Inject HTML before KAPITEL 11 (if it exists, else before </main>)
if 'Das Pepsiversum Spielzimmer' not in code:
    if '<!-- KAPITEL 11 -->' in code:
        code = code.replace('<!-- KAPITEL 11 -->', minigames_html + '\n    <!-- KAPITEL 11 -->')
    else:
        code = code.replace('</main>', minigames_html + '\n  </main>')

# 2. Inject CSS before </style>
if 'SPIELZIMMER CSS' not in code:
    code = code.replace('</style>', minigames_css + '\n</style>')

# 3. Inject JS before // INIT APP
if 'SPIELZIMMER JS' not in code:
    code = code.replace('// INIT APP', minigames_js + '\n      // INIT APP')

with open('build_new_app.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("Injected Minigames successfully!")
