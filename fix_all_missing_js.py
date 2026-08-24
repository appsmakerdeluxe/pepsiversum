import re

js_inject = '''
      // ==========================================
      // KAPELLE & FINAL BUTTON & MINIGAMES JS
      // ==========================================
      
      const kapelleBtn = $('#kapelle-interact');
      if (kapelleBtn) {
        kapelleBtn.addEventListener('click', () => {
          kapelleBtn.style.display = 'none';
          const content = $('#kapelle-content');
          content.style.display = 'block';
          // Start animation
          content.style.animation = 'flyIn 1.5s ease-out forwards';
          
          playChime();
          
          // Spawn some light particles (sparks)
          const c = document.createElement('div');
          c.className = 'rain-container';
          c.style.position = 'fixed';
          c.style.top = '0'; c.style.left = '0'; c.style.width = '100%'; c.style.height = '100%';
          c.style.pointerEvents = 'none';
          c.style.zIndex = '9999';
          document.body.appendChild(c);
          
          for(let i=0; i<40; i++) {
            const p = document.createElement('div');
            p.innerHTML = '✨';
            p.style.position = 'absolute';
            p.style.fontSize = (Math.random() * 15 + 10) + 'px';
            p.style.left = (Math.random() * 100) + 'vw';
            p.style.bottom = '-50px';
            p.style.animation = `fall ${Math.random() * 4 + 4}s linear reverse forwards`;
            c.appendChild(p);
          }
        });
      }

      const finalBtn = $('#final-btn');
      if (finalBtn) {
        finalBtn.addEventListener('click', () => {
          finalBtn.style.display = 'none';
          const finalText = $('#final-text-container');
          finalText.style.display = 'block';
          finalText.style.animation = 'flyIn 2s ease-out forwards';
          playTada();
          
          const c = document.createElement('div');
          c.className = 'rain-container';
          c.style.position = 'fixed';
          c.style.top = '0'; c.style.left = '0'; c.style.width = '100%'; c.style.height = '100%';
          c.style.pointerEvents = 'none';
          c.style.zIndex = '9999';
          document.body.appendChild(c);
          
          for(let i=0; i<150; i++) {
            const p = document.createElement('div');
            p.innerHTML = '❤️';
            p.style.position = 'absolute';
            p.style.fontSize = (Math.random() * 25 + 10) + 'px';
            p.style.left = (Math.random() * 100) + 'vw';
            p.style.top = '-50px';
            p.style.animation = `fall ${Math.random() * 5 + 4}s linear forwards, spin ${Math.random() * 3 + 2}s linear infinite`;
            p.style.animationDelay = (Math.random() * 5) + 's';
            c.appendChild(p);
          }
        });
      }

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
            $('#fort-result').style.animation = 'flyIn 1s forwards';
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
'''

with open('build_new_app.py', 'r', encoding='utf-8') as f:
    code = f.read()

# Make sure we don't double inject if it's there
if 'KAPELLE & FINAL BUTTON & MINIGAMES JS' in code:
    print("Already injected.")
else:
    # Inject right before `renderApp();`
    code = code.replace('renderApp();', js_inject + '\n\nrenderApp();')
    with open('build_new_app.py', 'w', encoding='utf-8') as f:
        f.write(code)
    print("Injected all missing JS!")
