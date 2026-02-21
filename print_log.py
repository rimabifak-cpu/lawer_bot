with open('admin_panel.log', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    last_20 = lines[-20:] if len(lines) > 20 else lines
    for line in last_20:
        print(line.rstrip())
