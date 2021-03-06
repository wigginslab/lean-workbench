from database import db
import time
import datetime

ga_profiles_association = db.Table('user_profiles_association',
    db.Column('user_id', db.Integer, db.ForeignKey('google_analytics_oauth_credentials.id')),
    db.Column('profile_id', db.Integer, db.ForeignKey('google_analytics_profiles.id'))
)

class GoogleAnalyticsUserModel(db.Model):

    __tablename__ = "google_analytics_oauth_credentials"

    id = db.Column(db.Integer, primary_key=True)
    token_expiry = db.Column(db.DateTime, default = datetime.datetime.now()) 
    access_token = db.Column(db.String)
    client_id = db.Column(db.String)
    client_secret = db.Column(db.String)
    profile_id = db.Column(db.String)
    account_id = db.Column(db.String)
    webproperty_id = db.Column(db.String)
    refresh_token = db.Column(db.String)
    revoke_uri = db.Column(db.String)
    id_token = db.Column(db.String)
    token_response = db.Column(db.String)
    # LWB username
    username = db.Column(db.String)
    # already mined once?
    active = db.Column(db.Boolean)

    def __init__(self, credentials_dict):
		print credentials_dict
		self.username = credentials_dict.get("username")
		self.access_token = credentials_dict.get("access_token")
		self.client_id = credentials_dict.get("client_id"),
		self.client_secret = credentials_dict.get("client_secret")
		self.refresh_token = credentials_dict.get("refresh_token")
		self.token_expiry = credentials_dict.get("token_expiry")
		self.token_uri = credentials_dict.get("token_uri")
		self.user_agent = credentials_dict.get("user_agent")
                self.active = False

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def str(self):
        return str(self.username)
        
class GoogleAnalyticsProfiles(db.Model):
	
	__tablename__ = "google_analytics_profiles"

	id = db.Column(db.Integer, primary_key=True)
	user =  db.relationship("GoogleAnalyticsUserModel", secondary = ga_profiles_association)
	profile_id = db.Column(db.String)

	def __init__(self, user, profile_id):
		self.user = user
		self.profile_id = profile_id

class GoogleAnalyticsVisitors(db.Model):
    """
    Google Analytics Site Visitor Metrics
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    profile_id = db.Column(db.Integer)
    date = db.Column(db.DateTime)
    visitors = db.Column(db.Integer)
    new_visits = db.Column(db.Integer)
    percent_new_visits = db.Column(db.Integer)

    def __init__(self, username=None, profile_id=None, date=None, visitors=None, new_visits=None, percent_new_visits=None):
        self.username= username
        self.profile_id=profile_id
        self.date=date
        self.visitors=visitors
        self.new_visits = new_visits
        self.percent_new_visits = percent_new_visits

    def as_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'profile_id': self.profile_id,
            'date': time.mktime(datetime.datetime.timetuple(self.date))*1000,
            'visitors':self.visitors,
            'new_visits':self.new_visits,
            'percent_new_visits':self.percent_new_visits
        }

    def as_count(self, all_visitors=True):
        if all_visitors:
            return [time.mktime(datetime.datetime.timetuple(self.date))*1000, self.visitors]
        else:
            return [time.mktime(datetime.datetime.timetuple(self.date))*1000, self.new_visits]

class GoogleAnalyticsReferralsModel(db.Model):
    """
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    date = db.Column(db.DateTime, default=datetime.datetime.now())
    source = db.Column(db.String)
    medium = db.Column(db.String)
    sessions = db.Column(db.Integer)
    pageviews = db.Column(db.Integer)
    session_duration = db.Column(db.Float)
    exits = db.Column(db.Integer)

class GoogleAnalyticsSignups(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    date = db.Column(db.DateTime, default=datetime.datetime.now())
    signups = db.Column(db.Integer)

    def as_count(self):
        return [time.mktime(datetime.datetime.timetuple(self.date))*1000, self.signups]


class GoogleAnalyticsReturningVisitors(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    date = db.Column(db.DateTime, default=datetime.datetime.now())
    returning_visitors = db.Column(db.Integer)
    all_visitors = db.Column(db.Integer)

    def as_count(self):
        return [time.mktime(datetime.datetime.timetuple(self.date))*1000, self.returning_visitors]

class GoogleAnalyticsExperiment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now())
    status = db.Column(db.String)
    experiment_id = db.Column(db.String)
    objective_metric = db.Column(db.String)
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    minimum_experiment_length_in_days = db.Column(db.Integer)
    winner_id = db.Column(db.String)
    winner_found = db.Column(db.Boolean)
    variations = db.relationship('GoogleAnalyticsExperimentVariation',
      backref='GoogleAnalyticsExperiment',
      lazy='dynamic')
  
    def __init__(self, status, winner_found, start_time, end_time, experiment_id, username=username):
      self.status = status
      self.winner_found = winner_found
      self.start_time = start_time
      self.end_time = end_time
      self.experiment_id = experiment_id
      self.username = username

    def as_dict(self):
        return {
                "experiment_id":self.experiment_id,
                "winner_found":self.winner_found,
                "variations": [x.as_dict() for x in self.variations]
                }
class GoogleAnalyticsExperimentVariation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, default=datetime.datetime.now())
    url = db.Column(db.String)
    status = db.Column(db.String)
    name = db.Column(db.String)
    weight = db.Column(db.Float(5))
    experiment_id = db.Column(db.Integer, db.ForeignKey('google_analytics_experiment.id'))
    won = db.Column(db.Boolean)

    def __init__(self, url,status,weight, won, name):
        self.url = url
        self.status = status
        self.weight = weight
        self.won = won
        self.name = name

    def as_dict(self):
        return{
            "name":self.name,
            "url":self.url,
            "won":self.won,
            "status":self.status
        }
