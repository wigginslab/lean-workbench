#!/usr/bin/python
import sys
import logging
from os import environ

logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/lean-workbench/lean_workbench/")

from uwsgi_app import app as _application

def application(req_environ, start_response):
	environ['db_url'] = req_environ['db_url']
	_application.secret_key = "bob"
	return _application(req_environ, start_response)
