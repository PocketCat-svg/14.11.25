import sqlite3

# Создание/подключение к БД
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Включение поддержки внешних ключей
cursor.execute("PRAGMA foreign_keys = ON")

# Создание таблицы пользователей
cursor.execute('''
CREATE TABLE IF NOT EXISTS belka (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    age INTEGER,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
)
''')

conn.commit()