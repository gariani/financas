import json
import tornado
from connection import db


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

    def sucesso(self, json_retorno):
        self.write(json_retorno)
        self.set_header('Content-Type', 'application/json')
        self.set_status(200)

    def falha(self, json_retorno):
        self.set_status(404)
        self.set_header('Content-Type', 'application/json')
        self.write(json.dumps(
            {'status': 'fail', 'Error:': json_retorno}))
