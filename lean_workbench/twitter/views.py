from flask import Blueprint, Response, render_template, request, session, redirect, jsonify,\
url_for, make_response, current_app
from flask.ext.security import current_user
import os
from twitter_model import Twitter_model, db
import urllib
from twython import Twython

app = Blueprint('twitter', __name__, template_folder='templates')

@app.route('/connect/twitter', methods=['GET', 'POST'])
def twitter_oauth_step_one():
	app_key = current_app.config['TWITTER_APP_KEY']
	app_secret = current_app.config['TWITTER_APP_SECRET']
	twitter_callback_url = current_app.config['TWITTER_APP_CALLBACK_URL'] 
	twitter = Twython(app_key, app_secret)
	auth = twitter.get_authentication_tokens(callback_url=twitter_callback_url)
	session['twitter_oauth_token'] = auth['oauth_token']
	session['twitter_oauth_token_secret'] = auth['oauth_token_secret']
	auth_url = auth['auth_url']
	return jsonify(redirect_url=auth_url,status=100)

@app.route('/connect/twitter/success/', methods=['GET', 'POST'])
def twitter_success():
	return redirect('/onboarding/pay')

@app.route('/connect/twitter/callback/',methods=['GET', 'POST'])
def twitter_oauth_callback():
	oauth_verifier = request.args.get('oauth_verifier')
	app_key = current_app.config['TWITTER_APP_KEY']
	app_secret = current_app.config['TWITTER_APP_SECRET']
	oauth_token = session['twitter_oauth_token']
	oauth_token_secret = session['twitter_oauth_token_secret'] 
	twitter = Twython(app_key, app_secret, oauth_token, oauth_token_secret)
	final_step = twitter.get_authorized_tokens(oauth_verifier)
	user_oauth_token = final_step['oauth_token']
	user_oauth_token_secret = final_step['oauth_token_secret']
	twitter_username = final_step['screen_name']
	twitter_row = Twitter_model({'username':current_user.email,
		'twitter_handle':twitter_username,
		'oauth_token':user_oauth_token,
		'oauth_token_secret':user_oauth_token_secret, 
		'company':current_user.company
	})
	db.session.add(twitter_row)
	db.session.commit()
	db.session.close()
	return render_template("oauth_success.html", service="Twitter")
