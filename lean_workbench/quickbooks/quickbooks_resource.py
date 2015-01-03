import sys
import os
from quickbooks_model import * 
from flask.ext.restful import Resource, reqparse
from flask import Flask, jsonify, request, make_response
import os
from database import db
from flask.ext.security import current_user
from json import dumps
import requests
import datetime
import time

class Quickbooks_DAO(object):

    def __init__(self):
        self.user_qb = Quickbooks_model.query.filter_by(username=current_user.email).first()

    def as_dict(self):
	return self.user_qb.as_dict()

class Quickbooks_resource(Resource):
    def get(self, **kwargs):
        args = request.args
        get_data = args.get('data')
	if current_user.is_anonymous():
	    return jsonify(qb_authed=False)
	qb = Quickbooks_DAO()
	if qb.user_qb:
            if get_data:
                api_key = current_app.config['QUICKBOOKS_SERVER_API_TOKEN']
                quickbooks_server = current_app.config['QUICKBOOKS_SERVER_URL']
                payload = {"username":current_user.email, "api_key": api_key}
                r = requests.get(quickbooks_server, payload)
                data = r.json()
                date_balance = [[self.return_date_in_ms(x["date"]),x["balance"]] for x in data]
                return make_response(dumps(date_balance)) 
            else:
                return make_response(dumps([{'qb_authed':True, 'qb_server_url':current_app.config.get('QUICKBOOKS_SERVER_URL')}]))
        else:
            return make_response(dumps([{'qb_authed':False}]))

    def post(self):
        args = request.args
        new_user = args.get('new_user')
        if new_user:
            new_qb_user = QuickbooksUser(username=new_user)
            db.session.add(new_qb_user)
            db.session.commit()
            return jsonify(status=200)
	return jsonify(qb_authed=True)

    def return_date_in_ms(self,date_string):
        """
        For D3 to parse

        args:
            date_string - ruby on rails date string output
        returns:
            date_ms - date in milliseconds
        """
        date_tuple = datetime.datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S.%fZ")
        date_ms = time.mktime(date_tuple)*1000
        return date_ms
