import os
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from main import app_factory
import config

app = app_factory(config.Dev)
app.run()
