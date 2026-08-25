# AppsMakerDeluxe – Love2Love / Pepsiversum (AGENTS.md)

Diese Datei dient als vollständige Dokumentation, Architekturübersicht und Entwicklungsleitfaden für das Projekt **Love2Love (Pepsiversum)** sowie als Blaupause für künftige, identisch aufgebaute Webprojekte.

---

## 1. 🚨 Kritische Sicherheits- & Datenschutz-Vorgaben (Strikte Priorität)

- **100% geschützt vor Öffentlichkeit und Suchmaschinen:**
  - Die gesamte Webanwendung und sämtliche vertraulichen Inhalte sind **ausschließlich nach Eingabe der geheimen Passphrase** zugänglich.
  - Ohne den korrekten Schlüssel sieht die Außenwelt und jeder Web-Crawler lediglich die leere Gatekeeper-Startseite (`index.html`).
  - Im `<head>` sind stets `<meta name="robots" content="noindex,nofollow,noarchive" />` und `<meta name="referrer" content="no-referrer" />` verankert, um jegliche Suchmaschinen-Indexierung zuverlässig zu unterbinden.
- **Keine README.md oder öffentlichen Klartext-Dokumente:**
  - Im Root-Verzeichnis darf **niemals** eine `README.md` angelegt werden. Dies verhindert, dass das Repository und persönliche Inhalte auf GitHub gerendert oder von Suchmaschinen erfasst werden.
- **Keine Klartext-Chats, Passwörter oder persönliche Daten im Git-Remote:**
  - Rohe Chat-Exportdateien (`WhatsApp*.txt`, `*.log`, `data.json`) sowie unverschlüsselte Bildoriginale gehören ausnahmslos in die `.gitignore`.
  - Passwörter und kryptografische Schlüssel dürfen **niemals** im Klartext in committete Dateien, Tickets oder Git-Logs geschrieben werden.
- **GitHub Repository & Sichtbarkeit:**
  - Repository: `https://github.com/appsmakerdeluxe/pepsiversum`
  - GitHub-Organisation: `appsmakerdeluxe` (Verwaltung und Authentifizierung via `gh` CLI).
  - Das Repository verbleibt standardmäßig privat und wird über GitHub Pages statisch ausgeliefert.
- **Lokale Build-Tools vs. Remote Runtime:**
  - Alle Generierungs-, Parsing- und Build-Skripte (`*.py`) verbleiben ausschließlich lokal und sind in `.gitignore` ignoriert.
  - Im Remote-Repository befinden sich ausschließlich die für die Client-Ausführung benötigten statischen Dateien: `index.html`, `unlock.css`, `unlock.js`, `pepsi.enc`, `.nojekyll`, `.gitignore` und `AGENTS.md`.
- **Entkopplung neuer Projekte (Design- & Inhalts-Autonomie):**
  - Diese Datei dient als technische Architektur-Blaupause (Kryptografie, Gatekeeper-Logik, Zero-Backend-Modell).
  - **Neue Projekte**, die auf dieser Architektur aufbauen, erhalten ein **völlig eigenständiges Design, Theme, Look & Feel sowie individuelle Inhalte**, die komplett unabhängig von Pepsiversum gestaltet werden.


---

## 2. 🏗 Architektur & Funktionsweise (Zero-Backend Single Page Application)

Das System besitzt **kein serverseitiges Backend**. Es handelt sich um eine statische Webanwendung, die auf GitHub Pages gehostet wird und ein clientseitig verschlüsseltes Payload (`pepsi.enc`) im Browser entschlüsselt.

```
[Lokaler Workflow (Offline)]
Rohdaten (Chats/JSON) -> Monolithische HTML/CSS/JS Assemblierung -> PBKDF2 + AES-GCM (256-bit) -> pepsi.enc

[Client Runtime (Browser)]
GitHub Pages (index.html + unlock.js + unlock.css)
        │
        ▼ (Nutzer gibt Passwort ein)
Web Crypto API (crypto.subtle) entschlüsselt pepsi.enc
        │
        ▼ (document.write(payload.html))
Vollständige, interaktive Webanwendung wird nahtlos gerendert
```

