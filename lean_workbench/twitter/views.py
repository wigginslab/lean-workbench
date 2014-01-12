from flask import Blueprint, render_template, request, session, redirect, url_for
from flask.ext.security import current_user
import os
from twython import Twython
from twitter_model import Twitter_model, db

app = Blueprint('twitter', __name__, template_folder='templates')

# google analytics routes
@app.route('/connect/twitter', methods=['GET', 'POST'])
def twitter_oauth_step_one():
	app_key = os.getenv("twitter_app_key")
	app_secret = os.getenv("twitter_app_secret")
	twitter = Twython(app_key, app_secret)
	session['twitter_oauth_token'] = auth['oauth_token']
	session['twitter_oauth_token_secret'] = auth['oauth_token_secret']
	auth = twitter.get_authentication_tokens(callback_url=os.getenv('twitter_callback_url'))

@app.route('/connect/twitter/callback/',methods=['GET', 'POST'])
def twitter_oauth_callback():
	print request.args()
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