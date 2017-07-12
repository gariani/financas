from Entity import *


class Gasto(Entity):
    def __init__(self):
        self._table_name = "gasto"
        self._columns = ('id', 'descricao_previsto', 'valor_previsto', 'total_realizado', 'saldo')
        self._query_all = """SELECT id, descricao_previsto, valor_previsto, total_realizado, saldo FROM gasto"""
        self._query_count = """SELECT COUNT(*) FROM gasto"""
        Entity.__init__(self, self._table_name, self._columns, self._query_all, self._query_count)
