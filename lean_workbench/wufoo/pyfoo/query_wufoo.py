import os
from pyfoo import PyfooAPI

wufoo_api_key= os.getenv("wufoo_api_key")
wufoo_account = os.getenv("wufoo_account")
wufoo_api = PyfooAPI(wufoo_account, wufoo_api_key)
print wufoo_api

for form in wufoo_api.forms:
    print '%s (%s)' % (form.Name, form.entry_count)

for report in wufoo_api.reports:
    print '%s (%s)' % (report.Name, report.entry_count)

for user in api.users:
    print '%s (%s)' % (report.Name, report.entry_count)

contact_form = wufoo_api.forms[0]
email_field = contact_form.get_field('Email')    
entries = contact_form.get_entries() # By default this returns 100 entries sorted by DateCreated descending
for entry in entries: 
    print entry[email_field.ID]

entry = entries[0]
for field in contact_form.fields:
    if field.SubFields:
        for subfield in field.SubFields:
            print '%s: %s' % (subfield.Label, entry[subfield.ID])
    else:
        print '%s: %s' % (field.Title, entry[field.ID])
