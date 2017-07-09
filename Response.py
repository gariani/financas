import os
import tornado.httpserver
import tornado.ioloop
import tornado.web
import json
import asyncio
import asyncpg
from urllib.parse import urlparse
from urllib.parse import urlsplit


class Conexao():

    async def run():
        url = urlparse(os.environ["DATABASE_URL"])
        conn = await asyncpg.connect(host=url.hostname,
                                     port=url.port,
                                     user=url.username,
                                     password=url.password,
                                     database=url.path[1:])

        #conn = await asyncpg.connect(url)

        #values = await conn.fetch('''SELECT * FROM gasto''')
        await conn.close()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())


class Mock():
    def mock(self, id=1):
        dic = {}
        dic["id"] = id
        dic["descricaoPrevisto"] = "Alimentação"
        dic["valorPrevisto"] = 200.00
        dic["realizados"] = "realizados1"
        dic["totalRealizado"] = 10.0
        dic["saldo"] = 190.00
        return dic


class MainHandler(tornado.web.RequestHandler):

    def set_default_headers(self):
        print("setting headers!!!")
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    def options(self):
        self.set_status(204)
        self.finish()

    def get(self):
        try:
            _conexao = Conexao()
            _mock = Mock()
            _json = json.dumps(_mock.mock())
            # kk = tornado.escape.json_encode(_json)
            self.write(_json)
        except Exception() as e:
            self.write(json.dumps(
                {'status': 'fail', 'error': "Error: %s" % format(e)}))


class IdHandler(tornado.web.RequestHandler):

    def get(self, *args, **kwargs):
        _id = args[0]
        _mock = Mock()
        self.write(_mock.mock(_id))


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
