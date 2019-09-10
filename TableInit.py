from peewee import SqliteDatabase
from Models import RealtyItem

db = SqliteDatabase('database.db')
db.drop_tables([RealtyItem])
db.create_tables([RealtyItem])
