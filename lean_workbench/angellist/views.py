from flask import Blueprint, render_template, request, session, redirect

app = Blueprint('angel_list', __name__, template_folder='templates')
@app.route('/connect/angellist/', methods=['GET'])
def connect_angellist():
	"""
	Step 1 of connection to angellist api
	"""
	#if request.method =='GET':
	#	return render_template('partials/angellist.html')
	redirect_url = AngelList().getAuthorizeURL()
	print redirect_url
	return redirect(redirect_url)

@app.route('/connect/angellist/callback',methods=['GET'])
def angellist_callback():
	print 'in callback'
	if 'username' in session:
		username = escape(session['username'])
	else:
		username = None
	code = request.args.get("code")
	al = AngelList()
	code = al.getAccessToken(code=code)
	al.save(code=code, username=username)
	return redirect(url_for('index'))
