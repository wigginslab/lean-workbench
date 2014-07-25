# setup-dev.sh

# packages first
sudo add-apt-repository ppa:chris-lea/node.js
sudo apt-get update
sudo apt-get install -y python-software-properties python g++ make nodejs postgresql postgresql-contrib libpq-dev python-dev npm
sudo pip install virtualenv
npm install -g grunt-cli

# brass tacks
mkdir /var/www
cd /var/www
git clone https://github.com/wigginslab/lean-workbench
cd /var/www/lean-workbench

# turn on virtualenv
virtualenv virtualenv. venv/bin/activate 
virtualenv
pip install -r "requirements.txt"
npm install .
grunt sass

# fire db & server
python lean_workbench/manage.py create_db
python lean_workbench/manage.py runserver