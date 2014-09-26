import os
import datetime
from twitter_model import TwitterModel, DateCount
from twython import Twython
from database import db
from flask import current_app

def track_keywords(username = None):
	app_key = current_app.config['TWITTER_APP_KEY']
	app_secret = current_app.config['TWITTER_APP_SECRET']
	if username:
		twitter_models = TwitterModel.query.filter_by(username=username).all()
        else:
		twitter_models = TwitterModel.query.all()

	if twitter_models:
		for user_twitter in twitter_models:
			oauth_token = user_twitter.oauth_token
			oauth_token_secret = user_twitter.oauth_token_secret
			twitter = Twython(app_key, app_secret, oauth_token, oauth_token_secret)
			search_words = user_twitter.words
			for word in search_words:
				search_results = twitter.search(q=word.word)
				print search_results
				count = len(search_results['statuses'])
				print 'count :%i' %(count)
				date_count = DateCount(count=count)
				word.counts.append(date_count)
				db.session.commit()
			user_twitter.active = True
			db.session.add(user_twitter)
			db.session.commit()

