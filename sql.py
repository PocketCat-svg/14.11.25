import sqlite3
import csv
import json
import os

class SQLiteManager:
    def __init__(self, db_name='database.db'):
        self.db_name = db_name
        self.connection = None
        
    def connect(self):
        """Установка соединения с базой данных"""
        try:
            self.connection = sqlite3.connect(self.db_name)
            self.connection.row_factory = sqlite3.Row  # Для доступа к колонкам по имени
            print(f"Подключение к базе данных {self.db_name} установлено")
            return True
        except sqlite3.Error as e:
            print(f"Ошибка подключения: {e}")
            return False
    
    def create_tables(self):
        """Создание таблиц в базе данных"""
        try:
            cursor = self.connection.cursor()
            
            # Создание таблицы пользователей
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    age INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            
            self.connection.commit()
            print("Таблицы успешно созданы")
        except sqlite3.Error as e:
            print(f"Ошибка создания таблиц: {e}")




class UserCRUD:
    def __init__(self, db_manager):
        self.db = db_manager
    
    # CREATE операции
    def create_user(self, name, last_name, age=None):
        """Создание нового пользователя"""
        try:
            cursor = self.db.connection.cursor()
            cursor.execute(
                "INSERT INTO users (name, last_name, age) VALUES (?, ?, ?)",
                (name, last_name, age)
            )
            self.db.connection.commit()
            print(f"Пользователь {name} успешно создан с ID: {cursor.lastrowid}")
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            print(f"Пользователь с last_name {last_name} уже существует")
            return None
        

    def get_all_users(self):
        """Получение всех пользователей"""
        cursor = self.db.connection.cursor()
        cursor.execute("SELECT * FROM users")
        return cursor.fetchall()
    
    def get_user_by_id(self, user_id):
        """Получение пользователя по ID"""
        cursor = self.db.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        return cursor.fetchone()
    
    def get_user_by_last_name(self, last_name):
        """Получение пользователя по last_name"""
        cursor = self.db.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE last_name = ?", (last_name,))
        return cursor.fetchone()    


    def update_user(self, user_id, name=None, last_name=None, age=None):
        """Обновление данных пользователя"""
        try:
            cursor = self.db.connection.cursor()
            
            updates = []
            params = []
            
            if name:
                updates.append("name = ?")
                params.append(name)
            if last_name:
                updates.append("last_name = ?")
                params.append(last_name)
            if age is not None:
                updates.append("age = ?")
                params.append(age)
            
            if not updates:
                print("Нет данных для обновления")
                return False
            
            params.append(user_id)
            query = f"UPDATE users SET {', '.join(updates)} WHERE id = ?"
            
            cursor.execute(query, params)
            self.db.connection.commit()
            
            if cursor.rowcount > 0:
                print(f"Пользователь с ID {user_id} успешно обновлен")
                return True
            else:
                print(f"Пользователь с ID {user_id} не найден")
                return False
                
        except sqlite3.Error as e:
            print(f"Ошибка обновления: {e}")
            return False
    
    # DELETE операции
    def delete_user(self, user_id):
        """Удаление пользователя"""
        try:
            cursor = self.db.connection.cursor()
                     
            # Затем удаляем пользователя
            cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
            self.db.connection.commit()
            
            if cursor.rowcount > 0:
                print(f"Пользователь с ID {user_id} успешно удален")
                return True
            else:
                print(f"Пользователь с ID {user_id} не найден")
                return False
                
        except sqlite3.Error as e:
            print(f"Ошибка удаления: {e}")
            return False

class DataFileManager:
    def __init__(self, db_manager):
        self.db = db_manager
    
    def export_users_to_csv(self, filename='users_export.csv'):
        """Экспорт пользователей в CSV файл"""
        try:
            cursor = self.db.connection.cursor()
            cursor.execute("SELECT * FROM users")
            users = cursor.fetchall()
            
            with open(filename, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                # Записываем заголовки
                writer.writerow(['id', 'name', 'last_name', 'age', 'created_at'])
                # Записываем данные
                for user in users:
                    writer.writerow([user['id'], user['name'], user['last_name'], 
                                   user['age'], user['created_at']])
            
            print(f"Данные экспортированы в {filename}")
            return True
        except Exception as e:
            print(f"Ошибка экспорта в CSV: {e}")
            return False
    
    def import_users_from_csv(self, filename):
        """Импорт пользователей из CSV файла"""
        try:
            if not os.path.exists(filename):
                print(f"Файл {filename} не найден")
                return False
            
            cursor = self.db.connection.cursor()
            imported_count = 0
            
            with open(filename, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    try:
                        cursor.execute(
                            """INSERT OR IGNORE INTO users 
                               (name, last_name, age) VALUES (?, ?, ?)""",
                            (row['name'], row['last_name'], row['age'])
                        )
                        imported_count += 1
                    except sqlite3.Error as e:
                        print(f"Ошибка импорта пользователя {row['name']}: {e}")
            
            self.db.connection.commit()
            print(f"Импортировано {imported_count} пользователей из {filename}")
            return True
        except Exception as e:
            print(f"Ошибка импорта из CSV: {e}")
            return False
    
    def export_users_to_json(self, filename='users_export.json'):
        """Экспорт пользователей в JSON файл"""
        try:
            cursor = self.db.connection.cursor()
            cursor.execute("SELECT * FROM users")
            users = cursor.fetchall()
            
            users_list = []
            for user in users:
                users_list.append({
                    'id': user['id'],
                    'name': user['name'],
                    'last_name': user['last_name'],
                    'age': user['age'],
                    'created_at': user['created_at']
                })
            
            with open(filename, 'w', encoding='utf-8') as file:
                json.dump(users_list, file, indent=2, ensure_ascii=False)
            
            print(f"Данные экспортированы в {filename}")
            return True
        except Exception as e:
            print(f"Ошибка экспорта в JSON: {e}")
            return False
    
    def import_users_from_json(self, filename):
        """Импорт пользователей из JSON файла"""
        try:
            if not os.path.exists(filename):
                print(f"Файл {filename} не найден")
                return False
            
            with open(filename, 'r', encoding='utf-8') as file:
                users_data = json.load(file)
            
            cursor = self.db.connection.cursor()
            imported_count = 0
            
            for user_data in users_data:
                try:
                    cursor.execute(
                        """INSERT OR IGNORE INTO users 
                           (name, last_name, age) VALUES (?, ?, ?)""",
                        (user_data['name'], user_data['last_name'], user_data.get('age'))
                    )
                    imported_count += 1
                except sqlite3.Error as e:
                    print(f"Ошибка импорта пользователя {user_data['name']}: {e}")
            
            self.db.connection.commit()
            print(f"Импортировано {imported_count} пользователей из {filename}")
            return True
        except Exception as e:
            print(f"Ошибка импорта из JSON: {e}")
            return False

def json_create(filename):
    users_list = []
    continues = True
    while continues: 
        users_list.append({
           'name':  input('введите имя '),
           'last_name': input('введите фамилию '),
           'age': input('введите возраст '),
                             })
        continues = input('продолжить? ')
            
    with open(filename, 'w', encoding='utf-8') as file:
       json.dump(users_list, file, indent=2, ensure_ascii=False)



manager = SQLiteManager('database2.db')
manager.connect()
manager.create_tables()
CRUID = UserCRUD(manager)
CRUID.create_user('Alex', "logvinov", 29)
CRUID.delete_user(6)
json_create('spisok.json')
datam = DataFileManager(manager)
datam.import_users_from_json("spisok.json")