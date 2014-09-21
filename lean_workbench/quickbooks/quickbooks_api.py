from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import os
from quickbooks_model import *

class Quickbooks_API:
    access_token = ''
    access_token_secret = ''
    consumer_key = ''
    consumer_secret = ''
    company_id = 0
    callback_url = ''
    session = None

    base_url_v3 =  "https://quickbooks.api.intuit.com/v3"
    base_url_v2 = "https://qbo.intuit.com/qbo1"

    request_token_url = "https://oauth.intuit.com/oauth/v1/get_request_token"
    access_token_url = "https://oauth.intuit.com/oauth/v1/get_access_token"

    authorize_url = "https://appcenter.intuit.com/Connect/Begin"

    # Things needed for authentication
    qbService = None

    request_token = ''
    request_token_secret = ''

    def __init__(self, **args):
	
        if 'cred_path' in args:
            self.read_creds_from_file(args['cred_path'])

        if 'consumer_key' in args:
            self.consumer_key = args['consumer_key']

        if 'consumer_secret' in args:
            self.consumer_secret = args['consumer_secret']
                               
        if 'access_token' in args:
            self.access_token = args['access_token']

        if 'access_token_secret' in args:
            self.access_token_secret = args['access_token_secret']

        if 'company_id' in args:
            self.company_id = args['company_id']

        if 'callback_url' in args:
            self.callback_url = args['callback_url']

        if 'verbose' in args:
            self.verbose = True
        else:
            self.verbose = False

        self._BUSINESS_OBJECTS = [

        "Account","Attachable","Bill","BillPayment",
        "Class","CompanyInfo","CreditMemo","Customer",
        "Department","Employee","Estimate","Invoice",
        "Item","JournalEntry","Payment","PaymentMethod",
        "Preferences","Purchase","PurchaseOrder",
        "SalesReceipt","TaxCode","TaxRate","Term",
        "TimeActivity","Vendor","VendorCredit"

        ]



    def get_authorize_url(self):
        """Returns the Authorize URL as returned by QB, 
        and specified by OAuth 1.0a.
        :return URI:
        """
        print 'inside get_authorize_url'
        self.qbService = OAuth1Service(
                name = None,
                consumer_key = self.consumer_key,
                consumer_secret = self.consumer_secret,
                request_token_url = self.request_token_url,
                access_token_url = self.access_token_url,
                authorize_url = self.authorize_url,
                base_url = None
            )
        self.request_token, self.request_token_secret = self.qbService.get_request_token(
                params={'oauth_callback':self.callback_url}
            )

        print self.qbService.get_request_token(
                params={'oauth_callback':self.callback_url}
        )
        return self.qbService.get_authorize_url(self.request_token)


