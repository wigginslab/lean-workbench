# -*- coding:utf-8 -*-

from flask.ext import script

import commands

from gunicorn_server import GunicornServer

from celery import Celery

if __name__ == "__main__":
	from main import app_factory
	import config
	from flask.ext.script import Server, Manager
	import os
	manager = script.Manager(app_factory)
	manager.add_option("-c", "--config", dest="config", required=False, default=config.Dev)
	manager.add_command("test", commands.Test())
	manager.add_command("create_db", commands.CreateDB())
	manager.add_command("drop_db", commands.DropDB())
	manager.add_command("mine", commands.Mine())

	manager.run()