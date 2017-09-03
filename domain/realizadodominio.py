import json

from model.gastomodel import Gasto
from model.realizadomodel import Realizado
from playhouse.shortcuts import model_to_dict


class RealizadoDominio:
    def selecionar_gasto(self, id_gasto):
        gasto = Gasto.select().where(Gasto.id == id_gasto)
        if not gasto:
            raise Exception('gasto nao encontrado')
        return gasto

    def salvar_realizado(self, gasto, dados):
        return Realizado.create(descricao=dados['descricao'],
                                valor=dados['valor'],
                                gasto=gasto)

    def salvar_dados(self, id_gasto, dados):

        if not id_gasto:
            raise Exception("informe o gasto correspondente")
        gasto = self.selecionar_gasto(id_gasto)
        dados_json = json.loads(dados)
        retorno = self.salvar_realizado(gasto, dados_json)
        return json.dumps(model_to_dict(retorno))

    def realizado(self, id_gasto, id_retorno):
        retorno_realizado = (Realizado
                             .select(Realizado.id, Realizado.descricao, Realizado.valor)
                             .where((Realizado.gasto_id == id_gasto),
                                    (Realizado.id == id_retorno)).get())
        return model_to_dict(retorno_realizado)

    def lista_realizado(self, id_gasto):
        json_retorno = (Realizado
                        .select(Realizado.id, Realizado.descricao, Realizado.valor)
                        .join(Gasto)
                        .where(Gasto.id == id_gasto))
        retorno_realizado = []
        for i in json_retorno:
            retorno_realizado.append(model_to_dict(i))
        return json.dumps(retorno_realizado)
