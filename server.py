from tornado.httpserver import HTTPServer
from tornado.wsgi import WSGIContainer
from tornado.ioloop import IOLoop
from run import app

s=HTTPServer(WSGIContainer(app))
s.listen(8026)
IOLoop.current().start()