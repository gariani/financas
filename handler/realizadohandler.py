from handler.mainhandler import MainHandler
from model.realizadomodel import Realizado
from domain.realizadodominio import RealizadoDominio


class RealizadoHandler(MainHandler):
    realizadoDominio = RealizadoDominio()

    def post(self, instancia_id: str = None):
        try:
            if instancia_id:
                if self.request.body:
                    retorno = self.realizadoDominio.salvar_dados(instancia_id, self.request.body)
                    self.sucesso(retorno)
                else:
                    raise Exception('nenhum dado informado')
        except Exception as e:
            self.falha(str(e))

    def get(self, instancia_id: str = None, instancia_id2: str = None):
        try:
            if instancia_id:
                if instancia_id2:
                    json_retorno = self.realizadoDominio.realizado(instancia_id, instancia_id2)
                else:
                    json_retorno = self.realizadoDominio.lista_realizado(instancia_id)
            else:
                raise Exception('deve-se informar o gasto desejado')
            self.sucesso(json_retorno)
        except Realizado.DoesNotExist:
            self.falha('Nao foi encontrado o valor correspondente.')
        except Exception as e:
            self.falha(str(e))
