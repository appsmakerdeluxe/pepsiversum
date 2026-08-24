import os
import re
import json
import base64
import hashlib
from collections import Counter
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

PASSWORD = b"suripamuk2026"
CHAT_FILE = r"c:\Users\DrAvE\vs_workspaces\Love2Love\WhatsApp-Chat mit Pepsi.txt"

print("Parsing WhatsApp chat...")
line_regex = re.compile(r'^\[?(\d{1,2}\.\d{1,2}\.\d{2,4})[,\s]+(\d{1,2}:\d{2}(?::\d{2})?)\]?\s*(?:-\s*)?([^:]+):\s*(.*)$')

messages = []
with open(CHAT_FILE, "r", encoding="utf-8", errors="ignore") as f:
    for line in f:
        m = line_regex.match(line)
        if m:
            date_str, time_str, sender, text = m.groups()
            messages.append({'date': date_str, 'time': time_str, 'sender': sender.strip(), 'text': text})

print(f"Total messages loaded: {len(messages)}")

# 1. SPOTIFY SONGS EXTRACTION (ALL UNIQUE)
spotify_tracks = []
seen_ids = set()

for i, m in enumerate(messages):
    matches = re.findall(r'https://open\.spotify\.com/(?:intl-[a-z]+/)?(track|album|playlist)/([a-zA-Z0-9]+)', m['text'])
    for kind, track_id in matches:
        if track_id not in seen_ids:
            seen_ids.add(track_id)
            txt = m['text']
            mood = "Love & Vibes"
            if any(w in txt.lower() for w in ['nacht', 'schlafen', 'bett', 'ruhig', 'chill']):
                mood = "Late Night Chill"
            elif any(w in txt.lower() for w in ['feiern', 'tanzen', 'party', 'auto', 'bass']):
                mood = "Energy & Driving"
            elif any(w in txt.lower() for w in ['herz', 'liebe', 'schön', 'engel', 'traum']):
                mood = "Deep Romance"
            elif any(w in txt.lower() for w in ['traurig', 'vermiss', 'allein', 'nachdenken']):
                mood = "Melancholy & Heart"
                
            spotify_tracks.append({
                'id': track_id,
                'type': kind,
                'url': f"https://open.spotify.com/{kind}/{track_id}",
                'embedUrl': f"https://open.spotify.com/embed/{kind}/{track_id}?utm_source=generator&theme=0",
                'sender': m['sender'],
                'date': m['date'],
                'time': m['time'],
                'msg': m['text'].replace('\n', ' ').strip()[:180],
                'mood': mood
            })

print(f"Extracted {len(spotify_tracks)} unique Spotify items.")

# 2. LATE NIGHT DIALOGUES (00:00 to 05:59)
romantic_kw = ['liebe dich', 'mein herz', 'engel', 'schnecke', 'traum', 'wunderschön', 'vermisse dich', 'nur dich', 'für immer', 'küssen', 'kuscheln', 'schönste', 'süße', 'süßer', 'glücklich', 'bärchen', 'schatz']
flirty_kw = ['sexy', 'heiß', 'bett', 'nackt', 'körper', 'berühren', 'spüren', 'ausziehen', 'verführen', 'anfassen', 'lippen', 'küssen', 'kuscheln', 'intim', 'erotik', 'lust', 'leidenschaft', 'vermiss', 'anziehen', 'wecken', 'warm', 'umarmen']
deep_kw = ['zukunft', 'angst', 'leben', 'druck', 'verstehen', 'nachdenken', 'mensch', 'herz', 'sorgen', 'egal was passiert', 'vertrauen', 'treue', 'zusammenhalt', 'problem', 'stolz', 'schaffen das']

keywords = romantic_kw + flirty_kw + deep_kw
late_night_dialogues = []
seen_indices = set()

for i, m in enumerate(messages):
    if i in seen_indices: continue
    
    hour = int(m['time'].split(':')[0])
    if hour in [0, 1, 2, 3, 4, 5]:
        txt = m['text'].strip().lower()
        if len(txt) > 30 and any(k in txt for k in keywords):
            if any(w in txt for w in ['gelöscht', '<medien ausgeschlossen>', 'image omitted', 'audio omitted']):
                continue
                
            window = messages[max(0, i-2) : min(len(messages), i+3)]
            senders = set(msg['sender'] for msg in window)
            
            if len(senders) > 1:
                dialogue_msgs = []
                for msg in window:
                    dialogue_msgs.append({
                        'date': msg['date'],
                        'time': msg['time'],
                        'sender': msg['sender'],
                        'text': msg['text']
                    })
                late_night_dialogues.append(dialogue_msgs)
                
                # skip nearby messages to avoid overlapping dialogues
                for j in range(max(0, i-4), min(len(messages), i+5)):
                    seen_indices.add(j)
                    
            if len(late_night_dialogues) >= 15:
                break

