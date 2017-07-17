from peewee import BigIntegerField, CharField, FloatField, PrimaryKeyField, ForeignKeyField
from model.basemodel import BaseModel
from model.gastomodel import Gasto


class Realizado(BaseModel):
    id = PrimaryKeyField(null=False)
    descricao = CharField()
    valor = FloatField()
    gasto = ForeignKeyField(Gasto, related_name='gastos')

    class Main:
        order_by = ('id',)
        db_table = 'realizado'
