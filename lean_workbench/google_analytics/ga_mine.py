from google_time_string import Google_Time_String
from datetime import datetime, timedelta
from google_analytics_models import Google_Analytics_Visitors, Google_Analytics_User_Model, db
from google_analytics_client import Google_Analytics_API
import json 

def mine_visits():
	ga_users = Google_Analytics_User_Model.query.all()
	print ga_users
	for ga_user in ga_users:
		ga = Google_Analytics_User_Querier(username=ga_user.username)
		print ga.get_new_user_visit_data()
		break


class Google_Analytics_User_Querier:
	"""
	Used to make leanworkench specific queries to the Google Analytics API
	"""
	def __init__(self, username):
		self.username = username
		self.profile_id =  Google_Analytics_API(username).get_profile_id()
		print self.profile_id
	def get_new_user_visit_data(self):
		"""
		Get all the visits data available for a user who just connected their Google Analytics account
		"""
		# start at yesterday
		date = datetime.now()-timedelta(days=1)
		# google string formatted date
		google_date = Google_Time_String(str(date))
		g = Google_Analytics_API(self.username)
		# go backwards in time up to a year
		for backwards_days in range(1,366):
			# create google query object	
			# get visitors and visitor types for the day
			visitor_data = g.client.data().ga().get(
				ids='ga:' + self.profile_id,
				start_date=str(google_date),
				end_date=str(google_date),
				dimensions='ga:visitorType',
				metrics='ga:visits').execute()
			# if there were any visitors that day, rows key will exist
			visitors_type = visitor_data.get('rows')
			# set default 0 values in case no visitors
			total_visitors, new_visits, returning_visitors = 0,0,0
			# if visitors
			if visitors_type:
				for visitor_list in visitors_type:
					if visitor_list[0] == "New Visitor":
						new_visits = int(visitor_list[1])
					if visitor_list[0] == "Returning Visitor":
						returning_visitors = int(visitor_list[1])
				total_visitors = new_visits + returning_visitors
			try:
				percent_new_visits = new_visits/total_visitors
			except:
				percent_new_visits=0
			# add data to model
			visitors_data_model = Google_Analytics_Visitors(
					username=self.username,
					profile_id=self.profile_id,
					date=str(date),
					visitors=total_visitors,
					percent_new_visits=percent_new_visits,
					new_visits=new_visits
			)
			# save visitor data to database
			db.session.add(visitors_data_model)
			db.session.commit()
			db.session.close()
			# set date back in time one day
			date = datetime.now()+timedelta(days=-backwards_days)
			google_date = Google_Time_String(str(date))
	
	def get_new_user_funnel_data(self):
		"""

		Get all the funnels data available for a user who just connected their Google Analytics account

		args: 
			username: username/email of the user whose account it is
		"""
		# start at yesterday
		date = datetime.now()-timedelta(days=1)
		# google string formatted date
		google_date = Google_Time_String(str(date))
		# go backwards in time up to a year
		for backwards_days in range(1,366):
			# create google query object	
			g = Google_Analytics_API(self.username)
			page_path_data = g.client.data().ga().get(
				ids='ga:' + self.profile_id,
				start_date=str(google_date),
				end_date=str(google_date),
				metrics='ga:hostname').execute()
			print json.dumps(page_path_data)	
