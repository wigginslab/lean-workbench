# -*- coding:utf-8 -*-

from flask.ext import script

import commands

from main import app_factory
import config

from flask.ext.migrate import Migrate, MigrateCommand



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
	manager.add_command("users", commands.PrintUsers())
	manager.add_command("scale", commands.Scale())
	manager.add_command("cohort", commands.Cohort())
	manager.add_command("delete_ga", commands.DeleteGACreds())
	manager.add_command("refresh_ga", commands.RefreshGA())
	manager.add_command('db', MigrateCommand)
	manager.add_command('ping_qb', commands.PingQB())
	manager.run()
