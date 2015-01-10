from database import db
import datetime
import time

class QuickbooksUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    active = db.Column(db.Boolean, default=False)
    daily_balances = db.relationship('QuickbooksDailyAccountBalance', backref='quickbooks_user', lazy='joined')

class QuickbooksDailyAccountBalance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)    
    balance = db.Column(db.Float)
    quickbooks_user_id = db.Column(db.Integer, db.ForeignKey('quickbooks_user.id'))
    name = db.Column(db.String)

    def __init__(self,date, username, balance,name):
            self.date = date
            self.balance = balance
            self.name = name

    def date_balance(self):
        return [time.mktime(datetime.datetime.timetuple(self.date))*1000, self.balance]
