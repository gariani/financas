from peewee import Model

from conn.connection \
    import db


class BaseModel(Model):
    class Meta:
        database = db
