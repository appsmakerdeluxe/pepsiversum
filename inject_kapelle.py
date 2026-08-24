import re

# Read base64
with open(r'C:\Users\DrAvE\vs_workspaces\Love2Love\b64_kapelle.txt', 'r') as f:
    b64_img = f.read()

# Build HTML
kapelle_html = f'''
    <!-- KAPITEL 11 -->
    <section class="section" id="chapter-11">
      <h2 class="title reveal">Kapitel 11: Ein Kanal zu unseren Herzen</h2>
      <p class="reveal">
        Es gibt Momente, in denen das Universum stillsteht und uns zeigt, dass wir verbunden sind.<br>
        Selbst wenn wir nicht am selben Ort sind, spüren wir dasselbe.
      </p>
      
      <div id="kapelle-interact" class="reveal" style="margin: 40px auto; padding: 20px; background: rgba(0,0,0,0.6); border: 1px solid var(--gold); border-radius: 20px; cursor: pointer; transition: transform 0.3s; max-width: 500px;">
        <div style="font-size: 3rem;">🕯️</div>
        <h3 style="color: var(--gold);">Zünde eine Kerze für uns an</h3>
        <p style="font-size: 0.9rem; opacity: 0.8;">(Berühren)</p>
      </div>

      <div id="kapelle-content" style="display: none; opacity: 0; transition: opacity 2s ease-in-out;">
        <img src="data:image/jpeg;base64,{b64_img}" style="width: 100%; max-width: 400px; border-radius: 10px; margin: 20px auto; display: block; box-shadow: 0 10px 30px rgba(0,0,0,0.5);">
        
        <div style="text-align: left; max-width: 600px; margin: 0 auto; background: rgba(0,0,0,0.4); padding: 20px; border-left: 3px solid var(--gold); border-radius: 0 10px 10px 0;">
          <p style="font-style: italic; color: #ddd; margin-bottom: 10px;">"Bitte hilf seinem Vater wieder gesund zu werden. Auf dass seiner Familie nie etwas zustoßen wird und er sein großes Glück finden wird. Bitte beschütze ihn für immer! 24.8.26 D.S.N"</p>
          <p style="color: var(--brand); font-weight: bold;">- Deine Worte in der Waldkapelle, im exakt selben Moment, als ich durch eine Nonne an dich dachte.</p>
          <br>
          <p style="font-style: italic; color: #ddd; margin-bottom: 10px;">"Möge Maria dich auf all deinen Wegen begleiten... und wir werden durch sie einen Kanal zu unseren Herzen haben, wann immer einer von uns ruft."</p>
          <p style="color: var(--gold); font-weight: bold;">- Mein Versprechen an dich.</p>
        </div>
      </div>
    </section>

    <!-- FINAL BUTTON -->
    <div style="text-align: center; margin-bottom: 50px;">
      <button id="final-btn" class="reveal" style="padding: 15px 30px; font-size:1.2rem; background: var(--gradient-brand); color:white; border:none; border-radius:30px; font-weight:bold; cursor:pointer; box-shadow: 0 5px 15px rgba(255,77,109,0.4); transition: transform 0.3s;">Und noch etwas...</button>
      <div id="final-text-container" style="display:none; max-width:800px; margin: 20px auto 40px auto; padding: 20px; background: rgba(0,0,0,0.4); border-radius:15px; border: 1px solid rgba(255,255,255,0.1); font-style:italic; line-height: 1.8; color: var(--gold); text-align: left;">
        Du sagtest mal zu mir, wenn ich dich arg vermisse und dich hören will, soll ich dich einfach anrufen, der schlaf sei Dir egal... Ich möchte Dir trotzdem 10 Gründe nennen, wieso ich dich so sehr liebe und schätze: 
        <br><br>1. Ich liebe deine stimme, ich muss immer lächeln wenn du redest am Telefon. 
        <br>2. Deine art und dein Wesen, viele Momente die mir einfach das Gefühl geben wie wunderbar du bist.
        <br>3. Deine Offenheit und Ehrlichkeit, egal wann egal wo.
        <br>4. Deine liebevollen Tipps. 
        <br>5. Deine offenheit und dein Vertrauen mir gegenüber. 
        <br>6. Deine Stärke die du trotz deiner Vergangenheit und den Rückschlägen ausstrahlst. 
        <br>7. Das thema seele und die Zufälle zwischen uns. 
        <br>8. Ich liebe es zu hören dass es Momente gab an denen du mich auch stark vermisst hast. 
        <br>9. Ich liebe deine augen, du hast für mich einfach die schönsten augen auf dem Planeten. 
        <br>10. Ich liebe dich dafür dass ich dich kennen darf. Du hast ein so gutes Herz und ich wünschte ich könnte dich einfach umarmen und dir einfach in deine augen schauen, du fehlst mir einfach so sehr... Ich liebe Dich sehr ❤️.
      </div>
    </div>
'''

with open('build_new_app.py', 'r', encoding='utf-8') as f:
    code = f.read()

if 'KAPITEL 11' not in code:
    code = code.replace('</main>', kapelle_html + '\n  </main>')

# Add JS logic
js_inject = '''
      // Kapelle Interaction
      $('#kapelle-interact')?.addEventListener('click', () => {
        $('#kapelle-interact').style.display = 'none';
        const content = $('#kapelle-content');
        content.style.display = 'block';
        setTimeout(() => content.style.opacity = '1', 50);
        
        playTada();
        
        // Spawn some light particles (sparks)
        const c = document.createElement('div');
        c.className = 'rain-container';
        document.body.appendChild(c);
        for(let i=0; i<30; i++) {
          const p = document.createElement('div');
          p.innerHTML = '✨';
          p.style.position = 'absolute';
          p.style.fontSize = (Math.random() * 10 + 10) + 'px';
          p.style.left = (Math.random() * 100) + 'vw';
          p.style.bottom = '-50px';
          p.style.animation = `fall ${Math.random() * 4 + 4}s linear reverse forwards`;
          c.appendChild(p);
        }
      });

      // Final Button Logic
      $('#final-btn')?.addEventListener('click', () => {
        $('#final-btn').style.display = 'none';
        $('#final-text-container').style.display = 'block';
        $('#final-text-container').style.animation = 'fadeIn 2s forwards';
        playTada();
        
        const c = document.createElement('div');
        c.className = 'rain-container';
        document.body.appendChild(c);
        for(let i=0; i<100; i++) {
          const p = document.createElement('div');
          p.innerHTML = '❤️';
          p.style.position = 'absolute';
          p.style.fontSize = (Math.random() * 20 + 10) + 'px';
          p.style.left = (Math.random() * 100) + 'vw';
          p.style.top = '-50px';
          p.style.animation = `fall ${Math.random() * 4 + 4}s linear forwards, spin ${Math.random() * 3 + 2}s linear infinite`;
          p.style.animationDelay = (Math.random() * 5) + 's';
          c.appendChild(p);
        }
      });
'''
if 'kapelle-interact' not in code:
    code = code.replace('// INIT APP', js_inject + '\n      // INIT APP')

with open('build_new_app.py', 'w', encoding='utf-8') as f:
    f.write(code)