late_night_dict = {'romantic': late_night_dialogues}  # Keep format somewhat compatible, though we'll change frontend

# 3. KINTSUGI STORIES
kintsugi_stories = [
    {
        'title': "Der Schwur im Herzen",
        'date': "07.08.2025",
        'category': "Ewige Verbundenheit",
        'quote': "„Ich weiß nicht ob das eine Herausforderung ist der wir ausgesetzt sind oder was es ist, aber eines ist sicher: Ich habe deinen Namen in mein Herz geritzt und da bleibt er bis zum Tod.“",
        'author': "Denis",
        'lesson': "Egal wie viele Stürme oder Zweifel aufziehen – was Denis für Selly empfindet, ist für immer in Stein und Herz gemeißelt. Kein Streit kann das je auflösen."
    },
    {
        'title': "Unsere unterschiedlichen Love Languages",
        'date': "12.06.2025",
        'category': "Verständnis & Reife",
        'quote': "„Wir haben halt auch unterschiedliche Love Languages. Es ist ohnehin schon schwer übers Handy. Ich hasse Schreiben und liebe Telefonieren...“",
        'author': "Pepsi",
        'lesson': "Hier haben wir begriffen, wie der andere funktioniert: Denis drückt seine Gedanken oft in langen Texten aus – Selly braucht die lebendige Stimme und Nähe. Aus dem Verstehen wurde bedingungslose Liebe."
    },
    {
        'title': "Das Gedankenkarussell anhalten",
        'date': "01.06.2026",
        'category': "Ehrliche Entschuldigung",
        'quote': "„Ich weiß nicht wieso ich so reagiert habe, es hatten sich plötzlich viele Sachen im Kopf gestaut und manchmal ist es dann zu spät und man denkt sich: Hätte ich vorher nachgedacht. Es tut mir leid.“",
        'author': "Denis",
        'lesson': "Die wahre Stärke unserer Beziehung liegt darin, dass wir stolzlos sagen können: 'Ich habe einen Fehler gemacht, du bist mir wichtiger als mein Ego.'"
    },
    {
        'title': "Kein Druck im Leben",
        'date': "19.01.2025",
        'category': "Bedingungsloser Rückhalt",
        'quote': "„Niemand ist weiter im Leben als jemand anderes, weißt du. Jeder führt sein eigenes Leben und geht seinen eigenen Weg... entspann dich, alles kommt zur richtigen Zeit.“",
        'author': "Pepsi",
        'lesson': "Wenn einer von uns unter Arbeits- oder Zukunftsstress steht, ist der andere der sichere Fels in der Brandung, der die Last von den Schultern nimmt."
    },
    {
        'title': "Wachbleiben trotz Frühschicht",
        'date': "13.01.2025",
        'category': "Aufopferung & Liebe",
        'quote': "„Ich bleib extra länger wach für dich und schau einen Film an, obwohl ich am nächsten Morgen schaffen muss... weil ich einfach bei dir sein wollte.“",
        'author': "Denis",
        'lesson': "Selbst wenn die Müdigkeit drückt und der Wecker unbarmherzig klingelt: Die gemeinsame Zeit ist unbezahlbar."
    }
]

