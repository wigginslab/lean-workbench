from flask import Blueprint, render_template, jsonify, request, session, redirect, url_for
from flask.ext.security import current_user
import os
from facebook_model import Facebook_model, db
import urllib

app = Blueprint('facebook', __name__, template_folder='templates')

@app.route('/connect/facebook', methods=['GET', 'POST'])
def facebook_oauth_step_one():
	app_key = os.getenv('facebook_app_key')
	print app_key
	app_secret = os.getenv('facebook_app_secret')
	callback_url=os.getenv('facebook_callback_url')
	args = dict(client_id=app_key,
                    redirect_uri=callback_url)
	return jsonify({"redirect_url": "https://graph.facebook.com/oauth/authorize?" +
                urllib.urlencode(args), 'status':100})

@app.route('/connect/facebook/callback/',methods=['GET', 'POST'])
def facebook_oauth_callback():
	print request.args
	"""
	oauth_verifier = request.args.get('oauth_verifier')
	app_key = os.getenv('twitter_app_key')
	app_secret = os.getenv('twitter_app_secret')
	oauth_token = session['twitter_oauth_token']
	oauth_token_secret = session['twitter_oauth_token_secret'] 
	twitter = Twython(app_key, app_secret, oauth_token, oauth_token_secret)
	final_step = twitter.get_authorized_tokens(oauth_verifier)
	user_oauth_token = final_step['oauth_token']
	user_oauth_token_secret = final_step['oauth_token_secret']
	twitter_row = Twitter_model({'username':current_user.email, 'oauth_token':user_oauth_token,'oauth_token_secret':user_oauth_token_secret})
	db.session.add(twitter_row)
	db.session.commit()
	db.session.close()
	return "Success!"
	"""