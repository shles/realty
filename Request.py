import datetime
import time
import requests
from peewee import *
# from playhouse.postgres_ext import ArrayField
if __name__ == '__main__':

    db = SqliteDatabase('database.db')

    class BaseModel(Model):
        class Meta:
            database = db

    class RealtyItem(BaseModel):
        apiId = CharField()
        originalId = CharField()
        origin = CharField()
        url = CharField()
        time_appeared = DateField()
        time_disappeared = DateField(null=True)

        last_update = DateField(null=True)

        title = CharField()
        price = IntegerField()
        phone = CharField(null=True)
        contact_person = CharField()
        contact_type = CharField()  # Частное лицо", "Агентство" или "Частное лицо (фильтр)"
        city = CharField()
        region = CharField()
        subway = CharField()
        address = CharField()
        description = CharField()
        record_type = CharField()  # Продам, Сдам, Куплю или Сниму
        images = CharField()
        params = CharField()

        # room_count = IntegerField()
        # floor_number = IntegerField()
        # add other specific parameters

    def item_from_dict(dict):

        return RealtyItem.create(
            apiId=dict['id'],
            originalId=dict['avitoid'],
            origin=dict['source'],
            url=dict['url'],
            time_appeared=dict['time'],
            title=dict['title'],
            price=dict['price'],
            phone=dict['phone'],
            contact_person=dict['contactname'],
            contact_type=dict['person_type'],
            city =dict['city1'],
            region=dict['region'],
            subway=dict['metro'],
            address=dict['address'],
            description=dict['description'],
            record_type=dict['nedvigimost_type'],
            images=dict['images'],
            params=dict['params']
        )

    db.connect()
    # db.drop_tables([RealtyItem])
    # db.create_tables([RealtyItem])

    def update_base():
        current_time = datetime.datetime.now()
        not_loaded_all = True
        limit = 50

        start_id = ''

        while not_loaded_all:

            payload = {
                'user': 'temitrix@gmail.com',
                'token': '572333657467242b484974202551fe47',
                'limit': limit,
                'nedvigimost_type': '2',
                'category_id': '2',
                'city': 'Москва',
                'startid': start_id}

            r = requests.get('http://ads-api.ru/main/api', params=payload)
            print(r.url)
            print(r.status_code)
            # print(r.text)
            data = r.json()['data']

            for result in data:
                # print(result['id'])

                try:
                    item = RealtyItem.select().where(RealtyItem.origin == result['source'],
                                                     RealtyItem.originalId == result['avitoid']).get()
                except DoesNotExist:
                    item = item_from_dict(result)

                item.last_update = current_time

                item.save()

            not_loaded_all = (len(data) == limit)

            print('loaded', len(data))
            if not_loaded_all:
                start_id = data[len(data)-1]['id']
                time.sleep(5)

        print('disappeared at', current_time.strftime("%m/%d/%Y, %H:%M:%S"))
        for item in RealtyItem.select().where(
                (RealtyItem.last_update < current_time) & (RealtyItem.time_disappeared is None)):
            item.time_disappeared = current_time
            print('\t', item.id)


    # for item in RealtyItem.select():
    #     print(item.title)

    update_base()


#todo: make something ciclyc
#todo: write data to db
#todo: on each cycle compare is there each entry and if not place date of disappearing
#todo: decide what properties do I need
# To get all items it should iterate bu last id in 'if' field, until items count in response < 1000
# Alg:
# until lastResp.items.count < limit
#   getItemsFromAPI
#   update items.lastUpdated or add to db with current last update
# get items that hasn't been updated this time and add them date of disappearing
# repeat every hour