# 4. BLUEPRINT 150-JAHRE ZUHAUSE
blueprint_rooms = [
    {
        'id': "kitchen",
        'name': "Die Küche der doppelten Geräte",
        'icon': "🍳",
        'items': [
            {'name': "Doppelte Kaffeemaschinen", 'desc': "Weil Denis und Selly immer exakt dasselbe kaufen und am Ende alles doppelt da ist!", 'quote': "29.12.25: 'Wenn wir zusammenziehen haben wir alles doppelt hahahaha'"},
            {'name': "Das 500-Liter Matcha- & Eis-Tiefkühlfach", 'desc': "Gefüllt mit Pistazien-, Schoko- und Fruchteis für spontane 3-Uhr-Nachts-Gelüste.", 'quote': "Über 2.460x Eis im Chat erwähnt!"},
            {'name': "Die Mitternachts-Snack-Theke", 'desc': "Für Pizza, Pasta, Döner und spontane Pfannkuchen-Eskalationen.", 'quote': "Hier wird gekocht, gelacht und genascht."}
        ]
    },
    {
        'id': "cats",
        'name': "Suri & Pamuks Luxus-Kletterturm",
        'icon': "🐱",
        'items': [
            {'name': "Der unzerstörbare Weihnachtsbaum-Kratzbaum", 'desc': "Damit der echte Weihnachtsbaum im Dezember überlebt.", 'quote': "30.12.24: 'Katzen turnen auf dem Baum im Garten rum'"},
            {'name': "Die Anti-Staub-&-Pfoten-Reinigungszone", 'desc': "Direkt neben dem Saugroboter, der 24/7 hinter Suri und Pamuk herfährt.", 'quote': "30.12.24: '1h nach dem Wischen wieder überall Dreck wegen den Katzen XD'"},
            {'name': "Die 'Suri schläft auf Selly'-Kuschelkoje", 'desc': "Aus der Selly erst aufstehen darf, wenn Suri es erlaubt.", 'quote': "29.12.24: 'Suri ist auf mir, kann mich nicht bewegen'"}
        ]
    },
    {
        'id': "cinema",
        'name': "Die Kuschel- & Serien-Lounge",
        'icon': "🎬",
        'items': [
            {'name': "Riesencouch mit 10 Kuscheldecken", 'desc': "Für endlose Game of Thrones, Harry Potter und Netflix-Marathons.", 'quote': "30.12.24: 'Game of Thrones ist eine der besten Serien aller Zeiten'"},
            {'name': "Denis' Gaming- & Technik-Setup", 'desc': "Wo gezockt, gelacht und manchmal geflucht wird.", 'quote': "Highspeed-Verbindung & maximale Gemütlichkeit"},
            {'name': "Der 'Bis-5-Uhr-Morgens-Wachbleib'-Modus", 'desc': "Mit ambientem Sternenlicht und warmen Decken.", 'quote': "Über 5.500 Late-Night-Nachrichten wurden hier zelebriert"}
        ]
    },
    {
        'id': "bedroom",
        'name': "Das 150-Jahre-Schlafgemach",
        'icon': "👑",
        'items': [
            {'name': "Das Königsbett der 150 Jahre", 'desc': "Hier gilt das ewige Versprechen: Für immer aneinander gekuschelt alt werden.", 'quote': "11.08.25: 'Heirate mich und du wirst 150 Jahre alt werden ich sorge für dich wie für mein eigenes Baby xD'"},
            {'name': "Nachtkästchen mit Sprachnachrichten-Archiv", 'desc': "170+ Sprachnachrichten und unzählige 'Gute Nacht mein Engel'-Momente.", 'quote': "Jeden Abend der schönste Abschluss des Tages"},
            {'name': "Der Kuschel-Vertrag", 'desc': "Niemand geht jemals traurig oder unversöhnt schlafen.", 'quote': "Besiegelt für immer"}
        ]
    }
]

# 5. CATS HUB (SURI & PAMUK)
cat_anecdotes = [
    {
        'title': "Suri blockiert das gesamte Bett",
        'date': "29.12.2024",
        'text': "Selly: 'Ne muss Suri ins Bett holen xD... Suri ist auf mir, ich kann mich nicht bewegen!' – Denis: 'Katzen beherrschen dein Leben haha!'",
        'sound': "purr"
    },
    {
        'title': "Der verbannte Weihnachtsbaum",
        'date': "30.12.2024",
        'text': "Selly: 'Und ich verbanne heute meinen Weihnachtsbaum in den Garten dann können die Katzen noch drauf rumturnen.'",
        'sound': "meow"
    },
    {
        'title': "Frisch gewischt vs. Katzenchaos",
        'date': "30.12.2024",
        'text': "Denis: 'Katzen sind halt böse!' – Selly: 'Aber 1h nachdem er gewischt hat ist wieder überall Dreck wegen den Katzen XD'",
        'sound': "meow"
    },
    {
        'title': "Silvester im Badezimmer",
        'date': "31.12.2024",
        'text': "Selly verschanzt sich mit Suri & Pamuk im Bad, um sie vor der Silvesterknallerei zu schützen. Denis schreibt ihr die ganze Nacht, um sie aufzuheitern.",
        'sound': "purr"
    },
    {
        'title': "Tierarzt-Notfall-Einsatz",
        'date': "13.01.2025",
        'text': "Denis: 'Musste zwischendurch zum Tierarzt mit den Kleinen...' – Gemeinsam sorgen wir uns um unsere Babys!",
        'sound': "meow"
    }
]

