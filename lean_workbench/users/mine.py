import sys
sys.path.append('..')
from twitter.twitter_mine import *
from google_analytics.ga_mine import *
import os
from celery import Celery

celery_broker_url = os.getenv("CELERY_BROKER_URL")
celery = Celery('tasks', broker=celery_broker_url)

@celery.task()
def mine_new_user(username):
	# get twitter keyword tracking
	track_keywords(username=username)
	# get GA visits
	mine_visits(username=username)

@celery.task()
def mine_all_users():
	# get twitter keyword tracking
	track_keywords()
	# get GA visits
	mine_visits()