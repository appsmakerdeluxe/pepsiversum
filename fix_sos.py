import re

with open('builder.py', 'r', encoding='utf-8') as f:
    code = f.read()

replacement = """# 7. SAFE HARBOR SOS BUTTONS
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
    {
        'title': "Und noch etwas...",
        'icon': "💌",
        'advice': "Egal was passiert, egal wie schwer die Zeiten sein mögen...",
        'quote': "Du bist das absolut Schönste, was mir in meinem ganzen Leben passiert ist. Ich liebe dich über alles, mein Schatz.",
        'actionText': "Für immer dein Pepe.",
        'bonus': "150 Jahre und länger. ❤️"
    }
]

# 8. THE PROMISE VAULT"""

code = re.sub(r'# 7\. SAFE HARBOR SOS BUTTONS.*?# 8\. THE PROMISE VAULT', replacement, code, flags=re.DOTALL)

with open('builder.py', 'w', encoding='utf-8') as f:
    f.write(code)
