(function () {
  const form = document.getElementById('unlock-form');
  const input = document.getElementById('passphrase');
  const errorMsg = document.getElementById('error-msg');
  const unlockContainer = document.getElementById('unlock-container');
  const appRoot = document.getElementById('app-root');

  const b64ToUint8 = (b64) => {
    const binStr = atob(b64);
    const len = binStr.length;
    const bytes = new Uint8Array(len);
    for (let i = 0; i < len; i++) {
      bytes[i] = binStr.charCodeAt(i);
    }
    return bytes;
  };

  async function decryptPayload(passphrase) {
    const res = await fetch('pepsi.enc', { cache: 'no-store' });
    if (!res.ok) throw new Error('Verschlüsseltes Archiv konnte nicht geladen werden.');
    
    const bundle = await res.json();
    const salt = b64ToUint8(bundle.salt);
    const iv = b64ToUint8(bundle.iv);
    const data = b64ToUint8(bundle.data);
    const tag = b64ToUint8(bundle.tag);
    const iterations = bundle.iterations || 100000;

    // Concat data + tag for AES-GCM decryption
    const ciphertext = new Uint8Array(data.length + tag.length);
    ciphertext.set(data, 0);
    ciphertext.set(tag, data.length);

    const enc = new TextEncoder();
    const keyMaterial = await crypto.subtle.importKey(
      'raw',
      enc.encode(passphrase),
      'PBKDF2',
      false,
      ['deriveKey']
    );

    const key = await crypto.subtle.deriveKey(
      {
        name: 'PBKDF2',
        salt: salt,
        iterations: iterations,
        hash: 'SHA-256'
      },
      keyMaterial,
      { name: 'AES-GCM', length: 256 },
      false,
      ['decrypt']
    );

    const decryptedBuf = await crypto.subtle.decrypt(
      { name: 'AES-GCM', iv: iv },
      key,
      ciphertext
    );

    const decStr = new TextDecoder('utf-8').decode(decryptedBuf);
    return JSON.parse(decStr);
  }

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    errorMsg.textContent = '';
    const pass = input.value.trim();
    if (!pass) return;

    const btn = document.getElementById('btn-unlock');
    btn.disabled = true;
    btn.textContent = 'Entschlüssele...';

    try {
      const appData = await decryptPayload(pass);
      
      // Inject CSS
      const styleEl = document.createElement('style');
      styleEl.textContent = appData.css;
      document.head.appendChild(styleEl);

      // Set global data
      window.__PEPSI_DATA__ = appData.data;

      // Inject HTML
      appRoot.innerHTML = appData.html;
      unlockContainer.style.display = 'none';
      appRoot.style.display = 'block';

      // Execute JS
      const scriptFn = new Function(appData.js);
      scriptFn();

    } catch (err) {
      console.error(err);
      errorMsg.textContent = 'Falscher Zugangscode oder Entschlüsselung fehlgeschlagen.';
      btn.disabled = false;
      btn.textContent = 'Öffnen ➔';
      input.focus();
    }
  });
})();
