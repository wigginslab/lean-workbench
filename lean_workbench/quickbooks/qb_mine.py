from quickbooks_model import *
import sys
import requests
from database import db

def mine_qb_data(quickbooks_server_url, api_token, username=None):
        if username:
            users = [QuickbooksUserModel.query.filter_by(username=username)]
        else: 
            users = [x for x in QuickbooksUser.query.all()]
        for user in users:
            username = user.username
            payload = {"username":username, "api_key": api_key}
            r = requests.get(quickbooks_server, payload)
            data = r.json()
            for row in data:
                date = date_tuple(data['date'])
                username = username
                balance = data['balance']
                new_daily_balance = QuickbooksDailyBalance(username=username, balance=balance, date=date)
                user.balances.append(new_daily_balance)
                db.session.add(user)
                db.session.commit()

def date_tuple(self,date_string):
        """
        """
        date_tuple = datetime.datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S.%fZ")
        return date_tuple

