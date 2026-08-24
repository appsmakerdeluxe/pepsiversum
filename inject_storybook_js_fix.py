with open('fix_storybook_direct.py', 'r', encoding='utf-8') as f:
    sb_script = f.read()

# Extract new_storybook_js from fix_storybook_direct.py
start_marker = 'new_storybook_js = """'
end_marker = '"""\n\n# Replace old storybook'
idx1 = sb_script.find(start_marker) + len(start_marker)
idx2 = sb_script.find(end_marker)
new_js = sb_script[idx1:idx2]

with open('build_new_app.py', 'r', encoding='utf-8') as f:
    code = f.read()

if 'touchZone.addEventListener' not in code:
    code = code.replace('renderApp();', new_js + '\n\n      renderApp();')
    with open('build_new_app.py', 'w', encoding='utf-8') as f:
        f.write(code)
    print("Injected Storybook JS right before renderApp()!")
else:
    print("Already present!")
