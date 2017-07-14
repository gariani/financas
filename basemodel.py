from peewee import Model
from session import connection_pg


class BaseModel(Model):
    class Meta:
        database = connection_pg
