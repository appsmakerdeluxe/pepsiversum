import re
import json

CHAT_FILE = r'c:\Users\DrAvE\vs_workspaces\Love2Love\WhatsApp-Chat mit Pepsi.txt'
line_regex = re.compile(r'^\[?(\d{1,2}\.\d{1,2}\.\d{2,4})[,\s]+(\d{1,2}:\d{2}(?::\d{2})?)\]?\s*(?:-\s*)?([^:]+):\s*(.*)$')

messages = []
with open(CHAT_FILE, 'r', encoding='utf-8', errors='ignore') as f:
    for line in f:
        m = line_regex.match(line)
        if m:
            messages.append({'date': m.group(1), 'time': m.group(2), 'sender': m.group(3).strip(), 'text': m.group(4).strip()})

dialogues = []
seen_indices = set()
keywords = ['für immer', 'liebe dich', 'zukunft', 'ohne dich', 'mein herz', '150 jahre', 'heiraten', 'danke dass es']

for i, m in enumerate(messages):
    if i in seen_indices: continue
    
    hour = int(m['time'].split(':')[0])
    if hour in [0,1,2,3,4,5]:
        txt = m['text'].lower()
        if any(k in txt for k in keywords) and len(txt) > 40:
            window = messages[max(0, i-2) : min(len(messages), i+3)]
            senders = set(msg['sender'] for msg in window)
            if len(senders) > 1:
                dialogues.append(window)
                for j in range(max(0, i-4), min(len(messages), i+4)):
                    seen_indices.add(j)
            if len(dialogues) >= 15:
                break

for idx, d in enumerate(dialogues):
    print(f'--- Dialogue {idx+1} ---')
    for msg in d:
        print(f"{msg['time']} {msg['sender']}: {msg['text']}")