### Die Runtime-Komponenten:
1. **`index.html` (Gatekeeper Landing Page):**
   - Minimalistisches, atmosphärisches UI mit schwebendem Sternenhimmel und pulsierendem Orb (`#orb-trigger`).
   - Schützt die App durch ein geschütztes Passwortformular (`#unlock`), das erst nach Klick/Tastendruck sanft eingeblendet wird.
   - Verwendet `robots=noindex,nofollow,noarchive` und `referrer=no-referrer` im `<head>`.
2. **`unlock.css` (Gatekeeper Stylesheet):**
   - Eigenständiges CSS für den Landing-Screen (Radial-Gradients, Ambient-Partikel, Glasmorphismus-Karten, responsive Typografie).
3. **`unlock.js` (Entschlüsselungs-Engine):**
   - Lädt `pepsi.enc` via `fetch('pepsi.enc', { cache: 'no-store' })`.
   - Nutzt die native Web Crypto API (`crypto.subtle`).
   - Leitet aus der eingegebenen Passphrase mittels PBKDF2 (SHA-256, 100.000 Iterationen) den 256-Bit AES-GCM Schlüssel ab.
   - Entschlüsselt das Bundle und injiziert den kompletten HTML-String via `document.open(); document.write(payload.html); document.close();`.
4. **`pepsi.enc` (Verschlüsseltes Anwendungs-Payload):**
   - Enthält ein JSON-Objekt mit Base64-kodierten Feldern:
     - `salt`: 16 Bytes Zufallssalt für PBKDF2.
     - `iv`: 12 Bytes Initialisierungsvektor für AES-GCM.
     - `iterations`: Anzahl der PBKDF2-Iterationen (Standard: `100000`).
     - `data`: Der verschlüsselte Chiffretext des Payloads.
     - `tag`: 16 Bytes AES-GCM Authentifizierungs-Tag.
   - Entschlüsseltes JSON-Format: `{"html": "<!DOCTYPE html><html>...</html>"}`.
5. **`.nojekyll`:**
   - Verhindert, dass GitHub Pages Dateien oder Ordner mit führenden Unterstrichen oder speziellen Endungen filtert.

---

## 3. 🎨 Design-System & Ästhetik-Spezifikation

Die visuelle Gestaltung folgt einem luxuriösen, romantisch-magischen und modernen Editorial-Look.

### Farbpalette (CSS-Variablen):
- `--ink: #142526` (Tiefe, edle Textfarbe)
- `--deep: #08282b` (Mystischer, dunkler Hintergrund)
- `--sea: #236d6a` (Petrol-Akzent für Links & Highlights)
- `--cream: #f4efe5` (Warmer, pergamentartiger Grundton)
- `--sand: #d8c8af` (Sanfte Zwischentöne & Rahmen)
- `--gold: #b5925e` (Edles Gold für Zitate, Icons & Sterne)
- `--paper: #fbf8f1` (Karten- und Container-Hintergrund)
- `--line: rgba(20, 37, 38, 0.16)` (Dezente Trennlinien)

### Typografie:
- **Headlines / Zitate:** `'Playfair Display', Georgia, serif` (Editorial, elegant, emotional)
- **Fließtext / UI:** `'DM Sans', Arial, sans-serif` (Klar, modern, lesefreundlich)
- **Metadaten / Zahlen / Badges:** `'DM Mono', monospace` (Feine Zeitstempel, Indikatoren)

---

## 4. 🧩 Feature-Blueprint & Module der entschlüsselten App

Die entschlüsselte Anwendung ist vollständig autark und kombiniert zahlreiche interaktive Erlebnisbereiche:

