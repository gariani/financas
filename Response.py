import os
import tornado.httpserver
import tornado.ioloop
import tornado.web

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("to mostrando para o anderson")

def make_app():
    application = tornado.web.Application([(r"/", MainHandler), ])
    http_server = tornado.httpserver.HTTPServer(application)
    port = int(os.environ.get("PORT", 5000))
    http_server.listen(port)
    tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    make_app()    
    
