with open('build_new_app.py', 'r', encoding='utf-8') as f:
    code = f.read()

target_old = "stand schnurstracks auf und fuhr zu einer abgelegenen Waldkapelle. Dort entzündete sie eine Kerze und schrieb diese unendlich berührenden Zeilen in das Gästebuch:"
target_new = "stand schnurstracks auf und fuhr zu einer abgelegenen Waldkapelle. Dort schrieb sie diese unendlich berührenden Zeilen in das Gästebuch:"

if target_old in code:
    code = code.replace(target_old, target_new)
    print("Found and replaced UTF-8 string directly!")
else:
    # Try regex in case of slight encoding differences
    import re
    code = re.sub(
        r'stand schnurstracks auf und fuhr zu einer abgelegenen Waldkapelle\.\s*Dort entz.*?ndete sie eine Kerze und schrieb diese unendlich ber.*?hrenden Zeilen in das G.*?stebuch:',
        'stand schnurstracks auf und fuhr zu einer abgelegenen Waldkapelle. Dort schrieb sie diese unendlich berührenden Zeilen in das Gästebuch:',
        code
    )
    print("Replaced via regex fallback!")

with open('build_new_app.py', 'w', encoding='utf-8') as f:
    f.write(code)
