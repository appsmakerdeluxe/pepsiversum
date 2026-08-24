import re

# We will replace the cat sound bindings and the audio functions.

new_bindings = """
  // 4. Cats
  $all('.cat-sound').forEach(btn => {
    btn.addEventListener('click', (e) => {
      const type = e.target.dataset.type;
      if(type === 'sweetMeow') playSweetMeow();
      else if(type === 'sassyMeow') playSassyMeow();
      else playPurr();
      const heart = document.createElement('div');
"""

new_audio_functions = """
function playPurr() {
  safePlay(() => {
    const bufferSize = audioCtx.sampleRate * 2; // 2 seconds
    const buffer = audioCtx.createBuffer(1, bufferSize, audioCtx.sampleRate);
    const data = buffer.getChannelData(0);
    // Darker noise for purring
    for (let i = 0; i < bufferSize; i++) { data[i] = (Math.random() * 2 - 1) * 0.4; }
    const noise = audioCtx.createBufferSource();
    noise.buffer = buffer;
    
    // Lowpass filter to muffle the noise
    const biquad = audioCtx.createBiquadFilter();
    biquad.type = 'lowpass'; 
    biquad.frequency.value = 400; // a bit higher than 150 to hear the purr character
    
    // The "motor" of the purr (Amplitude Modulation)
    const gain = audioCtx.createGain();
    gain.gain.setValueAtTime(0, audioCtx.currentTime);
    
    const lfo = audioCtx.createOscillator();
    lfo.type = 'triangle'; // triangle gives a nice rhythmic in-out breathing feel
    lfo.frequency.value = 26; // cats purr at roughly 25-30 Hz
    
    const lfoGain = audioCtx.createGain(); 
    lfoGain.gain.value = 0.8; // deep modulation
    
    lfo.connect(lfoGain); 
    lfoGain.connect(gain.gain);
    
    noise.connect(biquad); 
    biquad.connect(gain); 
    gain.connect(audioCtx.destination);
    
    // Envelope for the whole sound
    gain.gain.linearRampToValueAtTime(0.8, audioCtx.currentTime + 0.2);
    gain.gain.linearRampToValueAtTime(0, audioCtx.currentTime + 1.9);
    
    noise.start(); 
    lfo.start(); 
    noise.stop(audioCtx.currentTime + 2); 
    lfo.stop(audioCtx.currentTime + 2);
  });
}

function playSweetMeow() {
  safePlay(() => {
    const osc = audioCtx.createOscillator();
    const gain = audioCtx.createGain();
    
    osc.connect(gain); 
    gain.connect(audioCtx.destination);
    
    osc.type = 'triangle'; 
    
    // Sweet, cute meow: high pitched, sliding up then slightly down
    osc.frequency.setValueAtTime(600, audioCtx.currentTime);
    osc.frequency.exponentialRampToValueAtTime(900, audioCtx.currentTime + 0.2);
    osc.frequency.exponentialRampToValueAtTime(750, audioCtx.currentTime + 0.5);
    
    gain.gain.setValueAtTime(0, audioCtx.currentTime);
    gain.gain.linearRampToValueAtTime(0.6, audioCtx.currentTime + 0.1);
    gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.5);
    
    osc.start(); 
    osc.stop(audioCtx.currentTime + 0.5);
  });
}

function playSassyMeow() {
  safePlay(() => {
    const osc = audioCtx.createOscillator();
    const gain = audioCtx.createGain();
    
    osc.connect(gain); 
    gain.connect(audioCtx.destination);
    
    // Sassy meow: sawtooth for a rougher, throatier sound
    osc.type = 'sawtooth'; 
    
    // Starts mid, goes up slightly, drops sharply
    osc.frequency.setValueAtTime(500, audioCtx.currentTime);
    osc.frequency.exponentialRampToValueAtTime(650, audioCtx.currentTime + 0.15);
    osc.frequency.exponentialRampToValueAtTime(300, audioCtx.currentTime + 0.6);
    
    gain.gain.setValueAtTime(0, audioCtx.currentTime);
    gain.gain.linearRampToValueAtTime(0.5, audioCtx.currentTime + 0.1);
    gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.6);
    
    osc.start(); 
    osc.stop(audioCtx.currentTime + 0.6);
  });
}
"""

with open('build_new_app.py', 'r', encoding='utf-8') as f:
    code = f.read()

# Replace bindings
old_bindings = """  // 4. Cats
  $all('.cat-sound').forEach(btn => {
    btn.addEventListener('click', (e) => {
      if(e.target.dataset.type === 'meow') playMeow();
      else playPurr();
      const heart = document.createElement('div');"""

code = code.replace(old_bindings, new_bindings)

# Replace playPurr
purr_pattern = re.compile(r'function playPurr\(\) \{.*?\n\}\n', re.DOTALL)
if purr_pattern.search(code):
    # we will just replace it with empty because we inject the whole block later
    code = purr_pattern.sub('', code)

sweet_pattern = re.compile(r'function playSweetMeow\(\) \{.*?\n\}\n', re.DOTALL)
if sweet_pattern.search(code):
    code = sweet_pattern.sub('', code)

sassy_pattern = re.compile(r'function playSassyMeow\(\) \{.*?\n\}\n', re.DOTALL)
if sassy_pattern.search(code):
    code = sassy_pattern.sub('', code)

# Inject the new audio functions right after playHeartbeat or just before playTada
code = code.replace('function playTada()', new_audio_functions + '\nfunction playTada()')

with open('build_new_app.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("Updated cat sounds!")
