import peewee

from settings import DATABASE as db


class Client(peewee.Model):
    name = peewee.CharField()
    slug = peewee.CharField()

    class Meta:
        database = db


class TimeCard(peewee.Model):
    date = peewee.DateField()
    start = peewee.TimeField()
    end = peewee.TimeField()
    client = peewee.ForeignKeyField(Client, related_name='timecards')

    class Meta:
        database = db
