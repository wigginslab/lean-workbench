import urllib
import urllib2
import json

def ajaxRequest(url=None,values=None):
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
