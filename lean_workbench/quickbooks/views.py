from flask import Blueprint, jsonify, render_template, redirect, request, session, redirect, current_app
import urllib
import json
import calendar
import time
import oauth2 as oauth
from quickbooks_model import *
from flask.ext.security import current_user
from quickbooks import QuickBooks

QUICKBOOKS_TOKEN="dcb197a3b9244b41beb886bb327cc4e21bef"
QUICKBOOKS_APP_KEY="qyprdRQ8jzw8c83JDT9mEfWns69bNT"
QUICKBOOKS_APP_SECRET="glVdi3UXU3gr6lB9EI8W5y19mHEspikNzc3RHkHM"
QUICKBOOKS_APP_CALLBACK_URL="http://127.0.0.1:5000/connect/quickbooks/callback/"

qb = QuickBooks(
    consumer_key = QUICKBOOKS_APP_KEY,
    consumer_secret = QUICKBOOKS_APP_SECRET,
    callback_url = QUICKBOOKS_APP_CALLBACK_URL,
)


app = Blueprint('quickbooks', __name__, template_folder='templates')
@app.route('/connect/quickbooks')
def quickbooks():
    oauth_path = qb.get_authorize_url()
    return redirect(oauth_path)
	
@app.route('/connect/quickbooks/callback/')
def quickbooks_callback():

    oauth_verifier = request.args.get('oauth_verifier')
    oauth_token = request.args.get('oauth_token')
    print 'oauth token %s' %(oauth_token)

    #qb.set_up_service()
    qb.get_access_tokens( oauth_verifier)
    
    access_token = qb.access_token
    access_token_secret = qb.access_token_secret
    qbm = Quickbooks_model(oauth_verifier=oauth_verifier, realm_id=realm_id,username = current_user.email, access_token=access_token, access_token_secret=access_token_secret)
    db.session.add(qbm)
    db.session.commit()
    db.session.close()
    return render_template('oauth_success.html', service="Quickbooks")
