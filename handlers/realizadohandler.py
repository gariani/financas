import json
from tornado import escape
from playhouse.shortcuts import model_to_dict
from model.gastomodel import Gasto
from model.realizadomodel import Realizado
from handlers.mainhandler import MainHandler


class RealizadoHandler(MainHandler):

    def selecionar_gasto(self, id_gasto):
        return Gasto.select().where(Gasto.id == id_gasto)

    def salvar_dados(self, dados):

        if not 'gasto_id' in dados:
            raise Exception("informe o gasto correspondente")

        gasto = self.selecionar_gasto(dados['gasto_id'])
        realizado = Realizado.create(descricao=dados['descricao'],
                                     valor=dados['valor'],
                                     gasto=gasto)
        return realizado

    def post(self, instancia_id: str = None):

        try:
            if instancia_id:
                if self.request.body:
                    dados_json = escape.json_decode(self.request.body)
                    realizado = self.salvar_dados(dados_json)
                    self.write(json.dumps(model_to_dict(realizado)))
        except Exception as e:
            self.falha(str(e))

    def get(self, instancia_id: str = None, instancia_id2: str = None):

        try:
            if instancia_id:
                if instancia_id2:
                    retorno_realizado = (Realizado
                                         .select(Realizado.id, Realizado.descricao, Realizado.valor)
                                         .where((Realizado.gasto_id == instancia_id),
                                                (Realizado.id == instancia_id2)).get())
                    print(retorno_realizado._data)
                    json_retorno = model_to_dict(retorno_realizado)

                else:
                    json_retorno = (Realizado
                                    .select(Realizado.id, Realizado.descricao, Realizado.valor)
                                    .join(Gasto)
                                    .where(Gasto.id == instancia_id))
                    retorno_realizado = []
                    for i in json_retorno:
                        retorno_realizado.append(model_to_dict(i))

                    json_retorno = json.dumps(retorno_realizado)
                    print(json_retorno)

            else:
                retorno_realizado = (Realizado.select())
                dic = []
                print('teste')
                for i in retorno_realizado:
                    dic.append(model_to_dict(i))
                json_retorno = json.dumps(dic)

            self.sucesso(json_retorno)
        except Realizado.DoesNotExist:
            self.falha('Nao foi encontrado o valor correspondente.')
        except Exception as e:
            self.falha(str(e))
