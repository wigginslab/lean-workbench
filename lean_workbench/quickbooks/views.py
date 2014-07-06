from flask import Blueprint, jsonify, render_template, redirect, request, session, redirect, current_app
import urllib
import json
import calendar
import time
import oauth2 as oauth
from quickbooks_model import *
from flask.ext.security import current_user
from quickbooks import QuickBooks

app = Blueprint('quickbooks', __name__, template_folder='templates')
@app.route('/connect/quickbooks')
def quickbooks():
    print 'inside quickbooks granturl'
    consumer_key = current_app.config.get('QUICKBOOKS_OAUTH_CONSUMER_KEY')
    consumer_secret = current_app.config.get('QUICKBOOKS_OAUTH_CONSUMER_SECRET')
    app_token = current_app.config.get('QUICKBOOKS_APP_TOKEN')
    callback_url = current_app.config.get('QUICKBOOKS_CALLBACK_URL')
    qb = QuickBooks(
             consumer_key=consumer_key, 
             consumer_secret=consumer_secret, 
             callback_url=callback_url)
    global_qb = qb
    oauth_path = qb.get_authorize_url()
    return redirect(oauth_path)
	
@app.route('/connect/quickbooks/callback/')
def quickbooks_callback():

    consumer_key = current_app.config.get('QUICKBOOKS_OAUTH_CONSUMER_KEY')
    consumer_secret = current_app.config.get('QUICKBOOKS_OAUTH_CONSUMER_SECRET')
    app_token = current_app.config.get('QUICKBOOKS_APP_TOKEN')
    callback_url = current_app.config.get('QUICKBOOKS_CALLBACK_URL')
    print request.args
    oauth_token = request.args.get('oauth_token')
    oauth_verifier = request.args.get('oauth_verifier')
    oauth_token_secret = request.args.get('oauth_token_secret')
    qb = QuickBooks(
         consumer_key=consumer_key, 
         consumer_secret=consumer_secret, 
         callback_url=callback_url)

    qb.my_get_access_tokens(oauth_token, oauth_verifier, oauth_token_secret, consumer_secret)
    access_token = qb.access_token
    access_token_secret = qb.access_token_secret
    print 'access token: %s' %(access_token)
    print 'access token secret %s' %(access_token_secret)
    qbm = Quickbooks_model(oauth_verifier=oauth_verifier, realm_id=realm_id,username = current_user.email, access_token=access_token, access_token_secret=access_token_secret)
    db.session.add(qbm)
    db.session.commit()
    db.session.close()
    return render_template('oauth_success.html', service="Quickbooks")
