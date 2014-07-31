from flask import Blueprint, jsonify, render_template, redirect, request, session, redirect, current_app
import urllib
import json
import calendar
import time
import oauth2 as oauth
from quickbooks_model import *
from flask.ext.security import current_user
from quickbooks import QuickBooks
import os

app = Blueprint('quickbooks', __name__, template_folder='templates')

consumer_key = os.getenv('QUICKBOOKS_OAUTH_CONSUMER_KEY')
consumer_secret = os.getenv('QUICKBOOKS_OAUTH_CONSUMER_SECRET')
app_token = os.getenv('QUICKBOOKS_APP_TOKEN')
callback_url = os.getenv('QUICKBOOKS_CALLBACK_URL')
qb = QuickBooks(
 consumer_key=consumer_key, 
 consumer_secret=consumer_secret, 
 callback_url=callback_url)

@app.route('/connect/quickbooks')
def quickbooks():
    print 'original qb for auth url'
    print qb
    oauth_path = qb.get_authorize_url()
    print qb.qbService
    return redirect(oauth_path)
	
@app.route('/connect/quickbooks/callback/')
def quickbooks_callback():

    oauth_token = request.args.get('oauth_token')
    oauth_verifier = request.args.get('oauth_verifier')
    oauth_token_secret = request.args.get('oauth_token_secret')
    realm_id = request.args.get('realmId')
    print 'qb in callback'
    
    qb.get_access_tokens(oauth_verifier)
    
    access_token = qb.access_token
    access_token_secret = qb.access_token_secret
    print 'access token: %s' %(access_token)
    print 'access token secret %s' %(access_token_secret)
    qbm = Quickbooks_model(oauth_verifier=oauth_verifier, realm_id=realm_id,username = current_user.email, access_token=access_token, access_token_secret=access_token_secret)
    db.session.add(qbm)
    db.session.commit()
    db.session.close()
    return render_template('oauth_success.html', service="Quickbooks")
