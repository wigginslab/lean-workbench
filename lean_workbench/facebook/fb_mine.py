from facebook_model import FacebookPageData, FacebookModel, db
import facebook_module as facebook

def mine_fb_page_data(username=None):
	# if only for one user
	if username:
		fb_user = FacebookModel.query.filter_by(username=username).order_by('-id').first()
		users = [fb_user]
                fb_user.active = True
                db.session.add(fb_user)
                db.session.commit()

	else:
		users = FacebookModel.query.all()

	for user in users:
		oauth_access_token = user.access_token
		username = user.username
		if oauth_access_token:
                    try:
		        # get graph
			graph = facebook.GraphAPI(oauth_access_token)
			# get pages
			pages = graph.request('me/accounts')
			page_access_token = pages['data'][0]['access_token']
			# get likes per page for today
			page_id = pages['data'][0]['category_list'][0]['id']
			page = graph.request(str(page_id)+'?access_token='+page_access_token)
			print page
			try:
				likes = page['likes']
			except:
				likes = 0
			page_name = page.get('name')
			page_today = FacebookPageData(username = username, likes=likes, page_name=page_name)
			db.session.add(page_today)
			db.session.commit()
                    except:
                        print 'error in fb_mine.py for %s' %(user.username)
