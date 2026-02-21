with open('admin_panel/simple_test.html', 'r', encoding='utf-8') as f:
    html = f.read()
if 'switchTab' in html:
    print("Скрипт переключения вкладок добавлен")
    if 'onclick="switchTab' in html:
        print("Обработчики событий добавлены")
    else:
        print("Обработчики событий не найдены")
else:
    print("Скрипт не добавлен")
