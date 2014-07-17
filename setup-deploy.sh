# deploy-server.sh

# add dem repos and packages
sudo add-apt-repository ppa:chris-lea/node.js
sudo apt-get update
sudo apt-get install -y git libapache2-mod-wsdi postgresql postgresql-contrib python-software-properties python g++ make nodejs libpq-dev python-dev npm
sudo a2enmod wsgi
npm install -g grunt-cli

# brass tacks
mkdir /var/www
cd /var/www
git clone https://github.com/wigginslab/lean-workbench
cd /var/www/lean-workbench
sudo pip install virtualenv

# turn on virtualenv
virtualenv virtualenv. venv/bin/activate
virtualenv
pip install -r "requirements.txt"
npm install .
grunt sass
cp apache/LWB /etc/apache2/sites-available/LWB

# kick server over
sudo service apache2 restart
