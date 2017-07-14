import os
import tornado.httpserver
import tornado.ioloop
import tornado.web
import json


class MainHandler(tornado.web.RequestHandler):

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    def options(self):
        self.set_status(204)
        self.finish()


class GastoHandler(MainHandler):

    def get(self, instancia_id: str = None):

        try:

            self.set_status(200)
        except Exception():
            self.set_status(404)
            self.write(json.dumps(
                {'status': 'fail', 'Error:': 'Nao foi encontrado o valor correspondente'}))


class RealizadoHandler(MainHandler):
    def get(self, instancia_id: str = None):
        try:
            x = 1
            x = x + 1
            print(x)

        except Exception():
            self.set_status(404)
            self.write(json.dumps(
                {'status': 'fail', 'Error:': 'Nao foi encontrado o valor correspondente'}))


def make_app():
    route = [(r"/gasto", GastoHandler), (r"/gasto/(\d+)$", GastoHandler),
             (r"/gasto/(\d+)$/realizado/(\d+)$", RealizadoHandler), ]

    application = tornado.web.Application(route, debug=True, autoreload=True)
    http_server = tornado.httpserver.HTTPServer(application)
    port = int(os.environ.get("PORT", 5000))
    http_server.listen(port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    make_app()
