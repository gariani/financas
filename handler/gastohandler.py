from tornado import escape
from psycopg2 import IntegrityError
from handler.mainhandler import MainHandler
from domain.gastodominio import GastoDominio


class GastoHandler(MainHandler):
    gasto_dominio = GastoDominio()

    def delete(self, instancia_id: str = None):
        try:
            if instancia_id:
                if self.request.body:
                    retorno = self.gasto_dominio.delete(instancia_id)
                    self.sucesso(retorno)
            else:
                raise Exception('Informe um id valido para gasto')
        except IntegrityError as e:
            self.falha('exclua os dados realizados antes')
        except Exception as e:
            self.falha(str(e))

    def put(self, instancia_id: str = None):
        try:
            if instancia_id:
                if self.request.body:
                    dados = escape.json_decode(self.request.body)
                    self.gasto_dominio.atualizar(instancia_id, dados)
            else:
                raise Exception('informe o gasto a ser atualizado')
        except Exception as e:
            self.falha(str(e))

    def post(self):
        try:
            if self.request.body:
                data_json = escape.json_decode(self.request.body)
                retorno = self.gasto_dominio.salvar_dados(data_json)
                self.sucesso(retorno)
            else:
                retorno = self.gasto_dominio.retorna_novo_id()
                self.sucesso(retorno)
        except Exception as e:
            self.falha(str(e))

    def get(self, instancia_id: str = None):
        try:
            if instancia_id:
                retorno_gasto = self.gasto_dominio.retornar_gasto(instancia_id)
            else:
                retorno_gasto = self.gasto_dominio.retornar_lista_gasto()
            self.sucesso(retorno_gasto)
        except Gasto.DoesNotExist:
            self.falha('Nao foi encontrado o valor correspondente')
        except Exception as e:
            self.falha(str(e))
