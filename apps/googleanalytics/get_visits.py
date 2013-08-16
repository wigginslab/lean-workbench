from google_time_string import Google_Time_String
from datetime import datetime, timedelta
from models.google_analytics_models import Google_Analytics_Visitors, db
from google_analytics_client import Google_Analytics_API

class Google_Analytics_User_Querier:
	"""
	Used to make leanworkench specific queries to the Google Analytics API
	"""
	def __init__(self, username):
		self.username = username
		self.profile_id =  Google_Analytics_API(username).get_profile_id()
	def get_new_user_visit_data(self):
		"""
		Get all the visits data available for a user who just connected their Google Analytics account
		"""
		print 'datetime now'
		print datetime.now()
		date = datetime.now()-timedelta(days=1)
		print 'date'
		print date
		# google string formatted date
		google_date = Google_Time_String(str(date))
		for backwards_days in range(1,366):
			g = Google_Analytics_API(self.username)
			visitor_data = g.client.data().ga().get(
			ids='ga:' + self.profile_id,
			start_date=str(google_date),
			end_date=str(google_date),
			metrics='ga:visits').execute()
			#print visitor_data
			# set date back in time one day
			date = Google_Time_String(str(datetime.now()+timedelta(days=-backwards_days)))

	def get_new_user_funnel_data(self):
		"""
		Get all the funnels data available for a user who just connected their Google Analytics account

		args: 
			username: username/email of the user whose account it is
		"""
		pass
