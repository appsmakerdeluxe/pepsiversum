with open('builder.py', 'r', encoding='utf-8') as f:
    code = f.read()

# Fix the syntax error by moving the block out of the dict definition.
# 1. Remove the bad block
bad_block = """
# Rewrite Pepsi to Selly in timeline
for event in timeline_events:
    if 'desc' in event:
        event['desc'] = event['desc'].replace('Pepsi:', 'Selly:').replace('Pepsi bringt', 'Selly bringt')

"""
code = code.replace(bad_block, '')

# 2. Add it before app_data = {
if 'app_data = {' in code:
    code = code.replace('app_data = {', bad_block + 'app_data = {')
    with open('builder.py', 'w', encoding='utf-8') as f:
        f.write(code)
    print("Fixed builder.py syntax and injected properly")
