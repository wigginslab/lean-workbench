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
python create_db.py
```
Environment Variables
--------------------
The following variables must be set on your machine:

* db_url- url to a sqlalchemy compatible database
* port- port from which you wish the serve the app
* mail_server - mail server (e.g. smtp.example.com)
* mail_username - username for mail server
* mail_password- password for mail server
* mail_port - port for mail server

For each of these APIs you want to use

* crunchbase_key - API key for crunchbase
* path - path to application on server (so it can be added to python path within application)
*mixpanel_api_key - if using mixpanel
* mixpanel_api_secret- ...
* mixpanel_token - ..
* wufoo_api_token 
* wufoo_account
Running the Application
---------------------------
Set the environment variables then:
```
python app.py
```

License
-

MIT

Copyright (C) 2013 Jennifer Rubinovitz

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHOR(S) BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

Except as contained in this notice, the name of the author(s) shall not be used in advertising or otherwise to promote the sale, use or other dealings in this Software without prior written authorization from those author(s).
