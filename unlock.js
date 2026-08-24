const form = document.querySelector('#unlock');
const input = document.querySelector('#passphrase');
const error = document.querySelector('#error');

document.querySelector('#open').addEventListener('click', () => { 
  form.hidden = false; 
  input.focus(); 
});

const bytes = value => Uint8Array.from(atob(value), char => char.charCodeAt(0));

async function decrypt(passphrase) {
  const bundle = await fetch('pepsi.enc', { cache: 'no-store' }).then(response => response.json());
  const material = await crypto.subtle.importKey('raw', new TextEncoder().encode(passphrase), 'PBKDF2', false, ['deriveKey']);
  
  const key = await crypto.subtle.deriveKey(
    { name: 'PBKDF2', salt: bytes(bundle.salt), iterations: bundle.iterations, hash: 'SHA-256' }, 
    material, 
    { name: 'AES-GCM', length: 256 }, 
    false, 
    ['decrypt']
  );
  
  const joined = new Uint8Array(bytes(bundle.data).length + bytes(bundle.tag).length); 
  joined.set(bytes(bundle.data)); 
  joined.set(bytes(bundle.tag), bytes(bundle.data).length);
  
  const decrypted = await crypto.subtle.decrypt({ name: 'AES-GCM', iv: bytes(bundle.iv) }, key, joined);
  return JSON.parse(new TextDecoder().decode(decrypted));
}

form.addEventListener('submit', async event => {
  event.preventDefault(); 
  error.textContent = 'Das Pepsiversum wird geöffnet …';
  
  try {
    const payload = await decrypt(input.value);
    // write the fully compiled HTML payload to document
    document.open(); 
    document.write(payload.html); 
    document.close();
  } catch (err) { 
    console.error(err);
    error.textContent = 'Der Code stimmt leider nicht. Versuch es noch einmal.'; 
    input.select(); 
  }
});
