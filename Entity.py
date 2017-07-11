import json
from Conexao import *


class Entity(object):
    def __init__(self, table_name, columns, query_all, query_count):
        self._table_name: str = table_name
        self._columns: str = columns
        self._query_all: str = query_all
        self._query_count: str = query_count
        self.__conn: Conexao = None

    @property
    def conn(self):
        if not self.__conn:
            self.__conn = Conexao()
            return self.__conn.conn
        else:
            return self.__conn.conn

    def formatar(self, chaves, valores):
        _results = []
        for row in valores:
            _results.append(dict(zip(chaves, row)))
        return json.dumps(_results)

    def count(self):
        _valor = self.conn.fetchone(self._query_count)
        return self.formatar(('total'), _valor)

    def fetchall(self):
        _valores = self.conn.fetchall(self._query_all)
        return self.formatar(self._columns, _valores)

    def fetchone(self, id):
        _valores = []
        _valor = self.conn.fetchone("""SELECT {} FROM {} WHERE id={}"""
                                    .format(','.join(str(s) for s in self._columns), self._table_name,
                                            id))
        if _valor is not None:
            _valores.append(_valor)
            return self.formatar(self._columns, _valores)
        else:
            return self.formatar(['Error'], [('Nao foi encontrado o valor correspondente',)])
