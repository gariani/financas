import os
import tornado.httpserver
import tornado.ioloop
import tornado.web
import json

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
    def get(self):
        try:
            _mock = Mock()
            kk = tornado.escape.json_encode(_mock.mock())
            self.write(kk)
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
         (r"/id/(\d+)$", IdHandler), ], autoreload=True)
    http_server = tornado.httpserver.HTTPServer(application)
    port = int(os.environ.get("PORT", 5000))
    http_server.listen(port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    make_app()
