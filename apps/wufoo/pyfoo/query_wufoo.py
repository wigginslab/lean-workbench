import os
from pyfoo import PyfooAPI

wufoo_api_key= os.getenv("wufoo_api_key")
wufoo_account = os.getenv("wufoo_account")
wufoo_api = PyfooAPI(wufoo_account, wufoo_api_key)
print wufoo_api
