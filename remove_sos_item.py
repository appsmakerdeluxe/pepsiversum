import re

with open('builder.py', 'r', encoding='utf-8') as f:
    code = f.read()

# The item to remove:
target = """    {
        'title': "Und noch etwas...",
        'icon': "❤️",
        'advice': "Egal was passiert, egal wie schwer die Zeiten sein mögen...",
        'quote': "Du bist das absolut Schönste, was mir in meinem ganzen Leben passiert ist. Ich liebe dich über alles, mein Schatz.",
        'actionText': "Für immer dein Pepe.",
        'bonus': "150 Jahre und länger. ♾️"
    }"""

# Sometimes emojis or commas differ, let's use a regex to remove the dict with 'title': "Und noch etwas..."
pattern = re.compile(r'\{\s*\'title\':\s*"Und noch etwas\.\.\.".*?\},?', re.DOTALL)
if pattern.search(code):
    code = pattern.sub('', code)
    print("Removed 'Und noch etwas...' from builder.py")
else:
    print("Could not find 'Und noch etwas...' block using regex")

with open('builder.py', 'w', encoding='utf-8') as f:
    f.write(code)
