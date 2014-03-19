import os
import datetime
from twitter_model import Twitter_model, Date_count
from twython import Twython
from database import db

def track_keywords(username = None):
	app_key = os.getenv('twitter_app_key') 
	app_secret = os.getenv('twitter_app_secret')
	if username:
		twitter_models = Twitter_model.query.filter_by(username=username).first()
	else:
		twitter_models = Twitter_model.query.all()

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
				date_count = Date_count(count=count)
				word.counts.append(date_count)
				db.session.commit()
		db.session.close()
