with open('admin_panel/simple_test.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Найдем позицию для вставки скрипта
load_chat_dialogs_index = html.find('loadChatDialogs();')
if load_chat_dialogs_index == -1:
    print("Ошибка: не найден вызов loadChatDialogs()")
else:
    # Вставим скрипт перед вызовом loadChatDialogs()
    script = '''
    // Tab switching functionality
    function switchTab(tabName) {
        // Hide all content sections
        const sections = document.querySelectorAll('.section');
        sections.forEach(section => section.style.display = 'none');
        
        // Hide chat container if it's not the dialogs tab
        const chatContainer = document.querySelector('.chat-container');
        if (chatContainer) {
            chatContainer.style.display = tabName === 'dialogs' ? 'flex' : 'none';
        }
        
        // Show selected section
        if (tabName === 'home') {
            // Show all sections for home tab
            sections.forEach(section => section.style.display = 'block');
        }
        
        // Update active tab
        const tabs = document.querySelectorAll('.nav-links a');
        tabs.forEach(tab => tab.classList.remove('active'));
        event.target.classList.add('active');
    }

'''
    html = html[:load_chat_dialogs_index] + script + html[load_chat_dialogs_index:]

    # Добавим обработчики событий к ссылкам вкладок
    html = html.replace(
        '<a href="/test">🏠 Главная</a>',
        '<a href="#" onclick="switchTab(\'home\'); return false;">🏠 Главная</a>'
    )
    html = html.replace(
        '<a href="/dialogs">💬 Диалоги с пользователями</a>',
        '<a href="#" onclick="switchTab(\'dialogs\'); return false;">💬 Диалоги с пользователями</a>'
    )

    # Сохраним изменения
    with open('admin_panel/simple_test.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Скрипт для переключения вкладок добавлен")
