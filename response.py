import os
import tornado.httpserver
import tornado.ioloop
import tornado.web
from handler.gastohandler import GastoHandler
from handler.realizadohandler import RealizadoHandler


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
    print('youry') 
    make_app()
