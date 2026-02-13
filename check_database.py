import sqlite3
import sys

try:
    conn = sqlite3.connect('law_bot.db')
    cursor = conn.cursor()
    
    # Проверяем таблицы
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print('Найденные таблицы:')
    for t in tables:
        print(f'  - {t[0]}')
        
    # Проверяем данные в основных таблицах
    for table_name in ['users', 'partner_profiles', 'case_questionnaires', 'referral_relationships', 'referral_payouts']:
        try:
            cursor.execute(f'SELECT COUNT(*) FROM {table_name}')
            count = cursor.fetchone()[0]
            print(f'{table_name}: {count} записей')
        except Exception as e:
            print(f'{table_name}: ошибка - {e}')
    
    conn.close()
except Exception as e:
    print(f'Ошибка: {e}')
    sys.exit(1)
