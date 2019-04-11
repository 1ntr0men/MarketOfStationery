from db import DB, UserModel, ProductModel, CartsModel

db = DB()

UserModel(db.get_connection()).init_table()
UserModel(db.get_connection()).insert("user1", "password1")

ProductModel(db.get_connection()).init_table()
ProductModel(db.get_connection()).insert("Карандаш", 5, 10, 0)
ProductModel(db.get_connection()).insert("Ластик", 10, 15, 1)

CartsModel(db.get_connection()).init_table()
