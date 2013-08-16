import re
from google_analytics_client import Google_Analytics_API
from datetime import datetime, timedelta
import json
from get_visits import Google_Analytics_User_Querier
def test_get_user_accounts():
	g = Google_Analytics_API("jrubinovitz@gmail.com")
	return g.get_user_accounts()

def test_get_user_profile():
	g = Google_Analytics_API("jrubinovitz@gmail.com")
	user_accounts = g.get_user_accounts()
	return user_accounts.get('items')

def test_get_last_month_visits():
	g = Google_Analytics_API("jrubinovitz@gmail.com")
	user_profiles = g.get_user_accounts().get('items')
	profile = user_profiles[-1]
	profile_id = profile.get('id')
	now = datetime.now()
	one_week_delta = datetime.timedelta(weeks=1)
	one_week_ago = now - one_week_delta


def test_get_month_visits():
	"""
	Currently disallowed
	"""
	g = Google_Analytics_API("jrubinovitz@gmail.com")
	user_profiles = g.get_user_accounts().get('items')
	profile = user_profiles[-1]
	profile_id = profile.get('id')
	# convert date from isoformat to GA query format
	current_date = Google_Time_String(str(datetime.now()-timedelta(days=1))) 
	last_week = Google_Time_String(str(datetime.now() - timedelta(weeks=1)))	
	g.client.data().ga().get(
			      ids='ga:' + profile_id,
				        start_date=last_week,
						      end_date=current_date,
							        metrics='ga:visits').execute()
	assert True

def test_multichannel_funnel():
	g = Google_Analytics_API("jrubinovitz@gmail.com")
	profile_id = g.get_user_accounts().get('items')[0].get('id')
	#print user_profiles
	#profile = user_profiles[-1]
	#print profile
	#profile_id = profile.get('id')
	
	current_date = Google_Time_String(str(datetime.now()-timedelta(days=1))) 
	last_week = Google_Time_String(str(datetime.now() - timedelta(weeks=1)))
	print last_week
	print current_date
	profile_id = g.get_profile_id()

	apiQuery = g.client.data().mcf().get(
		ids="ga:" + profile_id,
		start_date= str(last_week),
		end_date = str(current_date),
		metrics="mcf:totalConversions,mcf:totalConversionValue").execute() 
	print json.dumps(apiQuery)

def test_visitor_count():
	g = Google_Analytics_API("jrubinovitz@gmail.com")
	profile_id = g.get_profile_id()
	query = g.client.data().ga().get(
			ids='ga:' + profile_id,
			start_date='2012-08-14',
			end_date='2013-08-14',
			metrics='ga:visits').execute()
	print json.dumps(query)

class Google_Time_String:
	def __init__(self,time):
		# regular expression that separates all "words"
		time_list = re.findall(r"[\w']+", time)
		self.year = str(time_list[0])
		self.month = str(time_list[1])
		self.day = str(time_list[2])

	def __repr__(self):
		return self.year+"-"+self.month+"-"+self.day

#print test_get_user_accounts()
#test_get_user_profile()
#test_get_month_visits()
#test_multichannel_funnel()
#print test_multichannel_funnel()
#print test_visitor_counts()

g = Google_Analytics_User_Querier("jrubinovitz@gmail.com")
g.get_new_user_visit_data()
