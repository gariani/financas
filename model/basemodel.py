from peewee import Model

from connection import db


class BaseModel(Model):
    class Meta:
        database = db
