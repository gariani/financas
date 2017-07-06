import os
import tornado.httpserver
import tornado.ioloop
import tornado.web
import json

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        try:
            response = {'status':'sucesso','resposta':'oi marcel!'}
            kk = tornado.escape.json_encode(response)
            kk = wrap_callback(self, kk)
            self.write(kk)
        except Exception e:
            self.write(json.dumps({'status':'fail','error': "Error: %s" % format_exec()}))
         

def make_app():
    application = tornado.web.Application([(r"/", MainHandler), ])
    http_server = tornado.httpserver.HTTPServer(application)
    port = int(os.environ.get("PORT", 5000))
    http_server.listen(port)
    tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    make_app()    
    
