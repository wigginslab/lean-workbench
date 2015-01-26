# -*- coding:utf-8 -*-

from flask.ext.script import Command, Option, prompt_bool
import os
import config
from main import app_factory
import datetime
from datetime import timedelta
from sqlalchemy import func
import json
from flask.ext.migrate import Migrate, MigrateCommand
import requests

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
            from scale.scale_model import StartupDataModel
            from scale.scale_mine import get_vcs
            users = StartupDataModel.query.filter_by(vc_matcher_done=False).filter(StartupDataModel.description != None).all()
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

    def run(self, new=False):
        app = app_factory(config.Dev)
        with app.app_context():
            from database import db
            from sqlalchemy.sql import func
            from users.user_model import Role, User
            from google_analytics.google_analytics_models import GoogleAnalyticsVisitors
            from twitter.twitter_model import TwitterModel, CohortTweetCountModel
            from facebook.facebook_model import FacebookPageData, CohortFacebookLikesModel

            # get all cohorts
            cohorts = db.session.query(Role.name.distinct()).all()
	    	
	    yesterday = datetime.datetime.now()-timedelta(days=1)
            today = datetime.datetime.now()


            # mine for each cohort 
            for cohort in cohorts:
                
                # get yesterday and today so we can query changes in between days
	        if not new:
                    start = yesterday
                    end = today

                else:
                    start = db.session.query(GoogleAnalyticsVisitors).order_by(GoogleAnalyticsVisitors.date).first().date
                    end = today
                while start < end:
                    # get all users in cohort
                    cohort_usernames = User.query.filter(User.roles.any(name=cohort[0])).with_entities(User.email).all()
                    # get all GA visitor counts from after this time yesterday and before now
                    visitors = GoogleAnalyticsVisitors.query.filter(GoogleAnalyticsVisitors.username.in_(cohort_usernames), GoogleAnalyticsVisitors.date > start, GoogleAnalyticsVisitors.date < end).with_entities(GoogleAnalyticsVisitors.visitors).all()
                    detupled_vistors = [x[0] for x in visitors]
		    print detupled_vistors
                    if detupled_vistors:
                        visitor_avg = (sum(detupled_vistors))/len(detupled_vistors)
                    else:
                        visitor_avg = 0

		    new_ga_visitors = GoogleAnalyticsVisitors.query.filter_by(username="cohort:"+cohort[0],  date = start).first()
		    if not new_ga_visitors:
			new_ga_visitors = GoogleAnalyticsVisitors(username="cohort:"+cohort[0], visitors=visitor_avg, date = start)
		    else:
			new_ga_visitors.visitors = visitor_avg
                    db.session.add(new_ga_visitors)
                    db.session.commit()
                    start = start + timedelta(days=1)


                # because you don't have time to figure out this query in SQLAlchemy right now
                tweet_DateCounts = {}
		fb_like_DateCounts = {}
                for username in cohort_usernames:
                    twitter_words = TwitterModel.query.filter_by(username=username).first()
                    
                    if twitter_words:
                        twitter_words = twitter_words.words
                        for word in twitter_words:
                            word_name = word.word
                            dates =  [counts.date for counts in word.counts.all() if counts.date > yesterday and counts.date < today ]
                            counts = [counts.count for counts in word.counts.all() if counts.date > yesterday and counts.date < today ]
                            
                            for i in range(len(dates)):
                                date = dates[i]
                                count = counts[i]
				try:
				    tweet_DateCounts[date] = tweet_DateCounts[date] + count
				except:
				    tweet_DateCounts[date] = count
                           
                        facebook_likes = FacebookPageData.query.filter_by(username=username).all()
                        for like in facebook_likes:
                            date = like.date
                            like_count =  like.likes
			    try:
				fb_like_DateCounts[date] = fb_like_DateCounts[date] + 1
			    except:
				fb_like_DateCounts[date] = like_count

		for date in tweet_DateCounts:
		    count = tweet_DateCounts[date]
		    new_tweet_count = CohortTweetCountModel.query.filter_by(date=date).first()
		    if not new_tweet_count: 
			new_tweet_count = CohortTweetCountModel(cohort_name=cohort, date=date, count=count)
		    else:
			new_tweet_count.count = count

		    db.session.add(new_tweet_count)
		    db.session.commit()
		
		for date in fb_like_DateCounts:
		    count = fb_like_DateCounts[date]
		    new_fb_count = CohortFacebookLikesModel.query.filter_by(date=date).first()
		    if not new_fb_count:
			new_fb_count = CohortFacebookLikesModel(cohort_name=cohort,date=date,likes_count=count)
		    else:
			new_fb_count.count = count
		    db.session.add(new_fb_count)
		    db.session.commit()

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
        from twitter.twitter_model import TwitterModel
        from quickbooks.quickbooks_model import QuickbooksUser
        from facebook.facebook_model import FacebookModel
        from google_analytics.google_analytics_models import GoogleAnalyticsUserModel
    	from twitter.twitter_mine import track_keywords
    	from google_analytics.ga_mine import mine_visits
        from facebook.fb_mine import mine_fb_page_data
        from quickbooks.qb_mine import mine_qb_data
        
        app = app_factory(config.Dev)
        print 'inside mine'
        with app.app_context():
            api_token = app.config.get('QUICKBOOKS_SERVER_API_TOKEN')
            quickbooks_server_url = app.config.get('QUICKBOOKS_SERVER_URL') + "/data"
              
            if new:
                new_twitters = TwitterModel.query.filter_by(active=False).all()
                new_fbs = FacebookModel.query.filter_by(active=False).all()
                new_gas = GoogleAnalyticsUserModel.query.filter_by(active=False).all()
                new_qbs = QuickbooksUser.query.filter_by(active=False).all()
                for user in new_twitters:
                    try:
                        track_keywords(username=user.username)
                    except:
                        print '%s failed twitter mine' %(user.username)
                for user in new_fbs:
                    try:
                        mine_fb_page_data(username=user.username)   
                    except:
                        print '%s failed fb mine' %(user.username)
                for user in new_gas:
                    try:
                        mine_visits(username=user.username)
                    except:
                        print '% failed ga visitor mine' %(user.username)
                for user in new_qbs:
                    try:
                        mine_visits(username=user.username, quickbooks_server_url=quickbooks_server_url,api_token=api_token)
                    except:
                        print '% failed qb mine' %(user.username)
            else:        
                #mine_fb_page_data()
                mine_visits()
                #track_keywords()
                #mine_qb_data(quickbooks_server_url,api_token)

