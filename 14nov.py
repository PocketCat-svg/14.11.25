import sqlite3
import csv
import json


# Пример использования
# import_users_from_csv('users.csv')

# Создание/подключение к БД
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Создание таблицы пользователей
#cursor.execute('''
#CREATE TABLE IF NOT EXISTS belka (
#    id INTEGER PRIMARY KEY AUTOINCREMENT,
#    name TEXT NOT NULL,
#    email TEXT UNIQUE NOT NULL,
#    age INTEGER,
#    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
#)
#''')
#
#conn.commit()

#Импорт из csv

def import_users_from_csv(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            cursor.execute('''
            INSERT OR IGNORE INTO belka (name, email, age)
            VALUES (?, ?, ?)
            ''', (row['name'], row['email'], int(row['age'])))
    conn.commit()


# Множественная вставка
users_data = [
    ('Петр Петров', 'petr@mail.com', 30),
    ('Мария Сидорова', 'maria@mail.com', 28),
    ('Алексей Козлов', 'alex@mail.com', 35)
]

#cursor.executemany('''
#INSERT INTO belka (name, email, age)
#VALUES (?, ?, ?)
#''', users_data)

#conn.commit()


# Экспорт данных в JSON
def export_to_json():
    cursor.execute("SELECT * FROM belka")
    columns = [column[0] for column in cursor.description]
    users = [dict(zip(columns, row)) for row in cursor.fetchall()]
    
    with open('users.json', 'w', encoding='utf-8') as file:
        json.dump(users, file, ensure_ascii=False, indent=2)

# Импорт из JSON
def import_from_json(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        users = json.load(file)
        
    for user in users:
        cursor.execute('''
        INSERT OR REPLACE INTO belka (id, name, email, age)
        VALUES (?, ?, ?, ?)
        ''', (user['id'], user['name'], user['email'], user['age']))
    
    conn.commit()


# Простой SELECT
cursor.execute("SELECT * FROM belka")
all_users = cursor.fetchall()
print("Все пользователи:", all_users)


#Экспорт данных в csv
def export_users_to_csv(filename):
    cursor.execute("SELECT * FROM belka")
    users = cursor.fetchall()
    
    with open(filename, 'w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['id', 'name', 'email', 'age', 'created_at'])
        writer.writerows(users)


#export_users_to_csv('users_export.csv')

#export_to_json()

#import_from_json('users.json')

