# -*- coding:utf-8 -*-

from flask.ext.script import Command, Option, prompt_bool
import os
import config
from main import app_factory
import datetime
from datetime import timedelta

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

class Scale(Command):
    """
    For now, just hit the VC-matcher server
    """
    
    # allow user to enter 
    # python manage.py scale --new=True
    # to mine only new API keys
    option_list = (
        Option('--new', '-n', dest='new'),
    ) 
    def run(self, new=False):
        """
        Run the mining

        args:
            new- if true, check for users that haven't been mined yet and mine only their data.
        """
        app = app_factory(config.Dev)
        with app.app_context():
            from scale.scale_model import Startup_data_model
            from scale.scale_mine import get_vcs
            users = Startup_data_model.query.filter_by(vc_matcher_done=False).filter(Startup_data_model.description != None).all()
            if users:
                get_vcs(users)

class Cohort(Command):
    """
    Aggregate cohort stats (daily) 
    """
    # allow user to enter 
    # python manage.py cohort --new=True
    # to mine only new API keys from the last day
    option_list = (
        Option('--new', '-n', dest='new'),
    ) 

    def run(self):
        app = app_factory(config.Dev)
        with app.app_context():
            from database import db
            from sqlalchemy.sql import func
            from users.user_model import Role, User
            from google_analytics.google_analytics_models import Google_Analytics_Visitors
            from twitter.twitter_model import Twitter_model
            from facebook.facebook_model import Facebook_page_data

            # get all cohorts
            cohorts = db.session.query(Role.name.distinct()).all()

            # mine for each cohort 
            for cohort in cohorts:
                
                # get yesterday and today so we can query changes in between days

                if new:
                    yesterday = datetime.datetime.now()-timedelta(days=1)
                    today = datetime.datetime.now()
                    start = yesterday
                    end = today

                else:
                    start = Google_Analytics_Visitors.order_by(Google_Analytics_Visitors.date).first().date
                    end = today
                while start < end:
                    # get all users in cohort
                    cohort_usernames = User.query.filter(User.roles.any(name=cohort[0])).with_entities(User.email).all()
                    # get all GA visitor counts from after this time yesterday and before now
                    visitors = Google_Analytics_Visitors.query.filter(Google_Analytics_Visitors.username.in_(cohort_usernames), Google_Analytics_Visitors.date > yesterday, Google_Analytics_Visitors.date < today).with_entities(Google_Analytics_Visitors.visitors).all()
                    detupled_vistors = [x[0] for x in visitors]
                    if detupled_vistors:
                        visitor_avg = (sum(detupled_vistors))/len(detupled_vistors)
                    else:
                        visitor_avg = 0

                    new_ga_visitors = Google_Analytics_Visitors(username="cohort:"+cohort[0], visitors=visitor_avg, date = start)
                    start = start + timedelta(days=1)

            # because you don't have time to figure out this query in SQLAlchemy right now
                tweet_date_counts = {}
                for username in cohort_usernames:
                    twitter_words = Twitter_model.query.filter_by(username=username).first()
                    if twitter_words:
                        twitter_words = twitter_words.words
                        print twitter_words
                        for word in twitter_words:
                            #.filter(word.counts.date < today).all()
                            dates =  [str(counts.date) for counts in word.counts.all() if counts.date > yesterday and counts.date < today ]
                            counts = [counts.count for counts in word.counts.all() if counts.date > yesterday and counts.date < today ]

                        facebook_likes = Facebook_page_data.query.filter_by(username=username).all()
                        for like in facebook_likes:
                            print str(like.date)
                            print like.likes
class Mine(Command):
    """
    Mines the data sources
    """
    
    # allow user to enter 
    # python manage.py mine --new=True
    # to mine only new API keys
    option_list = (
        Option('--new', '-n', dest='new'),
    ) 
    def run(self, new=False):
        """
        Run the mining

        args:
            new- if true, check for users that haven't been mined yet and mine only their data.
        """
        from twitter.twitter_model import Twitter_model
        from quickbooks.quickbooks_model import Quickbooks_model
        from facebook.facebook_model import Facebook_model
        from google_analytics.google_analytics_models import Google_Analytics_User_Model
    	from twitter.twitter_mine import track_keywords
    	from google_analytics.ga_mine import mine_visits
        from facebook.fb_mine import mine_fb_page_data
        #from quickbooks.qb_mine import mine_qb_data
        app = app_factory(config.Dev)
        with app.app_context():
            consumer_key = app.config.get('QUICKBOOKS_OAUTH_CONSUMER_KEY')
            consumer_secret = app.config.get('QUICKBOOKS_OAUTH_CONSUMER_SECRET')
            app_token = app.config.get('QUICKBOOKS_APP_TOKEN')
              
            if new:
                new_twitters = Twitter_model.query.filter_by(active=False).all()
                #new_qbs = Quickbooks_model.query.filter_by(active=False).all()
                new_fbs = Facebook_model.query.filter_by(active=False).all()
                new_gas = Google_Analytics_User_Model.query.filter_by(active=False).all()
                for user in new_twitters:
                    track_keywords(username=user.username)
                for user in new_fbs:
                    mine_fb_page_data(username=user.username)   
                for user in new_gas:
                    mine_visits(username=user.username)
            else:        
                mine_fb_page_data()
                mine_visits()
                track_keywords()
                #mine_qb_data(consumer_key,consumer_secret,app_token)

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
            print argv
            unittest.main(argv=argv)
        else:
            print("Directory '%s' was not found in project root." % start_discovery)
