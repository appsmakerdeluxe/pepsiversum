# Pepsiversum (Love2Love)

Ein zutiefst persönliches, clientseitig verschlüsseltes Web-Projekt, das als interaktive Liebeserklärung und Erinnerungsspeicher dient.

## 🌟 Projektübersicht

Dieses Projekt ist keine gewöhnliche Webseite. Es ist eine **passwortgeschützte, vollständig verschlüsselte "Web-App"**, die ohne Backend auskommt. Alle Daten, Bilder, Texte und Erinnerungen werden lokal in eine einzige Datei kompiliert und mit AES-GCM verschlüsselt. Erst durch die Eingabe des korrekten Passworts im Browser der Endnutzerin wird der Inhalt lokal im Arbeitsspeicher entschlüsselt und dargestellt.

Dadurch sind alle persönlichen Chatverläufe, Insider-Witze, Liebeserklärungen und gemeinsamen Bilder absolut sicher vor fremden Blicken.

## 🏗 Architektur & Tech-Stack

*   **Frontend:** Vanilla HTML5, CSS3, JavaScript (direkt generiert aus Python).
*   **Audio:** Web Audio API (synthetisiertes Schnurren, Miauen, Magie-Effekte).
*   **Sicherheit:** `crypto.subtle` (Web Crypto API) für die Entschlüsselung im Browser, Python `cryptography` für die Verschlüsselung beim Build.
*   **Build-System:** Python 3.

## 🚀 Build-Prozess

Wenn Änderungen an Inhalten oder am Design vorgenommen werden, muss die App neu kompiliert werden:

1.  **Inhalte anpassen:** Die Rohdaten (Zeitleiste, Whispers, Galerien) befinden sich in `builder.py`.
2.  **App-Struktur anpassen:** Das gesamte HTML, CSS und JavaScript befindet sich als riesiger String in `build_new_app.py`.
3.  **Kompilieren:** 
    ```bash
    python builder.py
    python build_new_app.py
    ```
4.  **Ergebnis:** Der Python-Build erzeugt die Datei `pepsi.enc`. Dies ist der verschlüsselte Payload, der auf GitHub Pages hochgeladen wird.

## 📂 Wichtige Dateien

*   `builder.py` – Definiert die Datenstrukturen (JSON-Export).
*   `build_new_app.py` – Der Kern-Compiler. Baut das HTML/JS zusammen und verschlüsselt es.
*   `pepsi.enc` – Die finale, verschlüsselte Datei (produktiv).
*   `WhatsApp-Chat mit Pepsi.txt` – Die Quelle für neue Inhalte, Zitate und Inspirationen.

---
*Erstellt mit ❤️ für die wichtigste Person im Universum.*
