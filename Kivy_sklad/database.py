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


def register_user(username, password, role, email):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # Проверка, существует ли пользователь с таким именем
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()

    if user:
        print("Пользователь с таким именем уже существует. Выберите другое имя.")
        conn.close()
        return False
    else:
        # Добавление пользователя, если такого имени еще нет
        cursor.execute("INSERT INTO users (username, password, role, email) VALUES (?, ?, ?, ?)",
                       (username, password, role, email))
        conn.commit()
        conn.close()
        return True

def add_product(name, quantity, location):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO products (name, quantity, location) VALUES (?, ?, ?)", (name, quantity, location))
    conn.commit()
    conn.close()

def update_product(product_id, quantity_change):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE products SET quantity = quantity + ? WHERE id = ?", (quantity_change, product_id))
    cursor.execute("INSERT INTO transactions (product_id, quantity_change) VALUES (?, ?)", (product_id, quantity_change))
    conn.commit()
    conn.close()

def get_product(product_id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
    product = cursor.fetchone()
    conn.close()
    return product

def get_transactions(product_id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM transactions WHERE product_id = ?", (product_id,))
    transactions = cursor.fetchall()
    conn.close()
    return transactions

def get_all_products():
    """Возвращает список всех продуктов из базы данных"""
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM products")  # Запрос всех продуктов
    products = cursor.fetchall()
    connection.close()
    return products

def get_product_by_id(product_id):
    """Возвращает данные о продукте по его ID"""
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
    product = cursor.fetchone()
    connection.close()
    return product


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

def save_user_to_db(username, password):
    """Сохранение нового пользователя в базе данных."""
    conn = sqlite3.connect('database.db')  # Подключение к базе данных
    cursor = conn.cursor()

    # SQL-запрос для добавления нового пользователя
    query = "INSERT INTO users (username, password) VALUES (?, ?)"
    cursor.execute(query, (username, password))
    conn.commit()
    conn.close()

