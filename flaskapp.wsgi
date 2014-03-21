#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/lean-workbench")

from uwsgi_app import app as application
application.secret_key = "fdsf"
