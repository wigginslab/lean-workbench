from flask import Blueprint, render_template, request, session, redirect, jsonify, \
url_for, make_response
from flask.ext.security import current_user
import os
import tweepy
from twitter_model import Twitter_model, db
import urllib
from twython import Twython

app = Blueprint('twitter', __name__, template_folder='templates')

# google analytics routes
@app.route('/connect/twitter', methods=['GET', 'POST'])
def twitter_oauth_step_one():
	app_key = os.getenv('twitter_app_key')
	app_secret = os.getenv('twitter_app_secret')
	twitter_callback_url = os.getenv('twitter_callback_url')
	oauth_token = "332196424-x9QD7N3oEH66ZQsEw70sSOVidOn3nkwmRmP0tjOK"
	oauth_secret="qhqNxOpl557NKk2uXcmkfGcGXdCgThgFF9FDcovbKm62P"
	print twitter_callback_url
	print app_key
	print app_secret
	twitter = Twython(app_key, app_secret)
	token = twitter.get_authentication_tokens(callback_url=twitter_callback_url)
	print token
#	session['twitter_oauth_token'] = auth['oauth_token']
#	session['twitter_oauth_token_secret'] = auth['oauth_token_secret']
	"""
	print app_key
	print app_secret
	auth = tweepy.auth.OAuthHandler(app_key, app_secret, "http://localhost:5000")
	print auth.request_token
	try:
		redirect_url = auth.get_authorization_url()
		print redirect_url
		resp = jsonify(status=200,redirect_url=redirect_url)
		return make_response(resp, 200)
	except tweepy.TweepError:
		error_msg = 'Error! Failed to get request token.'
		resp = jsonify(status=500, error=error_msg)
		return make_response(resp, 500)
	"""
	#oauth_token = "332196424-x9QD7N3oEH66ZQsEw70sSOVidOn3nkwmRmP0tjOK"
	#ajaxRequest(url="https://api.twitter.com/oauth/request_token", values={'oauth_callback':twitter_callback_url})


@app.route('/connect/twitter/callback/',methods=['GET', 'POST'])
def twitter_oauth_callback():
	print request.args()
	"""
	app_key = os.getenv("twitter_app_key")
	app_secret = os.getenv("twitter_app_secret")

	oauth_verifier = request.args['oauth_verifier']
	twitter = Twython(app_key, app_secret,
                  session['twitter_oauth_token'], session['twitter_oauth_token_secret'])
	final_step = twitter.get_authorized_tokens(oauth_verifier)
	oauth_token = final_step['oauth_token']
	oauth_secret = final_step['oauth_token_secret']
	credentials_model = Twitter_Model(username = current_user, oauth_token=oauth_token, oauth_secret=oauth_secret)
	db.session.add(credentials_model)
	db.session.submit()
	db.session.close()
	"""