# 6. EISLABOR & DATE-ROULETTE
ice_flavors = [
    {'name': "Pistazie Royale", 'color': "#93c572", 'note': "Für die besten Sommertage am See mit dir"},
    {'name': "Dunkle Schoko-Leidenschaft", 'color': "#3d1e11", 'note': "So intensiv wie unsere 3-Uhr-Nachts-Gespräche"},
    {'name': "Matcha Vanilla Dream", 'color': "#88a071", 'note': "Weil du Matcha und süße Dinge über alles liebst"},
    {'name': "Himbeer-Prickeln", 'color': "#e30b5d", 'note': "Für jedes freche Lachen und Kitzeln im Bauch"},
    {'name': "Karamell-Keks Crunch", 'color': "#c68b59", 'note': "Süß, crunchy und unverzichtbar wie Denis"},
    {'name': "Mango-Strand-Sorbet", 'color': "#ff8243", 'note': "Für unsere zukünftigen Urlaube ans Meer"}
]

date_roulette_ideas = [
    {'title': "🍦 Spontane Eis-Eskalation", 'desc': "Denis spendiert Selly das größte Eis der Stadt mit 5 Kugeln & Streuseln!", 'tag': "Genuss"},
    {'title': "🌊 Romantischer Sonnenuntergang am See", 'desc': "Decke einpacken, Musik über Spotify anmachen, aneinanderkuscheln und den Himmel beobachten.", 'tag': "Romantik"},
    {'title': "🏰 Wien-Traum-Wochenende", 'desc': "Gemeinsam durch Wien spazieren, Sachertorte probieren und Schloss Schönbrunn unsicher machen.", 'tag': "Reise"},
    {'title': "🎬 12-Stunden-Filmmarathon im Bett", 'desc': "Popcorn, Nachos, Deckenburg bauen und eine komplette Serie durchsuchten.", 'tag': "Cozy"},
    {'title': "🍕 Denis kocht Sellys Lieblingsessen", 'desc': "Küche reserviert für Denis – Selly darf sich einfach zurücklehnen und bekochen lassen.", 'tag': "Verwöhnung"},
    {'title': "🐾 Katzenspieltag & Kuschel-Olymp", 'desc': "Suri & Pamuk mit Leckerlis verwöhnen und gemeinsam auf der Couch dösen.", 'tag': "Family"}
]

# 7. SAFE HARBOR SOS BUTTONS
safe_harbor_data = [
    {
        'id': "stress",
        'title': "⚡ Ich bin gestresst von der Arbeit / der Welt",
        'icon': "🍃",
        'advice': "Tief einatmen. Schließe für 10 Sekunden die Augen.",
        'quote': "„Niemand ist weiter im Leben als jemand anderes. Jeder führt sein eigenes Leben. Entspann dich, du machst das großartig.“ (Selly)",
        'actionText': "Atemübung starten",
        'bonus': "Ein virtueller Schultermassage- & Ruhe-Gutschein von Denis!"
    },
    {
        'id': "mad",
        'title': "🔥 Ich bin sauer oder enttäuscht",
        'icon': "❤️‍🩹",
        'advice': "Schau dir diesen Moment an: Wir haben uns geschworen, niemals die Wut gewinnen zu lassen.",
        'quote': "„Ich habe deinen Namen in mein Herz geritzt und da bleibt er bis zum Tod.“ (Denis, 07.08.2025)",
        'actionText': "Friedenspfeife rauchen",
        'bonus': "Gutschein: Denis gibt sofort nach, entschuldigt sich mit einer Umarmung & bringt Eis!"
    },
    {
        'id': "miss",
        'title': "🥺 Ich vermisse dich gerade unendlich",
        'icon': "🌌",
        'advice': "Egal wo wir gerade physisch sind: Im Herzen halten wir uns fest an den Händen.",
        'quote': "„Ich bleib für dich wach, egal wie müde ich bin... weil du mein Zuhause bist.“",
        'actionText': "Herzschlag spüren",
        'bonus': "Sofort eine Sprachnachricht oder ein 'Ich liebe dich' anfordern!"
    },
    {
        'id': "hug",
        'title': "🧸 Ich brauche einfach Liebe & Geborgenheit",
        'icon': "💖",
        'advice': "Kuscheldecke nehmen, diesen Bildschirm ansehen und wissen: Du wirst bedingungslos geliebt.",
        'quote': "„Heirate mich und du wirst 150 Jahre alt werden...“ (11.08.2025)",
        'actionText': "Mega-Knuddler auslösen",
        'bonus': "Unendlicher digitaler Kuschel-Vorrat aktiviert!"
    }
]

