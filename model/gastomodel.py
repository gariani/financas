from peewee import CharField, FloatField, DateField, PrimaryKeyField, ForeignKeyField
from model.basemodel import BaseModel


class Gasto(BaseModel):
    id = PrimaryKeyField(null=False)
    descricao_previsto = CharField()
    valor_previsto = FloatField()
    total_realizado = FloatField()
    saldo = FloatField()
    created_at = DateField(null=True)

    class Meta:
        order_by = ('id',)
        db_table = 'gasto'
