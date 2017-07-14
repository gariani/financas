from basemodel import BaseModel
from peewee import CharField, BigIntegerField, FloatField


class Gasto(BaseModel):
    id = BigIntegerField(primary_key=True)
    descricao_previsto = CharField()
    total_realizado = FloatField()
    valor_previsto = FloatField()
    saldo = FloatField()

    class Meta:
        order_by = ('id',)
