from quickbooks_model import *
from quickbooks import QuickBooks
import sys

def mine_qb_data(consumer_key,consumer_secret, access_token, username=None):
	if username:
		qb_users = [Quickbooks_model.query.filter_by(username=username)].last()
	else:
		qb_users = Quickbooks_model.query.all()

	for qb_user in qb_users:
		access_token_secret = qb_user.access_token
		realm_id = qb_user.realm_id
        print consumer_key
        print consumer_secret
        print access_token
        print access_token_secret
        print realm_id
        """
        qb_querier = QuickBooks(
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            access_token=access_token,
            access_token_secret=access_token_secret,
            company_id=realm_id
        )
        """
        business_objects=["Account","Attachable","Bill","BillPayment",
                "Class","CompanyInfo","CreditMemo","Customer",
                "Department","Employee","Estimate","Invoice",
                "Item","JournalEntry","Payment","PaymentMethod",
                "Preferences","Purchase","PurchaseOrder",
                "SalesReceipt","TaxCode","TaxRate","Term",
                "TimeActivity","Vendor","VendorCredit"]
        qb_querier = QuickBooks(
                consumer_key="qyprdRIvDMh1GfAyToh39mK1WFlIDW",
                consumer_secret="5FYBaYYwMJLNt7ZrQsvsCP1ZBgtAYRo0QJd7ea79",
                access_token="e31e4187b9e5bb4bd2b94bdb9546dc76394a",
                access_token_secret="qyprdLT4aIijOVq8LJKn8GUC6228ninIZXhzeZEqLvOdyKiF"
        )
        print qb_querier.get_access_tokens('yxe21zk')
        sys.stop()
        for obj in business_objects:
            try:
                invoices = qb_querier.query_objects(obj)           
                print invoices 
            except:	
                print obj + ' exception'
                
