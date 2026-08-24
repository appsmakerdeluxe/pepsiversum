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
    {'title': "🍕 Denis kocht Sellys Lieblingsessen", 'desc': "Küche reserviert für Denis – Selly darf sich einfach zurücklehnen und bekochen lassen.", 'tag': "Verwöhnung"}
]

# 7. SAFE HARBOR SOS BUTTONS
safe_harbor_data = [
    {
        'title': "Schlechter Tag?",
        'icon': "🌧️",
        'advice': "Atme tief durch. Ich bin hier, auch wenn alles schwer scheint.",
        'quote': "Nichts ist so dunkel, dass wir es nicht zusammen erhellen können.",
        'actionText': "Lass den Regen fallen, bis die Sonne wieder scheint.",
        'bonus': "Denk an das Matcha-Eis, das auf uns wartet."
    },
    {
        'title': "Gedankenkarussell?",
        'icon': "🌪️",
        'advice': "Dein Kopf ist zu laut. Lass uns kurz alles andere ausblenden.",
        'quote': "In meinem Arm ist es still. Hier bist du sicher.",
        'actionText': "Fokus. Einatmen. Ausatmen.",
        'bonus': "Ich liebe jede deiner Facetten, auch die chaotischen."
    },
    {
        'title': "Vermisse dich",
        'icon': "🥺",
        'advice': "Die Distanz ist nur physisch. Mein Herz ist direkt bei deinem.",
        'quote': "Es gibt keinen Ort auf der Welt, an dem ich lieber wäre als bei dir.",
        'actionText': "Spürst du den Herzschlag?",
        'bonus': "Schau auf den Mond, wir sehen beide denselben."
    },
    {
        'title': "Wütend auf die Welt?",
        'icon': "😡",
        'advice': "Lass es raus! Die Welt ist dumm, aber wir beide sind ein super Team.",
        'quote': "Wenn alles nervt, ärgern wir die Welt einfach zusammen.",
        'actionText': "Lass es platzen!",
        'bonus': "Pamuk würde jetzt zur Ablenkung auf einen Baum klettern."
    },
    
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

# 9. EXTENDED TIMELINE (Real + Future)
timeline_events = []
if len(messages) > 0:
    # 1. First Message
    timeline_events.append({
        'year': messages[0]['date'],
        'title': 'Der allererste Funke',
        'desc': f"Unsere erste Nachricht. {messages[0]['sender']} sagte: '{messages[0]['text'][:40]}...'"
    })

# Hunt for specific milestones
milestones_found = set()
for m in messages:
    txt = m['text'].lower()
    date = m['date']
    if 'ich liebe dich' in txt and 'first_ily' not in milestones_found:
        timeline_events.append({'year': date, 'title': 'Die drei Worte', 'desc': f"{m['sender']}: '{m['text']}'"})
        milestones_found.add('first_ily')
    elif 'katze' in txt and 'first_cat' not in milestones_found:
        timeline_events.append({'year': date, 'title': 'Katzenthemen', 'desc': f"{m['sender']} bringt das wichtigste Thema auf den Tisch: Katzen."})
        milestones_found.add('first_cat')
    elif 'zukunft' in txt and 'first_future' not in milestones_found:
        timeline_events.append({'year': date, 'title': 'Zukunftsblicke', 'desc': f"Wir sprechen zum ersten Mal über unsere gemeinsame Zukunft."})
        milestones_found.add('first_future')
    elif 'eis' in txt and 'first_icecream' not in milestones_found:
        timeline_events.append({'year': date, 'title': 'Eis-Sucht', 'desc': f"Der Beginn unserer endlosen Eis-Dates."})
        milestones_found.add('first_icecream')
    elif 'suri' in txt and 'suri' not in milestones_found:
        timeline_events.append({'year': date, 'title': 'Suri betritt den Chat', 'desc': f"Die wahre Chefin wird erwähnt."})
        milestones_found.add('suri')

# Add a bunch of random cute moments spread across the timeline
import random
random.seed(42)
cute_msgs = [m for m in messages if len(m['text']) > 40 and any(k in m['text'].lower() for k in ['perfekt', 'danke', 'süß', 'schön', 'glücklich', 'kuscheln', 'wunderschön', 'traum'])]
if len(cute_msgs) > 10:
    sampled = random.sample(cute_msgs, min(10, len(cute_msgs)))
    # Sort them back by their original occurrence to keep time roughly linear
    sampled.sort(key=lambda x: messages.index(x))
    for i, m in enumerate(sampled):
        timeline_events.append({
            'year': m['date'],
            'title': f'Kapitel {i+1} der Verliebtheit',
            'desc': f"{m['sender']}: '{m['text'][:100]}...'"
        })

# Sort the past events strictly by their index in the chat to maintain chronological order
timeline_events.sort(key=lambda x: [m['date'] for m in messages].index(x['year']) if x['year'] in [m['date'] for m in messages] else 0)

# Add future milestones
future_events = [
    {'year': '2025', 'title': 'Der erste Urlaub', 'desc': 'Koffer packen, Flugtickets und Sonnenuntergänge.'},
    {'year': '2026', 'title': 'Zusammenziehen', 'desc': 'Kartons schleppen und das erste gemeinsame Frühstück in der neuen Küche.'},
    {'year': '2027', 'title': 'Suri & Pamuk\'s neues Reich', 'desc': 'Wir bauen den größten Kratzbaum der Welt ins Wohnzimmer.'},
    {'year': '2028', 'title': 'Der Roadtrip', 'desc': 'Mit dem Auto durch Europa, nur wir zwei und gute Musik.'},
    {'year': '2030', 'title': 'Die Hochzeit', 'desc': 'Ein Ring, ein Versprechen, ein großes Fest mit Suri & Pamuk als Ehrengäste.'},
    {'year': '2032', 'title': 'Das Traumhaus', 'desc': 'Wir kaufen unser Haus mit großem Garten.'},
    {'year': '2035', 'title': 'Familie', 'desc': 'Unser Zuhause füllt sich mit noch mehr Lachen und Leben.'},
    {'year': '2040', 'title': 'Das Haus am See', 'desc': 'Hunde, Kinderlachen und endlos Platz.'},
    {'year': '2050', 'title': 'Silberhochzeit', 'desc': '25 Jahre, und ich sehe dich immer noch so an wie am ersten Tag.'},
    {'year': '2060', 'title': 'Weltreise', 'desc': 'Wir haben Zeit. Wir reisen um die ganze Welt.'},
    {'year': '2074', 'title': 'Die Parkbank', 'desc': 'Wir sitzen alt und grau auf einer Bank und halten immer noch Händchen.'}
]
timeline_events.extend(future_events)

# 10. TRIVIA QUIZ
quiz_questions = [
    {'q': 'Wie lange wollen wir mindestens zusammenbleiben?', 'options': ['50 Jahre', '100 Jahre', '150 Jahre', 'Bis zur Unendlichkeit'], 'answer': 2},
    {'q': 'Wer von uns beiden ist der absolute Katzen-Boss im Haus?', 'options': ['Denis', 'Selly', 'Suri', 'Pamuk'], 'answer': 2},
    {'q': 'Welches Jahr markiert den offiziellen Start unserer Geschichte?', 'options': ['2022', '2023', '2024', '2025'], 'answer': 2},
    {'q': 'Was essen wir am liebsten (über 2.400 Erwähnungen im Chat)?', 'options': ['Pizza', 'Döner', 'Eis', 'Sushi'], 'answer': 2},
    {'q': 'Wo werden wir im Jahr 2074 sitzen?', 'options': ['Im Schaukelstuhl', 'Auf einer Parkbank', 'Am Strand', 'Im Raumschiff'], 'answer': 1},
    {'q': 'Wie wird Pamuk oft liebevoll genannt?', 'options': ['Der Kletterer/Chaot', 'Der Schläfer', 'Der Fresser', 'Der Schmuser'], 'answer': 0},
    {'q': 'Zu welcher Uhrzeit entstanden unsere tiefsten Gespräche?', 'options': ['20-22 Uhr', '0-2 Uhr', '2-5 Uhr', 'Am Vormittag'], 'answer': 2},
    {'q': 'Welches Land/Konzept verbindet aus Scherben wieder Gold (Kintsugi)?', 'options': ['China', 'Japan', 'Südkorea', 'Thailand'], 'answer': 1},
    {'q': 'Was ist dein süßer Spitzname, der auch auf den Startbildschirm dieser Seite passt?', 'options': ['Schnecke', 'Bärchen', 'Pepsi', 'Mausi'], 'answer': 2},
    {'q': 'Wie heißt mein (Denis) Spitzname oft von dir?', 'options': ['Pepe', 'Deni', 'Bär', 'Schatz'], 'answer': 0},
    {'q': 'Welche Farbe hat das SOS "Vermisse dich" Modal?', 'options': ['Blau', 'Grün', 'Lila', 'Warmes Rot/Pink'], 'answer': 3},
    {'q': 'Wer schnarcht/blockiert am meisten Platz im Bett?', 'options': ['Suri', 'Pamuk', 'Denis', 'Selly'], 'answer': 0},
    {'q': 'Welche Initialen sind in den Baum der Ewigkeit geritzt?', 'options': ['D & S', 'S N', 'S & P', 'P & D'], 'answer': 1},
    {'q': 'Was bringt das "Date Roulette" im Eislabor?', 'options': ['Kostenloses Eis', 'Zufällige Date-Ideen', 'Lustige Sprüche', 'Ein Spielzeug'], 'answer': 1},
    {'q': 'In welchem Jahr planen wir unsere Hochzeit (laut Blueprint)?', 'options': ['2026', '2028', '2030', '2035'], 'answer': 2},
    {'q': 'Was machen wir im Blueprint-Jahr 2040?', 'options': ['Weltreise', 'Haus am See', 'Marsmission', 'Pension'], 'answer': 1},
    {'q': 'Wie reagiere ich im Chat am häufigsten auf deine süßen Bilder?', 'options': ['Hahaha', 'Wunderschön', 'Okay', 'xD'], 'answer': 1},
    {'q': 'Wer ist der verrückte Baum-Kletterer unter den Katzen?', 'options': ['Suri', 'Selly', 'Denis', 'Pamuk'], 'answer': 3},
    {'q': 'Welches Symbol nutzen wir als "Schrein der Versprechen"?', 'options': ['Schloss', 'Ring', 'Siegel', 'Herz'], 'answer': 2},
    {'q': 'Was bedeutet es, wenn wir streiten?', 'options': ['Es ist vorbei', 'Wir sind müde', 'Wir wachsen durch Kintsugi stärker zusammen', 'Wir essen danach Eis'], 'answer': 2}
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
    'timeline': timeline_events,
    'quiz': quiz_questions
}

print("App data packaged! Size of JSON:", len(json.dumps(app_data)))

# Save raw payload to data.json for packaging
with open(r"c:\Users\DrAvE\vs_workspaces\Love2Love\data.json", "w", encoding="utf-8") as f:
    json.dump(app_data, f, ensure_ascii=False, indent=2)

print("Saved raw payload to data.json!")
