with open('update_storybook_fresh.py', 'r', encoding='utf-8') as f:
    script = f.read()

start_marker = 'new_storybook_js = """'
end_marker = '"""\n\n# Replace HTML'
idx1 = script.find(start_marker) + len(start_marker)
idx2 = script.find(end_marker)
new_js = script[idx1:idx2]

with open('build_new_app.py', 'r', encoding='utf-8') as f:
    code = f.read()

pos1 = code.find('// ==========================================\n      // DAS BUCH UNSERES LEBENS')
pos2 = code.find('renderApp();', pos1)

code = code[:pos1] + new_js + '\n\n      ' + code[pos2:]

with open('build_new_app.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("Replaced JS accurately!")