# 8. THE PROMISE VAULT
promises = [
    {
        'id': "p1",
        'seal': "👑",
        'title': "Das 150-Jahre-Versprechen",
        'date': "11.08.2025",
        'text': "Wir haben versprochen, gemeinsam durchs Leben zu gehen, füreinander zu sorgen und gemeinsam steinalt und glücklich zu werden.",
        'status': "Für immer versiegelt"
    },
    {
        'id': "p2",
        'seal': "💍",
        'title': "Das Treue- & Schutz-Gelübde",
        'date': "09.07.2026",
        'text': "Denis verspricht Selly, ihr immer den Rücken freizuhalten, sie vor allem Schlechten zu beschützen und ihr Wort stets über alles andere zu stellen.",
        'status': "Ewig gültig"
    },
    {
        'id': "p3",
        'seal': "❤️‍🩹",
        'title': "Der Versöhnungs-Pakt",
        'date': "07.08.2025",
        'text': "Egal wie hitzig ein Gespräch wird: Wir schlafen nie im Streit ein und wissen immer, dass unsere Liebe stärker ist als jedes Missverständnis.",
        'status': "Unzerbrechlich"
    },
    {
        'id': "p4",
        'seal': "🐾",
        'title': "Das Katzen- & Familien-Versprechen",
        'date': "30.12.2024",
        'text': "Gemeinsam auf Suri & Pamuk aufpassen, egal wie viel Chaos sie anrichten oder wie viele Haare auf der Couch liegen.",
        'status': "Pfoten-Ehrenwort"
    }
]

# 9. TIMELINE 2024 TO 2074
timeline_milestones = [
    {'year': "29.12.2024", 'title': "Der Funke zündet", 'desc': "Die allererste Nachricht im Chat. Niemand ahnte, dass daraus über 215.000 Nachrichten und eine unendliche Liebesgeschichte werden."},
    {'year': "Silvester 2024", 'title': "Katzen-Schutz & Nachtwache", 'desc': "Selly verschanzt sich mit den Katzen im Bad, Denis hält ihr stundenlang digital die Hand."},
    {'year': "Sommer 2025", 'title': "Tiefe Bekenntnisse & Schwüre", 'desc': "Der Schwur 'Name ins Herz geritzt', die 150-Jahre-Heirats-Sprüche und unzählige Spotify-Nächte."},
    {'year': "2026", 'title': "Das Jetzt & Unsere Festung", 'desc': "Gereift, unzertrennlich, verständnisvoll. Wir wissen genau, wie der andere tickt und halten zusammen wie Pech und Schwefel."},
    {'year': "2028 - 2030", 'title': "Das gemeinsame Reich", 'desc': "Die erste gemeinsame Wohnung. Doppelte Geräte, eine gigantische Eistruhe und glückliche Katzen."},
    {'year': "2040+", 'title': "Große Abenteuer & Reisen", 'desc': "Wien, Strände am Mittelmeer, Roadtrips mit Musik aus unserem 183-Lieder-Mixtape."},
    {'year': "2074+", 'title': "150 Jahre & Parkbank-Eis", 'desc': "Mit 80 Jahren Hand in Hand auf einer Bank sitzen, heimlich Matcha-Eis löffeln und über alte WhatsApp-Nachrichten lachen."}
]

