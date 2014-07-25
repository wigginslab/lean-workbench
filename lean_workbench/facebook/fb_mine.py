from facebook_model import Facebook_page_data, Facebook_model, db
import facebook_module as facebook

def mine_fb_page_data(username=None):
	# if only for one user
	if username:
		fb_user = Facebook_model.query.filter_by(username=username).order_by('-id').first()
		users = [fb_user]
                fb_user.active = True
                db.session.add(fb_user)
                db.session.commit()

	else:
		users = Facebook_model.query.all()

	for user in users:
		oauth_access_token = user.access_token
		username = user.username
		if oauth_access_token:
			# get graph
			graph = facebook.GraphAPI(oauth_access_token)
			# get pages
			pages = graph.request('me/accounts')
			page_access_token = pages['data'][0]['access_token']
			print oauth_access_token
			print '\n'
			print page_access_token
			print '\n'
			# get likes per page for today
			page_id = pages['data'][0]['category_list'][0]['id']
			page = graph.request(str(page_id)+'?access_token='+page_access_token)
			print page
			try:
				likes = page['likes']
			except:
				likes = 0
			page_name = page.get('name')
			page_today = Facebook_page_data(username = username, likes=likes, page_name=page_name)
			db.session.add(page_today)
			db.session.commit()
