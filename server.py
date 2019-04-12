from flask import Flask, render_template, redirect
from forms import LoginForm
import sqlite3
import os

app = Flask(__name__)


# class DB:
#     def __init__(self, db_file):
#         conn = sqlite3.connect(db_file, check_same_thread=False)
#         self.conn = conn
#
#     def get_connection(self):
#         return self.conn
#
#     def __del__(self):
#         self.conn.close()
#
#
# class UsersDB(DB):
#     def __init__(self):
#         super().__init__('databases/users_db_db')
#
#     def init_table(self):
#         cursor = self.conn.cursor()
#         cursor.execute('''CREATE TABLE IF NOT EXISTS users
#                             (id INTEGER PRIMARY KEY AUTOINCREMENT,
#                              user_name VARCHAR(50),
#                              password_hash VARCHAR(128)
#                              )''')
#         cursor.close()
#         self.conn.commit()
#
#     def insert(self, user_name, password_hash):
#         cursor = self.conn.cursor()
#         cursor.execute('''INSERT INTO users
#                           (user_name, password_hash)
#                           VALUES (?,?)''', (user_name, password_hash))
#         cursor.close()
#         self.conn.commit()
#
#     def get(self, user_id):
#         cursor = self.conn.cursor()
#         cursor.execute("SELECT * FROM users WHERE id = ?", (str(user_id)))
#         row = cursor.fetchone()
#         return row
#
#     def get_all(self):
#         cursor = self.conn.cursor()
#         cursor.execute("SELECT * FROM users")
#         rows = cursor.fetchall()
#         return rows
#
#
# class ItemsDB(DB):
#     def __init__(self):
#         super().__init__('databases/items_db_db')
#
#     def init_table(self):
#         cursor = self.conn.cursor()
#         cursor.execute('''CREATE TABLE IF NOT EXISTS items
#                             (id INTEGER PRIMARY KEY AUTOINCREMENT,
#                              name VARCHAR(100),
#                              content VARCHAR(1000),
#                              item_id INTEGER,
#                              cost INTEGER
#                              )''')
#         cursor.close()
#         self.conn.commit()
#
#     def insert(self, name, content, item_id, cost):
#         cursor = self.conn.cursor()
#         cursor.execute('''INSERT INTO items
#                           (title, content, user_id)
#                           VALUES (?,?,?,?)''', (name, content, str(item_id), str(cost)))
#         cursor.close()
#         self.conn.commit()
#
#     def get(self, news_id):
#         cursor = self.conn.cursor()
#         cursor.execute("SELECT * FROM items WHERE id = ?", (str(news_id)))
#         row = cursor.fetchone()
#         return row
#
#     def get_all(self, user_id=None):
#         cursor = self.conn.cursor()
#         if user_id:
#             cursor.execute("SELECT * FROM items WHERE user_id = ?",
#                            (str(user_id)))
#         else:
#             cursor.execute("SELECT * FROM items")
#         rows = cursor.fetchall()
#         return rows
#
#     def delete(self, news_id):
#         cursor = self.conn.cursor()
#         cursor.execute('''DELETE FROM items WHERE id = ?''', (str(news_id)))
#         cursor.close()
#         self.conn.commit()


@app.route('/', methods=['POST', 'GET'])
def main():
    # return render_template('index.html', username='JHBVkg', product=[['a', 'b', 'c']])
    pass


@app.route('/<int:user_id>', methods=['POST', 'GET'])
def basket(user_id):
    # return render_template('basket.html', )
    pass


@app.route('/add_to_basket/<int:item_id>', methods=['POST', 'GET'])
def add_to_basket(item_id):
    pass


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect('/index')
    return render_template('login.html', title='Singing in', form=form)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
