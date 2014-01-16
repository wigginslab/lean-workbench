#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/lean-workbench/lean_workbench/")

from uwsgi_app import app as application
application.config['db_url'] = 'sdfsdf'
application.secret_key = 'Add your secret key'
