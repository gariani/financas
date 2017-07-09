import os
import tornado.httpserver
import tornado.ioloop
import tornado.web
import json
from urllib.parse import urlparse
import psycopg2

class Conexao():
    # user=oivwavjrjjhwnx
    # pasword=c42a72b35ed8c8f96008da2be25f5f3f4d32f6bbe4fbec4e1555bcd3237b5da4
    # hostname=ec2-23-21-96-159.compute-1.amazonaws.com:5432
    # database=d73u6atflfqjbf

    def run(self):
        # url = urlparse(os.environ["DATABASE_URL"])
        # print(url)
        # print(url.hostname)
        # print(url.port)
        # print(url.username)
        # print(url.password)
        # print(url.path[1:])

        # connect_srt = "dbname='{}' user='{}' host='{}' password='{}'".format(url.path[1:],url.username,url.port+':'+url.port,url.password)
        connect_srt = "dbname='d73u6atflfqjbf' user='oivwavjrjjhwnx' host='ec2-23-21-96-159.compute-1.amazonaws.com:5432' password='c42a72b35ed8c8f96008da2be25f5f3f4d32f6bbe4fbec4e1555bcd3237b5da4'"
        conn = psycopg2.connect(connect_srt)

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
            _conexao.run()
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
