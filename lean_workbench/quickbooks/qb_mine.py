from quickbooks_model import *
from quickbooks import QuickBooks
import sys
import traceback

def mine_qb_data(consumer_key,consumer_secret,  username=None):
	if username:
		qb_users = [Quickbooks_model.query.filter_by(username=username)].last()
                qb_users[0].active = True
                db.session.add(qb_users[0])
                db.session.commit()
	else:
		qb_users = Quickbooks_model.query.all()

	for qb_user in qb_users:
	    access_token_secret = qb_user.access_token_secret
	    realm_id = qb_user.realm_id
            access_token = qb_user.access_token

	    print "consumer_key %s" %(consumer_key)
	    print "consumer_secret %s" %(consumer_secret)
	    print "access_token %s" %(access_token)
	    print "access_token_secret %s" %(access_token_secret)
	    print "realm_id %s" %(realm_id)
	    business_objects=["Account","Attachable","Bill","BillPayment",
		    "Class","CompanyInfo","CreditMemo","Customer",
		    "Department","Employee","Estimate","Invoice",
		    "Item","JournalEntry","Payment","PaymentMethod",
		    "Preferences","Purchase","PurchaseOrder",
		    "SalesReceipt","TaxCode","TaxRate","Term",
		    "TimeActivity","Vendor","VendorCredit"]
	    qb_querier = QuickBooks(
		    consumer_key=consumer_key,
		    consumer_secret=consumer_secret,
		    access_token=access_token,
		    access_token_secret=access_token_secret,
		    realm_id=realm_id
	    )
	    for obj in business_objects:
		try:
		    invoices = qb_querier.query_objects("Bill")           
		    print invoices 
		except:
		    print traceback.format_exc()
		    print obj + ' exception'
		    break 
