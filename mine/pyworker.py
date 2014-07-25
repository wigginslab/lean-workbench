import pymongo
import requests
from iron_mq import IronMQ
import os

mongo_url = os.getenv("MONGO_URL")
mongo_user = os.getenv("MONGO_USER")
mongo_password = os.getenv("MONGO_PASSWORD")
schema_name = os.getenv("SCHEMA_NAME")

project_id = os.getenv("IRON_PROJECT_ID")
token = os.getenv("IRON_TOKEN")

