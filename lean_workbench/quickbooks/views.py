from flask import Blueprint, jsonify, render_template, redirect, request, session, redirect, current_app
import urllib
import json
import calendar
import time
import oauth2 as oauth
from quickbooks_model import *
from flask.ext.security import current_user
from quickbooks import QUICKBOOKS_APP_CALLBACK_URL

app = Blueprint('quickbooks', __name__, template_folder='templates')

@app.route('/connect/quickbooks')
def quickbooks():
	print 'inside quickbooks granturl'
	
	app_key = current_app.config['QUICKBOOKS_APP_KEY']  
	consumer_secret = current_app.config['QUICKBOOKS_APP_SECRET']
	callback_url= current_app.config['QUICKBOOKS_APP_CALLBACK_URL']
	qb = QuickBooks({'consumer_key':app_key, 'consumer_secret':consumer_secret})
	oauth_path = qb.get_authorize_url()
	return redirect(oauth_path)
	
@app.route('/connect/quickbooks/callback/')
def quickbooks_callback():

	token = request.args.get('oauth_token')
	qbm = Quickbooks_model(username = current_user.email, access_token=token)
	db.session.add(qbm)
	db.session.commit()
	db.session.close()
	return render_template('oauth_success.html')

def sign_request(consumer_secret, app_key):
    from hashlib import sha1
    import hmac
    import binascii

    # If you dont have a token yet, the key should be only "CONSUMER_SECRET&"
    key = consumer_secret+"&"+app_key

    # The Base String as specified here: 
    raw = "https://oauth.intuit.com/oauth/v1/get_request_token" # as specified by oauth

    hashed = hmac.new(key, raw, sha1)

    # The signature
    return binascii.b2a_base64(hashed.digest())[:-1]