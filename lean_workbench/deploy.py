from lean_workbench import app
import os
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

http_server = HTTPServer(WSGIContainer(app))
port = os.getenv('port')
http_server.listen(port)
IOLoop.instance().start()


