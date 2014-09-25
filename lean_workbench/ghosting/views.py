from flask import Blueprint, jsonify, render_template, redirect, request, session, redirect, current_app
import urllib
import json
import calendar
import time
import oauth2 as oauth
from ghosting_model import GhostingModel
from flask.ext.security import current_user


app = Blueprint('ghosting', __name__, template_folder='templates')
@app.route('/ghosting')
def ghosting():
    args = request.json
    # get the feature being ghosted
    feature = args.get('feature')
    username = current_user.email
    ghost = GhostingModel(feature=feature,username=username)
    db.session.add(ghost)
    db.session.commit()
    db.session.close()
    return make_response(json.dumps([{'status':200, 'message':'Feature noted.'}]))
