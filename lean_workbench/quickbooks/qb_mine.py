from quickbooks_model import *
from quickbooks import QuickBooks

def mine_qb_data(app_key, app_secret, app_token, username=None):
	if username:
		qb_users = [Quickbooks_model.query.filter_by(username=username)].last()
	else:
		qb_users = Quickbooks_model.query.all()

	for qb_user in qb_users:
		access_token = qb_user.access_token
		realm_id = qb_user.realm_id
		print app_key
		print app_secret
		print app_token
		print access_token
	qb_querier = QuickBooks(
		consumer_key=app_key,
		consumer_secret=app_secret,
		access_token=app_token,
		access_token_secret=access_token,
		company_id=realm_id
	)
	invoices = qb_querier.query_objects("Bill")	
	print invoices