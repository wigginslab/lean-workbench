import angellist
import os

al = angellist.AngelList()
al.client_id = os.getenv('angelist_id') 
auth_url = al.getAuthorizeURL()
print auth_url

