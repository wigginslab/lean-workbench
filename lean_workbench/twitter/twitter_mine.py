import os
import datetime
from twitter_model import Twitter_model, Date_count
from twython import Twython

def track_keywords():
	app_key = os.getenv('twitter_app_key') 
	app_secret = os.getenv('twitter_app_secret')

	twitter_models = Twitter_model.query.all()
	for user_twitter in twitter_models:
		oauth_token = user_twitter.oauth_token
		oauth_token_secret = user.twitter.oauth_token_secret
		twitter = Twython(app_key, app_secret, oauth_token, oauth_token_secret)
		search_words = user_twitter.words
		for word.word in search_words:
			search_results = twitter.search(q=word)
			count = len(search_results['statuses'])
			date_count = Date_count(count=count)
			word.counts.append(date_count)
