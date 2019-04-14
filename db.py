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
                             password_hash VARCHAR(128),
                             admin INTEGER
                             )''')
        cursor.close()
        self.connection.commit()

    def insert(self, user_name, password_hash, admin):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO users 
                          (user_name, password_hash, admin) 
                          VALUES (?,?,?)''', (user_name, password_hash, admin))
        cursor.close()
        self.connection.commit()

    def exists(self, user_name, password_hash):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE user_name = ? AND password_hash = ?",
                       (user_name, password_hash))
        row = cursor.fetchone()
        return (True, row[0]) if row else (False,)

    def get(self, user_name):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE user_name = ?", (user_name,))
        row = cursor.fetchone()
        return row

    def user_exists(self, user_name):
        row = self.get(user_name)
        return (True, row[0]) if row else (False,)

    def is_admin(self, user_name):
        item = self.get(user_name)
        return bool(item[-1])

    def delete_table(self):
        cursor = self.connection.cursor()
        cursor.execute('DROP TABLE users')


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
        cursor.execute('''SELECT * FROM products WHERE id = ?''', (str(product_id),))
        row = cursor.fetchone()
        return row

    def get_all(self):
        cursor = self.connection.cursor()
        cursor.execute('''SELECT * FROM products''')
        rows = cursor.fetchall()
        return rows

    def delete(self, product_id):
        cursor = self.connection.cursor()
        cursor.execute('''DELETE FROM products WHERE id = ?''', (str(product_id),))
        cursor.close()
        self.connection.commit()

    def change_reserv(self, product_id, c):
        cursor = self.connection.cursor()
        if c > 0:
            cursor.execute('''UPDATE products SET reserv = reserv + ? WHERE id = ?''', (c, str(product_id)))
        else:
            cursor.execute('''UPDATE products SET reserv = reserv - ? WHERE id = ?''', (abs(c), str(product_id)))
        cursor.close()
        self.connection.commit()

    def change_count(self, product_id, c):
        cursor = self.connection.cursor()
        if c > 0:
            cursor.execute('''UPDATE products SET count = count + ? WHERE id = ?''', (c, str(product_id)))
        else:
            cursor.execute('''UPDATE products SET count = count - ? WHERE id = ?''', (abs(c), str(product_id)))
        cursor.close()
        self.connection.commit()

    def reserv(self, product_id):
        cursor = self.connection.cursor()
        cursor.execute('''UPDATE products SET reserv = 0 WHERE id = ?''', (str(product_id),))
        cursor.close()
        self.connection.commit()

    def buy(self, product_id, reserv):
        cursor = self.connection.cursor()
        cursor.execute('''UPDATE products SET count = count - ? WHERE id = ?''', (reserv, str(product_id)))
        cursor.close()
        self.connection.commit()

    def check_reserv(self, product_id):
        item = self.get(product_id)
        return item[2] >= item[4] + 1


class CartsModel:
    def __init__(self, connection):
        self.connection = connection

    def init_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS carts 
                            (id INTEGER PRIMARY KEY AUTOINCREMENT,
                             user_id INTEGER, 
                             product_id INTEGER,
                             product_name VARCHAR(128),
                             count INTEGER,
                             price INTEGER,
                             total INTEGER
                             )''')
        cursor.close()
        self.connection.commit()

    def insert(self, user_id, product_id, product_name, count, price, total):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO carts 
                                  (user_id, product_id, product_name, count, price, total) 
                                  VALUES (?,?,?,?,?,?)''', (user_id, product_id, product_name, count, price, total))
        cursor.close()
        self.connection.commit()

    def get(self, user_id):
        cursor = self.connection.cursor()
        cursor.execute('''SELECT * FROM carts WHERE user_id = ?''', (str(user_id),))
        row = cursor.fetchall()
        return row

    def get_all(self):
        cursor = self.connection.cursor()
        cursor.execute('''SELECT * FROM carts''')
        rows = cursor.fetchall()
        return rows

    def get_by_id(self, cart_id):
        cursor = self.connection.cursor()
        cursor.execute('''SELECT * FROM carts WHERE id = ?''', (str(cart_id),))
        row = cursor.fetchall()
        return row

    def delete(self, user_id):
        cursor = self.connection.cursor()
        cursor.execute('''DELETE FROM carts WHERE user_id = ?''', (str(user_id),))
        cursor.close()
        self.connection.commit()

    def delete_from_carts(self, carts_id):
        cursor = self.connection.cursor()
        cursor.execute('''DELETE FROM carts WHERE id = ?''', (str(carts_id),))
        cursor.close()
        self.connection.commit()

    def delete_by_product(self, product_id):
        cursor = self.connection.cursor()
        cursor.execute('''DELETE FROM carts WHERE product_id = ?''', (str(product_id),))
        cursor.close()
        self.connection.commit()

    def get_products(self, user_id):
        cursor = self.connection.cursor()
        cursor.execute('''SELECT * FROM carts WHERE user_id = ?''', (str(user_id),))
        row = cursor.fetchall()
        m = []
        for i in row:
            m.append(i[2])
        return m

    def exists(self, user_id, product_id):
        cursor = self.connection.cursor()
        cursor.execute('''SELECT * FROM carts WHERE user_id = ? AND product_id = ?''',
                       (user_id, product_id))
        row = cursor.fetchone()
        return True if row else False

    def change_reserv(self, product_id, c, user_id):
        cursor = self.connection.cursor()
        if c > 0:
            cursor.execute('''UPDATE carts SET count = count + ? WHERE product_id = ? AND user_id = ?''',
                           (c, str(product_id), user_id))
        else:
            cursor.execute('''UPDATE carts SET count = count - ? WHERE product_id = ? AND user_id = ?''',
                           (abs(c), str(product_id), user_id))
        cursor.close()
        self.connection.commit()
