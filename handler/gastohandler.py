from tornado import escape
from domain.gastodominio import GastoDominio
from handler.mainhandler import MainHandler
from model.gastomodel import Gasto


class GastoHandler(MainHandler):
    gastoDominio = GastoDominio()

    def post(self):
        try:
            if self.request.body:
                data_json = escape.json_decode(self.request.body)
                retorno = self.gastoDominio.salvar_dados(self, data_json)
                self.sucesso(retorno)
            else:
                self.falha('nenhum dado informado')
        except Exception as e:
            self.falha(str(e))

    def get(self, instancia_id: str = None):
        try:
            if instancia_id:
                retorno_gasto = self.gastoDominio.retornar_gasto(self, instancia_id)
            else:
                retorno_gasto = self.gastoDominio.retornar_lista_gasto(self)
            self.sucesso(retorno_gasto)
        except Gasto.DoesNotExist:
            self.falha('Nao foi encontrado o valor correspondente')
        except Exception as e:
            self.falha(str(e))
