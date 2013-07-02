from google_analytics_client import Google_Analytics_API
from datetime import datetime

g = Google_Analytics_API("jen")

def test_get_user_accounts():
	
	return g.get_user_accounts()

def test_get_user_profile():
	user_accounts = g.get_user_accounts()
	return user_accounts.get('items')

def test_get_all_visits():
	user_profiles = g.get_user_accounts().get('items')
	profile = user_profiles[-1]
	profile_id = profile.get('id')
	# convert date from isoformat to GA query format
	date_created = profile.get('created').split('T')[0]
	current_date = datetime.now().timetuple()
	print current_date
	current_year = str(current_date[0])
	current_month = str(current_date[1])
	if len(current_month) < 2: current_month = '0'+current_month
	current_day = str(current_date[2])
	if len(current_day) < 2: current_day = '0'+current_day
	current_date_string = current_year + '-' +  current_month + '-' + current_day
	g.client.data().ga().get(
			      ids='ga:' + profile_id,
				        start_date=date_created,
						      end_date=current_date_string,
							        metrics='ga:visits').execute()

test_get_user_accounts()
test_get_user_profile()
test_get_all_visits()
