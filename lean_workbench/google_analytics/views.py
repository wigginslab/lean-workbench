from flask import Blueprint, render_template, request, session, redirect, url_for
from google_analytics_client import Google_Analytics_API
from flask.ext.security import current_user

app = Blueprint('google_analytics', __name__, template_folder='templates')

# google analytics routes
@app.route('/connect/google-analytics', methods=['GET', 'POST'])
def google_analytics_oauth():
	print current_user
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
			redirect_url = GA_API.step_one()
			return redirect(redirect_url)
	else:
		print "start oauth process"
		# start OAuth process
		redirect_url = GA_API.step_one()
		return redirect(redirect_url)

@app.route('/connect/google-analytics/callback/',methods=['GET', 'POST'])
def google_analytics_callback():
	if current_user:
		username = current_user.email
		GA_API = Google_Analytics_API('username')
		ga_api_code= request.args.get("code")
		print 'ga callback args'
		print request.args
		print GA_API
		client = GA_API.step_two(username, ga_api_code)
	else:
		return redirect('/')
	return redirect('/onboarding/virality')