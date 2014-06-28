# -*- coding:utf-8 -*-

from flask.ext.script import Command, Option, prompt_bool

import os
import config

from main import app_factory
import config

class CreateDB(Command):
    """
    Creates sqlalchemy database
    """

    def run(self):
        from database import create_all

        create_all()


class DropDB(Command):
    """
    Drops sqlalchemy database
    """

    def run(self):
        from database import drop_all

        drop_all()

class Mine(Command):
    """
    Mines the data sources
    """

    option_list = (
        Option('--new', '-n', dest='new'),
    ) 
    def run(self, new=False):
        """
        Run the mining

        args:
            new- if true, check for users that haven't been mined yet and mine only their data.
        """
        from twitter.twitter_model import *
        from quickbooks.quickbooks_model import *
        from facebook.facebook_model import *
    	from twitter.twitter_mine import track_keywords
    	from google_analytics.ga_mine import mine_visits
        from facebook.fb_mine import mine_fb_page_data
        from quickbooks.qb_mine import mine_qb_data
        app = app_factory(config.Dev)
        with app.app_context():
            if new:
                new_twitters = Twitter_model.query.filter_by(active=False).all()
                new_qbs = Quickbooks_model.query.filter_by(active=False).all()
                new_fbs = Facebook_model.query.filter_by(active=False).all()
                new_gas = Google_Analytics_User_Model.query.filter_by(active=False).all()

            mine_fb_page_data()
            mine_visits()
            track_keywords()
            consumer_key = app.config.get('QUICKBOOKS_OAUTH_CONSUMER_KEY')
            consumer_secret = app.config.get('QUICKBOOKS_OAUTH_CONSUMER_SECRET')
            app_token = app.config.get('QUICKBOOKS_APP_TOKEN')
            mine_qb_data(consumer_key,consumer_secret,app_token)
        pass

class PrintUsers(Command):
	"""
	Mines the data sources
	"""
	def run(self):
		from users.user_model import User
		users = User.query.all()
		for user in users:
			print users

class Test(Command):
    """
    Run tests
    """

    start_discovery_dir = "tests"

    def get_options(self):
        return [
            Option('--start_discover', '-s', dest='start_discovery',
                   help='Pattern to search for features',
                   default=self.start_discovery_dir),
        ]

    def run(self, start_discovery):
        import unittest

        if os.path.exists(start_discovery):
            argv = [config.project_name, "discover"]
            argv += ["-s", start_discovery]

            unittest.main(argv=argv)
        else:
            print("Directory '%s' was not found in project root." % start_discovery)
