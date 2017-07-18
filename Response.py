import os
import tornado.httpserver
import tornado.ioloop
import tornado.web
from Gasto import *


class GastoHandler(tornado.web.RequestHandler):

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    def options(self):
        self.set_status(204)
        self.finish()

    def get(self, instancia_id: str = None):

        try:
            gasto: Gasto = Gasto()
            if instancia_id is None:
                _valor = gasto.fetchall()
            else:
                _valor = gasto.fetchone(instancia_id)

            self.set_status(200)
            self.set_header('Content-Type', 'application/json')
            self.finish(_valor)
        except Exception():
            self.set_status(404)
            self.set_header('Content-Type', 'application/json')
            self.write(json.dumps(
                {'status': 'fail', 'Error:': 'Nao foi encontrado o valor correspondente'}))


class RealizadoHandler(tornado.web.RequestHandler):

    def get(self, instancia_id: str = None):
        try:
            realizado: Realizado = Realizado()
            if instancia_id is None:
                _valor = realizado.fetchall()
            else:
                _valor = realizado.fetchone(instancia_id)

            self.set_status(200)
            self.finish(_valor)

        except Exception():
            self.set_status(404)
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