class PrintUsers(Command):
	"""
	Mines the data sources
	"""
	def run(self):
		from users.user_model import User
		users = User.query.all()
		for user in users:
			print users

class DeleteGACreds(Command):
    def run(self):
        app = app_factory(config.Dev)
        with app.app_context():
            from database import db 
            from google_analytics.google_analytics_models import GoogleAnalyticsUserModel
            ga_users = GoogleAnalyticsUserModel.query.all()
            print 'ga_users before' + str(ga_users)
            for ga_user in ga_users:
                db.session.delete(ga_user)
                db.session.commit()
            print 'ga_users now ' + str([ ga_user.refresh_token for ga_user in ga_users])

class RefreshGA(Command):
    def run(self):
        from google_analytics.google_analytics_client import GoogleAnalyticsAPI
        app = app_factory(config.Dev)
        with app.app_context():
            from database import db 
            from google_analytics.google_analytics_models import GoogleAnalyticsUserModel
            ga_users = GoogleAnalyticsUserModel.query.all()
            for ga_user in ga_users:
                GoogleAnalyticsAPI(username=ga_user.username).refresh_token()
            print 'ga_users now ' + str([ ga_user.refresh_token for ga_user in ga_users])

            from google_analytics.google_analytics_models import GoogleAnalyticsUserModel
            ga_users = GoogleAnalyticsUserModel.query.all()
            print 'ga_users before' + str(ga_users)
            for ga_user in ga_users:
                db.session.delete(ga_user)
                db.session.commit()
            print 'ga_users now ' + str([ ga_user.refresh_token for ga_user in ga_users])


class Test(Command):
    """
    Run tests
    """
    def run(self):
        from flask import request
        from wufoo.wufoo_model import WufooSurveyModel


        app = app_factory(config.Dev)
        with app.test_client() as c:
            from database import db
            
            
            test_file = open("test/wufoo.json", "r").read()
            test_json_dict = json.loads(test_file)
            form_structure = json.loads(test_json_dict['FormStructure'])

            form_url = "https://rubinovitz.wufoo.com/forms/my-new-feature/"

            print form_structure
            new_survey = WufooSurveyModel(
                   username="jen@leanworkbench.com",
                   wufoo_email=form_structure['Email'],
                   url=form_url,
                   name=form_structure['Url']
            )
            db.session.add(new_survey)
            db.session.commit()

            rv = c.post(
                    '/api/v1/wufoo', data=test_json_dict
                    )
            db.session.delete(new_survey) 
            print rv

class MigrateUsers(Command):
    def run(self):
        import csv
        app = app_factory(config.Dev)
        
        with app.app_context():
            from database import db 
            from users.user_model import User
            with open('user_table.csv', 'rb') as csvfile:
                for row in csvfile:
                    id,email,password,last_login_at,current_login_at,last_login_ip,current_login_ip,login_count,created,company,active,confirmed_at,onboarded = row.split(';')
                    active = True
                    new_user = User(email=email,password=password,company=company,active=active, onboarded=False)
                    db.session.add(new_user)
                    db.session.commit()
                    print 'user ' + email + 'migrated'

class PingQB(Command):
    """
    ping quickbooks server to keep it awake
    """
    def run(self):
        app = app_factory(config.Dev)
        with app.app_context():
            requests.get(app.config.get('QUICKBOOKS_SERVER_URL'))