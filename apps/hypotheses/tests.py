import urllib
import urllib2
import json
from flask import session

username = "test_user"
session['username'] = username

def ajaxRequest(values=None, url=None):
	"""
	Makes an ajax request. If values == POST, if not == GET.

	values- data values (dict)
	url - endpoint(string)
	"""
	if values: #then POST
		print 'post request'
		data = urllib.urlencode(values)
		print data
		req = urllib2.Request(url, data)
	else: #then GET
		print 'get request'
		req = urllib2.Request(url)
	f = urllib2.urlopen(req)
	response = f.read()
	f.close()
	return response	

def test_add_hypothesis():
	data = {"goal":"awesome",
			"username":username,
			"event":"nada", 
			"google_analytics":"/endpoint", 
			"wufoo":"www.wufoourl.com"
			}
	response = ajaxRequest(data,"/api/v1/hypotheses")
	print response
	
def test_get_all_hypotheses():
	response = ajaxRequest("api/v1/hypotheses")
	print response

def test_get_a_hypothesis():
	pass		

test_get_all_hypotheses()
test_add_hypothesis()
test_get_a_hypothesis()

