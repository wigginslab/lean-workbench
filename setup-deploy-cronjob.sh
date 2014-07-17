# ./setup-cronjob.sh

# repos and packages
sudo add-apt-repository ppa:chris-lea/node.js
sudo apt-get update
sudo apt-get install -y libapache2-mod-wsgi postgresql postgresql-contrib git python-software-properties python g++ make postfix nodejs libpq-dev python-dev
sudo a2enmod wsgi
npm install -g grunt-cli
sudo pip install virtualenv

# brass tacks
mkdir /var/www
cd /var/www
git clone https://github.com/wigginslab/lean-workbench
cd lean-workbench
virtualenv virtualenv
. venv/bin/activate
virtualenv
pip install -r "requirements.txt"

