import sqlite3

def create_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT NOT NULL UNIQUE,
                        password TEXT NOT NULL,
                        role TEXT NOT NULL,
                        email TEXT NOT NULL)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS products (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        quantity INTEGER NOT NULL,
                        location TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS transactions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        product_id INTEGER NOT NULL,
                        quantity_change INTEGER NOT NULL,
                        date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (product_id) REFERENCES products (id))''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS password_reset (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER NOT NULL,
                        reset_code TEXT NOT NULL,
                        request_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users(id))''')
    conn.commit()
    conn.close()

def add_user(username, password, role, email):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # Проверка, существует ли уже пользователь с таким именем
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    existing_user = cursor.fetchone()

    if existing_user:
        print(f"Пользователь с именем {username} уже существует.")
        conn.close()
        return False  # Возвращаем False, если пользователь уже существует
    else:
        # Если пользователя нет, добавляем нового
        cursor.execute("INSERT INTO users (username, password, role, email) VALUES (?, ?, ?, ?)",
                       (username, password, role, email))
        conn.commit()
        conn.close()
        print(f"Пользователь {username} добавлен успешно.")
        return True  # Возвращаем True при успешной вставке

def add_product(name, quantity, price):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO products (name, quantity, price) VALUES (?, ?, ?)", (name, quantity, price))
    conn.commit()
    conn.close()

def update_product(product_id, new_quantity):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE products SET quantity = ? WHERE id = ?", (new_quantity, product_id))
    cursor.execute("INSERT INTO transactions (product_id, quantity_change) VALUES (?, ?)", (product_id, new_quantity))
    conn.commit()
    conn.close()


def update_user(product_id, new_quantity):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET password = ? WHERE id = ?", (new_quantity, product_id))
    cursor.execute("INSERT INTO transactions (product_id, quantity_change) VALUES (?, ?)", (product_id, new_quantity))
    conn.commit()
    conn.close()
def get_all_products():
    """Возвращает список всех продуктов из базы данных"""
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM products")  # Запрос всех продуктов
    products = cursor.fetchall()
    connection.close()
    return products
def get_all_users():
    """Возвращает список всех продуктов из базы данных"""
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users")  # Запрос всех продуктов
    users = cursor.fetchall()
    connection.close()
    return users

def get_product_by_id(product_id):
    """Возвращает данные о продукте по его ID"""
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
    product = cursor.fetchone()
    connection.close()
    return product


def get_user_by_id(product_id):
    """Возвращает данные о продукте по его ID"""
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (product_id,))
    product = cursor.fetchone()
    connection.close()
    return product

def get_table_data(table_name):
    """Возвращает данные из выбранной таблицы"""
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    try:
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = [column[1] for column in cursor.fetchall()]

        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
    except sqlite3.OperationalError as e:
        columns = []
        rows = []
        print(f"Ошибка при загрузке таблицы {table_name}: {e}")
    finally:
        conn.close()

    return {"columns": columns, "rows": rows}



def check_credentials(username, password):
    """Проверка учетных данных пользователя в базе данных."""
    conn = sqlite3.connect('database.db')  # Подключение к базе данных
    cursor = conn.cursor()

    # SQL-запрос для поиска пользователя с введенными данными
    query = "SELECT * FROM users WHERE username=? AND password=?"
    cursor.execute(query, (username, password))
    result = cursor.fetchone()

    conn.close()

    if result:  # Если результат найден, то возвращаем True
        return True
    else:
        return False

def check_role(username):
    """Проверка учетных данных пользователя в базе данных."""
    conn = sqlite3.connect('database.db')  # Подключение к базе данных
    cursor = conn.cursor()

    # SQL-запрос для поиска пользователя с введенными данными
    query = "SELECT role FROM users WHERE username=?"
    cursor.execute(query, (username,))
    result = cursor.fetchone()

    conn.close()

    if result:  # Если результат найден, то возвращаем True
        return result[0]
    else:
        return None

def save_user_to_db(username, password, role, email):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # SQL-запрос для добавления нового пользователя
    query = "INSERT INTO users (username, password, role, email) VALUES (?, ?, ?, ?)"
    try:
        cursor.execute(query, (username, password, role, email))
        conn.commit()
        print(f"Пользователь {username} успешно добавлен.")
    except sqlite3.IntegrityError as e:
        print(f"Ошибка добавления пользователя: {e}")
    finally:
        conn.close()

def reset_user_password(email):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()

    if user:
        reset_code = "123456"  # Генерация кода для сброса (можно заменить на более сложную логику)
        cursor.execute("INSERT INTO password_reset (user_id, reset_code) VALUES (?, ?)", (user[0], reset_code))
        conn.commit()
        conn.close()
        return True
    else:
        conn.close()
        return False

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random


def generate_random_six_digit_number():
    return random.randint(100000, 999999)

def send_reset_code(email, reset_code):
    sender_email = "cnaq@yandex.ru"
    sender_password = "xamwhgcjiyjoeaeb"
    subject = "Восстановление пароля"
    body = f"Ваш код для восстановления пароля: {reset_code}"

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Используем порт 465 с SSL
        server = smtplib.SMTP_SSL('smtp.yandex.ru', 465)
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, email, text)
        server.quit()
        return True
    except Exception as e:
        print(f"Ошибка при отправке письма: {e}")
        return False


def reset_user_password(email):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()

    if user:
        reset_code = generate_random_six_digit_number() # Генерация кода для сброса (можно заменить на более сложную логику)
        cursor.execute("INSERT INTO password_reset (user_id, reset_code) VALUES (?, ?)", (user[0], reset_code))
        conn.commit()
        conn.close()
        send_reset_code(email, reset_code)
        return True
    else:
        conn.close()
        return False
def confirm_password_reset(code, new_password):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM password_reset WHERE reset_code = ?", (code,))
    result = cursor.fetchone()

    if result:
        user_id = result[0]
        cursor.execute("UPDATE users SET password = ? WHERE id = ?", (new_password, user_id))
        cursor.execute("DELETE FROM password_reset WHERE reset_code = ?", (code,))
        conn.commit()
        conn.close()
        return True
    else:
        conn.close()
        return False