### A. Web Audio API Synthesizer (Zero-Asset Sound Engine)
Alle Klänge werden rein mathematisch im Browser synthetisiert – keine externen MP3/WAV-Dateien erforderlich:
- **`safePlay(fn)`:** Fängt gesperrte AudioContext-States ab (`audioCtx.state === 'suspended'`) und resumed bei Nutzerinteraktion.
- **`playPop()`:** Kurzer, sanfter Sinus-Ramp (600 Hz -> 800 Hz) mit exponentiellem Gain-Decay für Button-Klicks.
- **`playHeartbeat()`:** Tiefer 50 Hz Sinus-Doppelpuls für romantische Momente.
- **`playPurr()`:** Niederfrequenter Modulations-Oszillator (25–35 Hz) zur Nachbildung eines Katzenschnurrens.
- **`playSweetMeow()` / `playSassyMeow()`:** Frequenzmodulierte Formant-Sweeps für verspielte Katzenlaute.
- **`playChime()` & `playTada()`:** Harmonische Glocken-Akkorde und Fanfaren für Belohnungen und Quiz-Erfolge.

### B. Partikel- und Visual Effects Engine
- **`createFireworks()`:** Bunte Funkenregen-Explosionen im DOM/Canvas bei Meilensteinen.
- **`createConfetti()`:** Schwebende Konfetti-Elemente bei richtigen Antworten.
- **`createFloatingHearts()`:** Sanft aufsteigende Herz-Partikel beim Antippen von Liebesbekundungen.
- **`createRain()` & Ambient Stars:** Stimmungsvolle Hintergrund-Partikel zur Vertiefung der Atmosphäre.
- **`initObserver()`:** `IntersectionObserver` steuert sanftes Scroll-Fade-In (`.reveal` -> `.is-visible`).

### C. Interaktive Erlebnis-Hubs & Features
1. **Das Buch unseres Lebens (Interactive 3D Storybook):**
   - Dreidimensionales Blättern mit echten Seitenumschlag-Animationen (`flipBookNext()`, `flipBookPrev()`, `toggleBookFlap()`).
2. **Midnight FM (Spotify Jukebox):**
   - Spotify-Player-Embeds gefiltert nach Stimmungen (*Late Night Chill*, *Deep Romance*, *Energy & Driving*, *Melancholy & Heart*).
   - Volltextsuche nach Liedern, Interpreten und Chat-Kontexten.
3. **Late Night Whispers (02–05 Uhr):**
   - Spezielle Sammlung emotionaler Zitate, die zu nächtlichen Stunden entstanden sind.
4. **Kintsugi: Aus Scherben wird Gold:**
   - Interaktive Reflexion über Herausforderungen und gemeinsame Stärke, visualisiert durch goldene Verbindungslinien.
5. **Katzen-Palast (Suri & Pamuk):**
   - Interaktive Steckbriefe der Haustiere mit integrierter Miau- und Schnurr-Soundauslösung.
6. **Eislabor & Date-O-Mat (Date Roulette):**
   - Spontaner Zufallsgenerator für gemeinsame Aktivitäten, Lieblings-Eissorten und Unternehmungen.
7. **Blueprint 150 Jahre:**
   - Interaktiver Zukunftsplaner mit gemeinsamen Lebenszielen, Reiseplänen und Träumen.
8. **Safe Harbor SOS:**
   - Sofortiger Trost- und Beruhigungs-Button mit geführter Atem-Animation und tröstenden Worten.
9. **Schrein der Versprechen:**
   - Feierlich gestaltete Eide und Versprechen mit virtuellem Wachssiegel-Effekt.
10. **Zeitreise / Interaktive Timeline (2024–2074):**
    - Chronologischer Zeitstrahl mit Meilensteinen, ersten Begegnungen und Zukunftsdaten.
11. **Memory Side Quest & Quiz:**
    - Multiple-Choice-Quiz über gemeinsame Erlebnisse mit sofortigem Audio-Feedback und Punkte-Tracker.
12. **Waldkapelle & Kerzenschein:**
    - Stimmungsvolle Szene mit interaktiv entzündbaren Kerzenflammen und sanftem Lichtschein.

---

## 5. 🛠 Bauanleitung für ein neues, ähnliches Projekt

Wenn eine neue verschlüsselte Webanwendung erstellt wird, folgenden Ablauf durchführen:

### Schritt 1: Lokales Datenmodell definieren
Strukturierte Inhalte (Zitate, Meilensteine, Quiz-Fragen, Spotify-IDs) lokal in einer `data.json` oder in Python-Dictionaries vorbereiten.

