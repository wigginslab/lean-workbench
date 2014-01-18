lean-workbench
=========

lean-workbench is an analytics tool for early staged startups and NSF Innovation Corps projects.


Version
-

0.1

Tech
-----------

lean-workbench uses a number of open source projects to work properly:

* Python- an awesome scripting language
* Flask - a lean python web framework
* Flask-Sqlalchemy- a Flask SQL database wrapper
* Postgresql- A SQL database
* HTML5Boilerplate
 
Installation
--------------

```
git clone https://github.com/wigginslab/lean-workbench
cd lean-workbench
sudo pip install virtualenv
virtualenv venv
 . venv/bin/activate # whenever you want to work on the project, start by activating virtualenv
 pip install -r "requirements.txt"
python lean_workbench/manage.py create_db
python lean_workbench/manage.py runserver 
```
Configuration
--------------------
The following variables must be set in an object called UserConfig in lean_workbench/user_config.py

* DB_URL- url to a sqlalchemy compatible database
* SECRET - secret for hashing

For each of these APIs you want to use

* CRUNCHBASE KEY - API key for crunchbase
* PATH - path to application on server (so it can be added to python path within application)
* WUFOO_API_TOKEN
* WUFOO_ACCOUNT
* ANGELLIST_CLIENT_ID
* ANGELLIST_CLIENT_SECRET
* ANGELLIST_CALLBACK_URL
* TWITTER_APP_KEY
* TWITTER_APP_SECRET
* TWITTER_CALLBACK_URL
* FACEBOOK_APP_ID
* FACEBOOK_APP_SECRET

Example lean_workbench/user_config.py
```
class UserConfig(Object):
    FACEBOOK_APP_ID = '43543534534'
    ...
```

Styling
----
Sass files in the lean_workbench/sass folder are compiled to css in the lean_workbench/sass folder by running
```
grunt sass
```

Quirks
----
* For angular template variables use 
```
[[ template_variable ]]
```
Instead of 
```
{{ template_variable }}
```
For jinga compatiblity so jinga can pass in CSRF tokens.

License
-

MIT

Copyright (C) 2014 Jennifer Rubinovitz

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHOR(S) BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

Except as contained in this notice, the name of the author(s) shall not be used in advertising or otherwise to promote the sale, use or other dealings in this Software without prior written authorization from those author(s).
