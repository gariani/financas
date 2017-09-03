import json

from model.gastomodel import Gasto
from playhouse.shortcuts import model_to_dict


class GastoDominio:
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
