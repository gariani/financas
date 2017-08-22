import json
import os
import tornado.httpserver
import tornado.ioloop
import tornado.web

from tornado import escape
from collections import defaultdict
from playhouse.shortcuts import model_to_dict, dict_to_model
from model.gastomodel import Gasto
from model.realizadomodel import Realizado
from connection import db

"""class CreateTables:
    db.drop_tables([Gasto, Realizado])
    db.create_tables([Gasto, Realizado], safe=True)

    with db.atomic():
        Gasto.insert_many([
            {"id": 1, "descricao_previsto": "Teste", "valor_previsto": 11.2, "total_realizado": 8, "saldo": 4},
            {"id": 2, "descricao_previsto": "Teste 2", "valor_previsto": 14, "total_realizado": 7.5, "saldo": 6.5},
            {"id": 3, "descricao_previsto": "Teste 3", "valor_previsto": 20, "total_realizado": 10, "saldo": 10}
        ]).execute()

    with db.atomic():
        Realizado.insert_many([
            {"id": 1, "descricao": "Teste Realizado 1", "valor": 100.00, "gasto": 1},
            {"id": 2, "descricao": "Teste Realizado 2", "valor": 220.22, "gasto": 1},
            {"id": 3, "descricao": "Teste Realizado 3", "valor": 221.10, "gasto": 1},
            {"id": 4, "descricao": "Teste Realizado 4", "valor": 560.00, "gasto": 2},
            {"id": 5, "descricao": "Teste Realizado 5", "valor": 212.00, "gasto": 3},
            {"id": 6, "descricao": "Teste Realizado 6", "valor": 10.00, "gasto": 2},
            {"id": 7, "descricao": "Teste Realizado 7", "valor": 22.00, "gasto": 3},
            {"id": 8, "descricao": "Teste Realizado 8", "valor": 20.10, "gasto": 1},
            {"id": 9, "descricao": "Teste Realizado 9", "valor": 20.01, "gasto": 2},
            {"id": 10, "descricao": "Teste Realizado 10", "valor": 29.01, "gasto": 3}
        ]).execute()
        
        Teste
"""


class ErrorDadosObrigatorio(Exception):
    def __init__(self, code):
        self.code = code

    def __str__(self):
        return repr(self.code)


class MainHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    def options(self):
        self.set_status(204)
        self.finish()

    def prepare(self):
        if db.is_closed():
            db.connect()
        return super(MainHandler, self).prepare()

    def on_finish(self):
        if not db.is_closed():
            db.close()
        return super(MainHandler, self).on_finish()


class GastoHandler(MainHandler):
    def salvarDados(self, dados):
        print(dados)
        novo_gasto = Gasto.create(descricao_previsto=dados['descricao_previsto'],
                                  valor_previsto=dados['valor_previsto'],
                                  total_realizado=dados['total_realizado'],
                                  saldo=dados['saldo'])
        return novo_gasto

    def post(self):
        try:
            if self.request.body:
                data_json = escape.json_decode(self.request.body)
                gasto = self.salvarDados(data_json)
                self.write(json.dumps(model_to_dict(gasto)))
            else:
                self.write('vazio')
        except ErrorDadosObrigatorio as e:
            formataMensagem = {'error': str(e)}
            self.set_header('Content-Type', 'application/json')
            self.set_status(400)
            self.write(json.dumps(formataMensagem))

    def get(self, instancia_id: str = None):

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
            self.write(json_retorno)
            self.set_header('Content-Type', 'application/json')
            self.set_status(200)
        except Gasto.DoesNotExist:
            self.set_header('Content-Type', 'application/json')
            self.set_status(404)
            self.write(json.dumps(
                {'status': 'fail', 'Error:': 'Nao foi encontrado o valor correspondente'}))
        except Exception:
            self.set_header('Content-Type', 'application/json')
            self.set_status(404)
            self.write(json.dumps(
                {'status': 'fail', 'Error:': 'Nao foi encontrado o valor correspondente'}))


class RealizadoHandler(MainHandler):
    def selecionar_gasto(self, id_gasto):
        return Gasto.select().where(Gasto.id == id_gasto)

    def salvar_dados(self, dados):
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
            print(str(e))

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
                dict = []
                for i in retorno_realizado:
                    dict.append(model_to_dict(i))
                json_retorno = json.dumps(dict)

            print(json_retorno)
            self.write(json_retorno)
            self.set_header('Content-Type', 'application/json')
            self.set_status(200)
        except Realizado.DoesNotExist:
            self.set_status(404)
            self.set_header('Content-Type', 'application/json')
            self.write(json.dumps(
                {'status': 'fail', 'Error:': 'Nao foi encontrado o valor correspondente'}))
        except Exception:
            self.set_status(404)
            self.set_header('Content-Type', 'application/json')
            self.write(json.dumps(
                {'status': 'fail', 'Error:': 'Nao foi encontrado o valor correspondente'}))


def make_app():
    route = [(r"/gasto", GastoHandler),
             (r"/gasto/(\d+)$", GastoHandler),
             (r"/gasto\/(\d+)\/realizado", RealizadoHandler),
             (r"/gasto\/(\d+)\/realizado\/(\d+)", RealizadoHandler), ]

    application = tornado.web.Application(route, debug=True, autoreload=True)
    http_server = tornado.httpserver.HTTPServer(application)
    port = int(os.environ.get("PORT", 5000))
    http_server.listen(port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    make_app()
