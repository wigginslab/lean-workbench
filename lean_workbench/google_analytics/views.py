from flask import Blueprint, render_template, request, session, redirect, url_for
from google_analytics_client import Google_Analytics_API
from flask.ext.security import current_user
from flask import current_app

app = Blueprint('google_analytics', __name__, template_folder='templates')

# google analytics routes
@app.route('/connect/google-analytics', methods=['GET', 'POST'])
def google_analytics_oauth():
	google_analytics_callback_url = current_app.config['GOOGLE_ANALYTICS_CALLBACK_URL']
	google_analytics_client_id = current_app.config['GOOGLE_ANALYTICS_CLIENT_ID']
	username = current_user.email
	if not username:
		print 'not logged in'
		return redirect(url_for('index'))
	GA_API = Google_Analytics_API(username)
	if GA_API.credentials:
		expires_on = GA_API.credentials.as_dict()['token_expiry']
		current_time = datetime.now().isoformat()
		# if credentials have not expired
		if expires_on > current_time:
			print GA_API.credentials.as_dict()
			# you shouldn't have hit this link
			print "you have credentials for GA"
			return redirect(url_for('view_ga'))
		else:
			print "credentials expired, start oauth process"
			# start OAuth process
			redirect_url = GA_API.step_one(google_analytics_callback_url, google_analytics_client_id)
			return redirect(redirect_url)
	else:
		print "start oauth process"
		# start OAuth process
		redirect_url = GA_API.step_one(google_analytics_callback_url, google_analytics_client_id)
		return redirect(redirect_url)

@app.route('/connect/google-analytics/callback/',methods=['GET', 'POST'])
def google_analytics_callback():
	google_analytics_callback_url = current_app.config['GOOGLE_ANALYTICS_CALLBACK_URL']
	if current_user:
		username = current_user.email
		GA_API = Google_Analytics_API('username')
		ga_api_code= request.args.get("code")
		print 'ga callback args'
		print request.args
		print GA_API
		client = GA_API.step_two(username, ga_api_code, google_analytics_callback_url)
	else:
		return redirect('/')
	return redirect('/onboarding/virality')
