import sqlite3


class DB:
    def __init__(self):
        conn = sqlite3.connect('market.db', check_same_thread=False)
        self.conn = conn

    def get_connection(self):
        return self.conn

    def __del__(self):
        self.conn.close()


class UserModel:
    def __init__(self, connection):
        self.connection = connection

    def init_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                            (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                             user_name VARCHAR(50),
                             password_hash VARCHAR(128)
                             )''')
        cursor.close()
        self.connection.commit()

    def insert(self, user_name, password_hash):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO users 
                          (user_name, password_hash) 
                          VALUES (?,?)''', (user_name, password_hash))
        cursor.close()
        self.connection.commit()

    def exists(self, user_name, password_hash):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE user_name = ? AND password_hash = ?",
                       (user_name, password_hash))
        row = cursor.fetchone()
        return (True, row[0]) if row else (False,)

    def user_exists(self, user_name):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE user_name = ?", (user_name, ))
        row = cursor.fetchone()
        return (True, row[0]) if row else (False,)


class ProductModel:
    def __init__(self, connection):
        self.connection = connection

    def init_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS products 
                            (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                             name VARCHAR(100),
                             count INTEGER,
                             price INTEGER,
                             reserv INTEGER
                             )''')
        cursor.close()
        self.connection.commit()

    def insert(self, name, count, price, reserv):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO products 
                          (name, count, price, reserv) 
                          VALUES (?,?,?,?)''', (name, count, price, reserv))
        cursor.close()
        self.connection.commit()

    def get(self, product_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM products WHERE id = ?", (str(product_id),))
        row = cursor.fetchone()
        return row

    def get_all(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM products")
        rows = cursor.fetchall()
        return rows

    def delete(self, product_id):
        cursor = self.connection.cursor()
        cursor.execute('''DELETE FROM products WHERE id = ?''', (str(product_id),))
        cursor.close()
        self.connection.commit()


class CartsModel:
    def __init__(self, connection):
        self.connection = connection

    def init_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS carts 
                            (user_id INTEGER, 
                             product_id INTEGER,
                             count INTEGER,
                             price INTEGER,
                             total INTEGER
                             )''')
        cursor.close()
        self.connection.commit()

    def insert(self, user_id, product_id, count, price, total):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO carts 
                                  (user_id, product_id, count, price, total) 
                                  VALUES (?,?,?,?)''', (user_id, product_id, count, price, total))
        cursor.close()
        self.connection.commit()

    def get(self, user_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM carts WHERE id = ?", (str(user_id),))
        row = cursor.fetchone()
        return row

    def delete(self, user_id):
        cursor = self.connection.cursor()
        cursor.execute('''DELETE FROM carts WHERE id = ?''', (str(user_id),))
        cursor.close()
        self.connection.commit()
