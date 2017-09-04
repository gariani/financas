from tornado import escape
from psycopg2 import IntegrityError
from handler.mainhandler import MainHandler
from domain.realizadodominio import RealizadoDominio


class RealizadoHandler(MainHandler):
    realizado_dominio = RealizadoDominio()

    def delete(self, instancia_id, instancia_id2):
        try:
            if instancia_id:
                if instancia_id2:
                    if self.request.body:
                        retorno = self.realizado_dominio.delete(instancia_id, instancia_id2)
                        self.sucesso(retorno)
                else:
                    raise Exception('Informe um id valido para realizado')
            else:
                raise Exception('Informe um id valido para gasto')
        except IntegrityError as e:
            self.falha('exclua os dados realizados antes')
        except Exception as e:
            self.falha(str(e))

    def put(self, instancia_id, instancia_id2):
        try:
            if instancia_id:
                if instancia_id2:
                    if self.request.body:
                        dados = escape.json_decode(self.request.body)
                        self.realizado_dominio.atualizar(instancia_id, instancia_id2, dados)
                    else:
                        raise Exception('informe os dados a serem atualizados')
                else:
                    raise Exception('informe o realizado a ser atualizado')
            else:
                raise Exception('informe o gasto a ser atualizado')
        except Exception as e:
            self.falha(str(e))

    def post(self, instancia_id: str = None):
        try:
            if instancia_id:
                if self.request.body:
                    retorno = self.realizado_dominio.salvar_dados(instancia_id, self.request.body)
                    self.sucesso(retorno)
                else:
                    raise Exception('nenhum dado informado')
            else:
                raise Exception('informe um gasto valido')
        except Exception as e:
            self.falha(str(e))

    def get(self, instancia_id: str = None, instancia_id2: str = None):
        try:
            if instancia_id:
                if instancia_id2:
                    json_retorno = self.realizado_dominio.realizado(instancia_id, instancia_id2)
                else:
                    json_retorno = self.realizado_dominio.lista_realizado(instancia_id)
            else:
                raise Exception('deve-se informar o gasto desejado')
            self.sucesso(json_retorno)
        except Exception as e:
            self.falha(str(e))
