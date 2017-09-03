from peewee import Model

from connection import *


class BaseModel(Model):
    class Meta:
        database = db
