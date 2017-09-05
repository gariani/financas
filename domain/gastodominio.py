import json
from model.gastomodel import Gasto
from model.realizadomodel import Realizado
from playhouse.shortcuts import model_to_dict


class GastoDominio:
    def delete(self, id_gasto):
        realizado = Realizado.delete().where(Realizado.gasto_id == id_gasto)
        realizado.execute()
        retorno = Gasto.delete().where(Gasto.id == id_gasto)
        num = retorno.execute()
        return {'excluido': num}

    def retorna_novo_id(self):
        retorno = Gasto.create()
        return json.dumps(model_to_dict(retorno))

    def salvar_dados(self, dados):
        retorno = Gasto.create(descricao_previsto=dados['descricao_previsto'],
                               valor_previsto=dados['valor_previsto'],
                               total_realizado=dados['total_realizado'],
                               saldo=dados['saldo'])

        return json.dumps(model_to_dict(retorno))

    def retornar_gasto(self, instancia_id):
        gasto = (Gasto
                 .select()
                 .where(Gasto.id == instancia_id).dicts().get())

        return json.dumps(gasto)

    def retornar_lista_gasto(self):
        retorno_gasto = []
        for i in Gasto.select().order_by(Gasto.id):
            retorno_gasto.append(i._data)

        return json.dumps(retorno_gasto)

    def atualizar(self, id_gasto, dados):

        if 'descricao_previsto' in dados:
            query = Gasto.update(descricao_previsto=dados['descricao_previsto']) \
                .where(Gasto.id == id_gasto)
            query.execute()
        if 'valor_previsto' in dados:
            query = Gasto.update(valor_previsto=dados['valor_previsto']) \
                .where(Gasto.id == id_gasto)
            query.execute()
        if 'total_realizado' in dados:
            query = Gasto.update(total_realizado=dados['total_realizado']) \
                .where(Gasto.id == id_gasto)
            query.execute()
        if 'saldo' in dados:
            query = Gasto.update(saldo=dados['saldo']) \
                .where(Gasto.id == id_gasto)
            query.execute()
