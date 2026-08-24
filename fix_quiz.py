import json
with open('builder.py', 'r', encoding='utf-8') as f:
    code = f.read()

prefix = code[:code.find('# 10. TRIVIA QUIZ')]
suffix = code[code.find('app_data = {'):]

quiz = """# 10. TRIVIA QUIZ
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

"""

with open('builder.py', 'w', encoding='utf-8') as f:
    f.write(prefix + quiz + suffix)
