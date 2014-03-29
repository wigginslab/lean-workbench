import sys
sys.path.append('..')
from twitter.twitter_mine import *
from google_analytics.ga_mine import *
from flask import current_app
import os


def mine_new_user(username):
	# get twitter keyword tracking
	track_keywords(username=username)
	# get GA visits
	mine_visits(username=username)

def mine_all_users():
	# get twitter keyword tracking
	track_keywords()
	# get GA visits
	mine_visits()