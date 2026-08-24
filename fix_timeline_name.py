with open('builder.py', 'r', encoding='utf-8') as f:
    code = f.read()

# We need to replace "Pepsi" with "Selly" in the timeline generation logic.
# Wait, it's easier to just do a post-processing step on timeline_events right before it's assigned to app_data.
# Let's find:
# 'timeline': timeline_events,
# And insert a loop before it.

insertion = """
# Rewrite Pepsi to Selly in timeline
for event in timeline_events:
    if 'desc' in event:
        event['desc'] = event['desc'].replace('Pepsi:', 'Selly:').replace('Pepsi bringt', 'Selly bringt')
"""

if '# Rewrite Pepsi to Selly in timeline' not in code:
    code = code.replace("'timeline': timeline_events,", insertion + "\n    'timeline': timeline_events,")
    with open('builder.py', 'w', encoding='utf-8') as f:
        f.write(code)
    print("Injected rewrite logic into builder.py")
else:
    print("Already injected")
