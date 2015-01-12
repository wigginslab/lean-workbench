from google_time_string import GoogleTimeString
from datetime import datetime, timedelta
from google_analytics_models import GoogleAnalyticsVisitors, GoogleAnalyticsReferralsModel, GoogleAnalyticsUserModel, db
from google_analytics_client import GoogleAnalyticsAPI
import json 

def mine_visits(username=None):
	if not username:
		ga_users = GoogleAnalyticsUserModel.query.all()
	else:
		ga_users = [GoogleAnalyticsUserModel.query.filter_by(username=username).first()]
                ga_users[0].active = True
                db.session.add(ga_users[0])
                db.session.commit()
	if ga_users:
		for ga_user in ga_users:
                    try:
                        ga = Google_Analytics_User_Querier(username=ga_user.username)
                        # get the latest visit data
                        ga.get_new_user_visit_data()
                        ga.get_referral_data()
                        print '%s ga data mined' %(ga_user.username)
                    except:
                        print 'exception mining %s ga data' %(ga_user.username)

class Google_Analytics_User_Querier:
	"""
	Used to make leanworkench specific queries to the Google Analytics API
	"""
	def __init__(self, username):
		self.username = username
		self.profile_id =  GoogleAnalyticsAPI(username).get_profile_id()
		print self.profile_id
        
        def get_referral_data(self):
	    # check to see if mined before
	    mined = GoogleAnalyticsReferralsModel.query.filter_by(username=self.username).all()
	    if mined:
		# just mine yesterday
		days_back = 2
		
	    else:
		# go a year back
		days_back = 366
	    date = datetime.now()
	    # go backwards in time up to a year
	    for backwards_days in range(1,days_back):
		try:
		    date = date - timedelta(days=1)
		    # google string formatted date
		    google_date = GoogleTimeString(str(date))
		    g = GoogleAnalyticsAPI(self.username)

		    referral_data = g.client.data().ga().get(
				    ids='ga:' + self.profile_id,
				    start_date=str(google_date),
				    end_date=str(google_date),
				    sort="ga:sessions",
				    dimensions='ga:source,ga:medium',
				    metrics='ga:sessions,ga:pageviews,ga:sessionDuration,ga:exits').execute()
		    column_headers = referral_data.get('columnHeaders')
		    rows =  referral_data.get('rows')

		    for row in rows:
			source, medium, sessions, pageviews, session_duration, exits = row
			referral_model = GoogleAnalyticsReferralsModel(username=self.username, date = date, source= source, medium=medium, sessions=sessions, pageviews=pageviews, session_duration=session_duration, exits = exits)
			db.session.add(referral_model)
			db.session.commit()

		except Exception,e: print str(e)


	def get_new_user_visit_data(self):
		"""
		Get all the visits data available for a user who just connected their Google Analytics account, or if visitor data exists get yesterday's data
		"""
		# start at yesterday
		date = datetime.now()-timedelta(days=1)
		# google string formatted date
		google_date = GoogleTimeString(str(date))
		g = GoogleAnalyticsAPI(self.username)
		user_visitor_data = GoogleAnalyticsVisitors.query.filter_by(username=self.username).all()
		
        # if already mined, just do yesterday
		if user_visitor_data:
			date = datetime.now()-timedelta(days=1)
			google_date = GoogleTimeString(str(date))

			visitor_data = g.client.data().ga().get(
				ids='ga:' + self.profile_id,
				start_date=str(google_date),
				end_date=str(google_date),
				dimensions='ga:visitorType',
				metrics='ga:visits').execute()

			# save visitor data to database
			self.process_visitor_data(visitor_data,date)
		
		# if first time mining GA data for user
		else:
			# go backwards in time up to a year
			for backwards_days in range(1,366):
				# create google query object	
				# get visitors and visitor types for the day
				try:
				    
				    visitor_data = g.client.data().ga().get(
					    ids='ga:' + self.profile_id,
					    start_date=str(google_date),
					    end_date=str(google_date),
					    dimensions='ga:visitorType',
					    metrics='ga:visits').execute()

				    # parse and save visitor data to database
				    self.process_visitor_data(visitor_data, date)

				except:
				    print 'ga new visitor mining exception, setting visitors to 0'
				    visitors_data_model = GoogleAnalyticsVisitors(username=self.username,profile_id=self.profile_id,date=str(date),visitors=total_visitors,percent_new_visits=percent_new_visits,new_visits=new_visit)
				    db.session.add(visitors_data_model)
				    db.session.commit()
		
				date = date - timedelta(days=1)
				google_date = GoogleTimeString(str(date))

	def process_visitor_data(self,visitor_data, date):
		"""
		Takes the result of a Google Analytics API Client query for visitors, parses, and saves to database
		"""
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
		visitors_data_model = GoogleAnalyticsVisitors(
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

	def get_new_user_funnel_data(self):
		"""

		Get all the funnels data available for a user who just connected their Google Analytics account

		args: 
			username: username/email of the user whose account it is
		"""
		# start at yesterday
		date = datetime.now()-timedelta(days=1)
		# google string formatted date
		google_date = GoogleTimeString(str(date))
		# go backwards in time up to a year
		for backwards_days in range(1,366):
			# create google query object	
			g = GoogleAnalyticsAPI(self.username)
			page_path_data = g.client.data().ga().get(
				ids='ga:' + self.profile_id,
				start_date=str(google_date),
				end_date=str(google_date),
				metrics='ga:hostname').execute()
			print json.dumps(page_path_data)	
