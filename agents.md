

# 🚨 CRITICAL PRIVACY & SECURITY WARNING 🚨
**DO NOT CREATE A README.md FILE OR ANY OTHER PUBLIC-FACING DOCUMENTATION.**
This project contains highly personal and intimate data. The GitHub repository might be public, and adding a README.md causes the project to be indexed by search engines and easily readable by strangers. 
**NEVER** expose the project's purpose, personal names, internal jokes, or sensitive context in plain text files in the root directory that render on GitHub. All instructions for AI agents MUST remain strictly inside this gents.md file (or other internal files), and you must guard the user's privacy above all else.
# 🤖 Agent Guidelines: Pepsiversum (Love2Love)

**CRITICAL INSTRUCTION FOR ALL AI AGENTS:** 
Read this document completely before modifying any code in this repository. This project has a highly unconventional architecture, and standard web development approaches (like editing `index.html` or creating standalone `.js` files) **will break the build**.

---

## 1. 📖 Context & Persona
- **Users:** Denis (the developer/client) and Selly/Pepsi (the recipient of the website).
- **Tone:** This is a deeply romantic, emotional, and personal project. When proposing ideas, always aim for beautiful, magical, interactive, and deeply contextual concepts (e.g., analyzing their WhatsApp chats to find inside jokes, spiritual moments, etc.).
- **Characters:** Suri and Pamuk are their cats. They are featured in the app (e.g., cat sounds, images).
- **Goal:** To maintain and extend an interactive, encrypted digital love letter.

## 2. 🏗 The Architecture (How it Works)
There is **NO** backend. The website is a static page that decrypts a payload (`pepsi.enc`) in the browser. 
You are **not** editing raw HTML files directly. You are editing Python scripts that generate the HTML string and encrypt it.

### The Pipeline:
1. `builder.py` -> Contains dictionaries and lists (whispers, gallery items, memory questions). It dumps this to `data.json`.
2. `build_new_app.py` -> Reads `data.json`. It contains a massive multi-line string (`full_html`) containing all HTML, CSS, and JS logic. It injects the JSON data into a JS variable inside the script tag. Then, it encrypts the *entire* HTML string using AES-GCM and saves it as `pepsi.enc`.
3. The real `index.html` (hosted on GitHub Pages, possibly in another repo branch) fetches `pepsi.enc`, asks the user for a password, decrypts the JSON payload, and renders the HTML.

## 3. 📝 How to Modify the Codebase

### A. Modifying Content/Data
If you just need to add a new question, a new "Late Night Whisper", or a timeline event:
- Edit `builder.py`.
- Run `python builder.py` to update `data.json`.
- Run `python build_new_app.py` to create the new `pepsi.enc`.

### B. Modifying HTML/CSS/JS (The Frontend)
If you need to add a new feature, a new chapter, animations, or DOM logic:
- Edit `build_new_app.py`.
- **WARNING:** Do not use `sed`, `awk`, or simple `grep`/Bash replacements to edit `build_new_app.py`. The file contains complex f-strings, JSON brackets `{ }`, and Python formatting that breaks instantly if mishandled in the shell.
- **BEST PRACTICE:** Write an injection Python script (e.g., `inject_feature.py`) that reads `build_new_app.py`, uses `.replace()` or string manipulation to insert your HTML/CSS/JS blocks, and writes the file back. See historical scripts like `inject_kapelle.py` or `fix_final.py` as examples.
- After modifying, always run `python build_new_app.py`.

### C. Adding Images
- Because the entire app is encapsulated in one encrypted payload, **images should be Base64 encoded** and embedded directly into the HTML/JS if they are personal/secret. 
- You can write a small script to read a `.jpg`, base64 encode it, and inject it into an `<img>` tag in `build_new_app.py`.

## 4. ⚠️ AI "Gotchas" & Known Issues

1. **IntersectionObserver (`.reveal` class):**
   - The app uses an IntersectionObserver to fade in elements as the user scrolls.
   - **Rule:** If you inject new DOM elements via JavaScript *after* the page has loaded (e.g., dynamically showing the next quiz question or revealing a modal), **do not** give them the `.reveal` class. The observer has already run. Use inline styles or CSS `@keyframes` (like `animation: fadeIn 1s forwards`) instead.
   
2. **Audio Context (Web Audio API):**
   - The app synthesizes sounds (cat meows, fireworks, magic chimes) using the `AudioContext`.
   - **Rule:** Browsers heavily restrict auto-playing audio. If you add a new sound, it **MUST** be wrapped in the `safePlay()` function provided in the JS. Calling `audioCtx.resume()` outside of a direct user interaction (like a button click) will fail or cause errors.

3. **Python String Formatting in `build_new_app.py`:**
   - The variable `full_html` is a multi-line string. If you use Python f-strings `f"""..."""`, be incredibly careful with CSS and JS braces `{}`. They must be escaped as `{{}}`. For this reason, `build_new_app.py` typically uses standard strings `"""..."""` and concatenates variables using `+ app_js +` to avoid formatting crashes.

## 5. 🔁 Standard Workflow for an AI Agent
When the user asks for a new feature:
1. **Analyze:** Check `WhatsApp-Chat mit Pepsi.txt` or the `verlauf/` folder to find beautiful, contextual meaning for the feature.
2. **Design:** Plan the UI (HTML), the Style (CSS animations, colors like `var(--gold)`, `var(--brand)`), and the Logic (Vanilla JS).
3. **Inject:** Write a python script to patch `build_new_app.py` or use your exact file editing tools carefully.
4. **Compile:** Run `python build_new_app.py`. Check for Python SyntaxErrors.
5. **Commit:** `git add .` and `git commit -m "Your descriptive message"` and `git push`. (Do not push `data.json` if it's in `.gitignore`, just push the `.py` files and `pepsi.enc`).
