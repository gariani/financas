from tornado import escape
from tornado.web import HTTPError
import json
from playhouse.shortcuts import model_to_dict
from handlers.mainhandler import MainHandler
from model.gastomodel import Gasto


class GastoHandler(MainHandler):
    def salvarDados(self, dados):
        return Gasto.create(descricao_previsto=dados['descricao_previsto'],
                            valor_previsto=dados['valor_previsto'],
                            total_realizado=dados['total_realizado'],
                            saldo=dados['saldo'])

    def post(self):

        if not self.valid_arguments():
            raise HTTPError("Argumentos invalidos")

        try:
            if self.request.body:
                data_json = escape.json_decode(self.request.body)
                gasto = self.salvarDados(data_json)
                self.write(json.dumps(model_to_dict(gasto)))
            else:
                self.write('vazio')

        except Exception as e:
            self.falha(e.__str__())

    def get(self, instancia_id: str = None):

        if not self.valid_arguments():
            raise HTTPError("Argumentos invalidos")

        try:
            if instancia_id:
                retorno_gasto = (Gasto
                                 .select()
                                 .where(Gasto.id == instancia_id).dicts().get())

            else:
                retorno_gasto = []
                for i in Gasto.select().order_by(Gasto.id):
                    retorno_gasto.append(i._data)

            json_retorno = json.dumps(retorno_gasto)
            self.sucesso(json_retorno)
        except Gasto.DoesNotExist:
            self.falha('Nao foi encontrado o valor correspondente')
        except Exception as e:
            self.falha(str(e))
