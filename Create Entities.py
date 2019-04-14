from db import DB, UserModel, ProductModel, CartsModel

db = DB()

UserModel(db.get_connection()).init_table()
UserModel(db.get_connection()).insert("user1", "password1", 0)
UserModel(db.get_connection()).insert("user2", "password2", 0)
UserModel(db.get_connection()).insert("admin", "admin", 1)

ProductModel(db.get_connection()).init_table()
ProductModel(db.get_connection()).insert("Карандаш", 5, 10, 0)
ProductModel(db.get_connection()).insert("Ножницы", 10, 150, 0)
ProductModel(db.get_connection()).insert("Ластик", 20, 15, 0)

CartsModel(db.get_connection()).init_table()