### Schritt 2: Monolithische HTML-Struktur aufbauen
Eine vollständige HTML-Datei entwerfen, in die:
- Alle CSS-Styles im `<style>`-Tag eingebettet sind.
- Alle Audio-Synthesizer und Partikelfunktionen im `<script>`-Tag enthalten sind.
- Eventuelle persönliche Bilder direkt als **Base64-Strings** (`data:image/jpeg;base64,...`) in `<img>`-Tags oder CSS-Backgrounds integriert sind.
- Die strukturierten Daten als JavaScript-Objekt (`const appData = { ... };`) vorliegen.

### Schritt 3: Verschlüsselungs-Pipeline (Python) ausführen
Nutze das folgende Referenz-Skript (lokal ausführen):

```python
import os
import json
import base64
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

def build_encrypted_payload(html_content: str, password: str, output_path: str = "pepsi.enc", iterations: int = 100000):
    salt = os.urandom(16)
    iv = os.urandom(12)
    
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=iterations
    )
    key = kdf.derive(password.encode('utf-8'))
    aesgcm = AESGCM(key)
    
    payload_json = json.dumps({"html": html_content}, ensure_ascii=False).encode('utf-8')
    ciphertext_with_tag = aesgcm.encrypt(iv, payload_json, None)
    
    ciphertext = ciphertext_with_tag[:-16]
    tag = ciphertext_with_tag[-16:]
    
    bundle = {
        "salt": base64.b64encode(salt).decode('ascii'),
        "iv": base64.b64encode(iv).decode('ascii'),
        "iterations": iterations,
        "data": base64.b64encode(ciphertext).decode('ascii'),
        "tag": base64.b64encode(tag).decode('ascii')
    }
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(bundle, f)
    print(f"Erfolgreich verschlüsselt: {output_path} ({len(html_content)} Bytes HTML)")
```

### Schritt 4: Gatekeeper-Dateien bereitstellen
Sicherstellen, dass im Web-Root `index.html`, `unlock.css` und `unlock.js` liegen.

### Schritt 5: Git-Bereinigung & Deployment
1. `.gitignore` prüfen (enthält `*.py`, `*.txt`, `data.json`, `*.log`).
2. Nur `index.html`, `unlock.css`, `unlock.js`, `*.enc`, `.nojekyll`, `.gitignore` und `AGENTS.md` committen.
3. Nach `origin/main` pushen.
4. In den GitHub Repository Settings **GitHub Pages** auf den Branch `main` (Root `/`) aktivieren.

---

## 6. ⚠️ Bekannte Fallstricke & Agenten-Regeln

1. **Keine nachträglichen `.reveal`-Klassen bei dynamischem DOM-Einfügen:**
   - Elemente, die erst nach dem Initial-Render per JavaScript erzeugt werden (z. B. nächste Quizfrage oder dynamische Karten), dürfen nicht die Klasse `.reveal` tragen, da der `IntersectionObserver` bereits abgeschlossen ist. Stattdessen CSS-Keyframe-Animationen (`animation: fadeIn 0.6s forwards;`) nutzen.
2. **Audio-Autoplay-Blockaden:**
   - Soundaufrufe müssen zwingend über direkte Nutzeraktionen (Click/Tap) initiiert werden und über `safePlay()` laufen.
3. **Keine HTML-Direktbearbeitung im Remote:**
   - Niemals versuchen, entschlüsselte Inhalte direkt in `index.html` abzulegen. `index.html` bleibt immer das reine Gatekeeper-Portal.

---

## 7. 🔒 AppsMakerDeluxe Master-Vorgaben

- **Systemintegrität:** Den Computer niemals herunterfahren, neustarten, in den Energiesparmodus/Ruhezustand versetzen oder sperren, außer es liegt eine ausdrückliche, aktuelle Benutzeranweisung vor.
- **Task-Management:** Hintergrundprozesse nach Abschluss terminieren; keine verwaisten Tasks hinterlassen.
- **Wissens-Synchronisation:** Generelle Verbesserungen an Verschlüsselung oder Gatekeeper-Technik werden in `C:\Users\DrAvE\vs_workspaces\AGENTS.md` gepflegt.
