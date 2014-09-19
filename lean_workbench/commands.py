# -*- coding:utf-8 -*-

from flask.ext.script import Command, Option, prompt_bool
import os
import config
from main import app_factory
import datetime
from datetime import timedelta
from sqlalchemy import func

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

    def run(self, new=False):
        app = app_factory(config.Dev)
        with app.app_context():
            from database import db
            from sqlalchemy.sql import func
            from users.user_model import Role, User
            from google_analytics.google_analytics_models import Google_Analytics_Visitors
            from twitter.twitter_model import Twitter_model, Cohort_Tweet_Count_Model
            from facebook.facebook_model import Facebook_page_data, Cohort_Facebook_Likes_Model

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
                    start = db.session.query(Google_Analytics_Visitors).order_by(Google_Analytics_Visitors.date).first().date
                    end = today
                while start < end:
                    # get all users in cohort
                    cohort_usernames = User.query.filter(User.roles.any(name=cohort[0])).with_entities(User.email).all()
                    # get all GA visitor counts from after this time yesterday and before now
                    visitors = Google_Analytics_Visitors.query.filter(Google_Analytics_Visitors.username.in_(cohort_usernames), Google_Analytics_Visitors.date > start, Google_Analytics_Visitors.date < end).with_entities(Google_Analytics_Visitors.visitors).all()
                    detupled_vistors = [x[0] for x in visitors]
		    print detupled_vistors
                    if detupled_vistors:
                        visitor_avg = (sum(detupled_vistors))/len(detupled_vistors)
                    else:
                        visitor_avg = 0

		    new_ga_visitors = Google_Analytics_Visitors.query.filter_by(username="cohort:"+cohort[0],  date = start).first()
		    if not new_ga_visitors:
			new_ga_visitors = Google_Analytics_Visitors(username="cohort:"+cohort[0], visitors=visitor_avg, date = start)
		    else:
			new_ga_visitors.visitors = visitor_avg
                    db.session.add(new_ga_visitors)
                    db.session.commit()
                    start = start + timedelta(days=1)


                # because you don't have time to figure out this query in SQLAlchemy right now
                tweet_date_counts = {}
		fb_like_date_counts = {}
                for username in cohort_usernames:
                    twitter_words = Twitter_model.query.filter_by(username=username).first()
                    
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
				    tweet_date_counts[date] = tweet_date_counts[date] + count
				except:
				    tweet_date_counts[date] = count
                           
                        facebook_likes = Facebook_page_data.query.filter_by(username=username).all()
                        for like in facebook_likes:
                            date = like.date
                            like_count =  like.likes
			    try:
				fb_like_date_counts[date] = fb_like_date_counts[date] + 1
			    except:
				fb_like_date_counts[date] = like_count

		for date in tweet_date_counts:
		    count = tweet_date_counts[date]
		    new_tweet_count = Cohort_Tweet_Count_Model.query.filter_by(date=date).first()
		    if not new_tweet_count: 
			new_tweet_count = Cohort_Tweet_Count_Model(cohort_name=cohort, date=date, count=count)
		    else:
			new_tweet_count.count = count

		    db.session.add(new_tweet_count)
		    db.session.commit()
		
		for date in fb_like_date_counts:
		    count = fb_like_date_counts[date]
		    new_fb_count = Cohort_Facebook_Likes_Model.query.filter_by(date=date).first()
		    if not new_fb_count:
			new_fb_count = Cohort_Facebook_Likes_Model(cohort_name=cohort,date=date,likes_count=count)
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
		    print user
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

class DeleteGACreds(Command):
    def run(self):
        app = app_factory(config.Dev)
        with app.app_context():
            from database import db 
            from google_analytics.google_analytics_models import Google_Analytics_User_Model
            ga_users = Google_Analytics_User_Model.query.all()
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


        app = app_factory(config.Dev)
        with app.test_client() as c:
            rv = c.get('/?vodka=42')
            from google_analytics_models import Google_Analytics_User_Model
            ga_users = Google_Analytics_User_Model.query.all()
            for user in ga_users:
                assert ga_user.refresh_token != None


