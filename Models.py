import peewee

db = peewee.SqliteDatabase('database.db')


class BaseModel(peewee.Model):
    class Meta:
        database = db


class RealtyItem(BaseModel):
    apiId = peewee.CharField()
    originalId = peewee.CharField()
    origin = peewee.CharField()
    url = peewee.CharField()
    time_appeared = peewee.DateField()
    time_disappeared = peewee.DateField(null=True)

    last_update = peewee.DateField(null=True)

    title = peewee.CharField()
    price = peewee.IntegerField()
    phone = peewee.CharField(null=True)
    contact_person = peewee.CharField()
    contact_type = peewee.CharField()  # Частное лицо", "Агентство" или "Частное лицо (фильтр)"
    city = peewee.CharField()
    region = peewee.CharField()
    subway = peewee.CharField()
    address = peewee.CharField()
    description = peewee.CharField()
    record_type = peewee.CharField()  # Продам, Сдам, Куплю или Сниму
    images = peewee.CharField()
    params = peewee.CharField()