# 10. TRIVIA QUIZ
quiz_questions = [
    {
        'q': "Wie oft wurde das Wort 'Eis' in unserem Chat erwähnt?",
        'options': ["Ca. 50 Mal", "Über 2.400 Mal!", "Exakt 120 Mal", "Gar nicht"],
        'answer': 1,
        'explanation': "Über 2.460 Mal! Eis ist Sellys absolute Superkraft und unser Dauer-Thema."
    },
    {
        'q': "Wo verschanzte sich Selly an Silvester 2024 mit den Katzen?",
        'options': ["Im Kleiderschrank", "Im Badezimmer", "Auf dem Dachboden", "Unter dem Bett"],
        'answer': 1,
        'explanation': "Im Badezimmer, um Suri & Pamuk vor der Knallerei zu beschützen!"
    },
    {
        'q': "Was passiert laut Denis, wenn wir zusammenziehen?",
        'options': ["Wir haben nichts zu essen", "Wir haben alles doppelt, weil wir immer dasselbe kaufen!", "Wir streiten um die Fernbedienung", "Die Katzen übernehmen die Macht"],
        'answer': 1,
        'explanation': "Denis am 29.12.25: 'Wenn wir zusammenziehen haben wir alles doppelt hahahaha!'"
    },
    {
        'q': "Wie alt wird Denis laut Sellys legendärem Heirats-Schwur?",
        'options': ["80 Jahre", "100 Jahre", "150 Jahre alt!", "Unsterblich"],
        'answer': 2,
        'explanation': "Selly am 11.08.25: 'Heirate mich und du wirst 150 Jahre alt werden ich sorge für dich wie für mein Baby XD'"
    },
    {
        'q': "Wohin verbannte Selly ihren Weihnachtsbaum nach den Feiertagen?",
        'options': ["In den Müll", "In den Garten für die Katzen zum Klettern", "In den Keller", "Zum Nachbarn"],
        'answer': 1,
        'explanation': "In den Garten, damit Suri & Pamuk darauf rumturnen konnten!"
    },
    {
        'q': "Was ist laut Denis sicher am 07.08.2025?",
        'options': ["Dass es regnet", "Dass er Sellys Namen in sein Herz geritzt hat", "Dass er Urlaub braucht", "Dass Suri hungrig ist"],
        'answer': 1,
        'explanation': "Denis: 'Eines ist sicher: Ich habe deinen Namen in mein Herz geritzt und da bleibt er bis zum Tod.'"
    },
    {
        'q': "Welche Serie wurde im Chat als 'eine der besten aller Zeiten' gefeiert?",
        'options': ["Breaking Bad", "Game of Thrones", "Squid Game 2", "The Walking Dead"],
        'answer': 1,
        'explanation': "Game of Thrones! (Während Squid Game 2 eher enttäuscht hat xD)"
    },
    {
        'q': "Wie viele Late-Night-Nachrichten haben wir zwischen 2:00 und 5:00 Uhr geschrieben?",
        'options': ["Ca. 200", "Rund 1.000", "Über 5.500 Nachrichten!", "Genau 50"],
        'answer': 2,
        'explanation': "Unglaubliche 5.556 Nachrichten zu nachtschlafender Zeit!"
    },
    {
        'q': "Was ist Sellys bevorzugte Love Language beim Handy?",
        'options': ["Lange Aufsätze schreiben", "Telefonieren & Voice Notes", "Nur Emojis schicken", "Rauchzeichen"],
        'answer': 1,
        'explanation': "Selly: 'Ich hasse Schreiben und liebe Telefonieren!' (während Denis Romane textet)."
    },
    {
        'q': "Wie heißen unsere beiden geliebten Chaoten auf vier Pfoten?",
        'options': ["Luna & Milo", "Suri & Pamuk", "Bella & Simba", "Pepsi & Cola"],
        'answer': 1,
        'explanation': "Suri & Pamuk! Der Namensgeber für unser geheimes Passwort 'suripamuk2026'."
    }
]

app_data = {
    'meta': {
        'title': "Love2Love: Selly & Denis Sanctuary",
        'created': "2026-08-24",
        'totalMsgs': len(messages),
        'uniqueSpotify': len(spotify_tracks),
        'cats': ["Suri", "Pamuk"],
        'passphraseHint': "suripamuk2026"
    },
    'spotify': spotify_tracks,
    'lateNight': late_night_dict,
    'kintsugi': kintsugi_stories,
    'blueprint': blueprint_rooms,
    'catsData': cat_anecdotes,
    'iceCreamLab': {
        'flavors': ice_flavors,
        'dates': date_roulette_ideas
    },
    'safeHarbor': safe_harbor_data,
    'promises': promises,
    'timeline': timeline_milestones,
    'quiz': quiz_questions
}

print("App data packaged! Size of JSON:", len(json.dumps(app_data)))

# Save raw payload to data.json for packaging
with open(r"c:\Users\DrAvE\vs_workspaces\Love2Love\data.json", "w", encoding="utf-8") as f:
    json.dump(app_data, f, ensure_ascii=False, indent=2)

print("Saved raw payload to data.json!")
