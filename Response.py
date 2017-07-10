import os
import tornado.httpserver
import tornado.ioloop
import tornado.web
import json
from PoolConection import PostgresConnectionPool

class Conexao():
    def __init__(self):
        self.query_all = """SELECT id, descricao_previsto, valor_previsto, realizado, total_realizado, saldo FROM gasto"""
        self.query_count = """SELECT * FROM gasto"""
        self.columns = ('id', 'descricao_previsto', 'valor_previsto', 'realizado', 'total_realizado', 'saldo')
        self.pool = PostgresConnectionPool(
            "dbname='d73u6atflfqjbf' user='oivwavjrjjhwnx' host='ec2-23-21-96-159.compute-1.amazonaws.com' password='c42a72b35ed8c8f96008da2be25f5f3f4d32f6bbe4fbec4e1555bcd3237b5da4'",
            maxsize=3)

    def formatar(self, chaves, valores):
        _results = []
        for row in valores:
            _results.append(dict(zip(chaves, row)))
        return json.dumps(_results)

    def execute(self):
        _valor = self.pool.execute(self.query_count)
        return self.formatar(('total'), _valor)

    def fetchall(self):
        _valores = self.pool.fetchall(self.query_all)
        return self.formatar(self.columns, _valores)

    def fetchone(self, id):
        _valores = []
        _valor = self.pool.fetchone("""SELECT * FROM gasto WHERE id={}""".format(id))
        if _valor is not None:
            _valores.append(_valor)
            return self.formatar(self.columns, _valores)
        else:
            return self.formatar(['Error'], [('Nao foi encontrado o valor correspondente',)])

class MainHandler(tornado.web.RequestHandler):

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    def options(self):
        self.set_status(204)
        self.finish()

    def get(self):
        try:
            print("ISAAK")
            _conexao = Conexao()
            _valor = _conexao.fetchall()
            self.write(_valor)
        except Exception() as e:
            self.set_status(404)
            self.write(json.dumps(
                {'status': 'fail', 'error': "Error: %s" % format(e)}))


class IdHandler(tornado.web.RequestHandler):

    def get(self, *args, **kwargs):
        _id = args[0]
        _conexao = Conexao()
        _valor = _conexao.fetchone(_id)
        self.write(_valor)

def make_app():
    application = tornado.web.Application(
        [(r"/", MainHandler),
         (r"/id/(\d+)$", IdHandler), ], debug=True, autoreload=True)
    http_server = tornado.httpserver.HTTPServer(application)
    port = int(os.environ.get("PORT", 5000))
    http_server.listen(port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    make_app()
