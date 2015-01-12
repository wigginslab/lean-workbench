# ./setup-cronjob.sh

# repos and packages
# add dem repos and packages
sudo apt-get install -y python-software-properties python g++ make
sudo add-apt-repository ppa:chris-lea/node.js
sudo apt-get update
sudo apt-get install -y git apache2 libapache2-mod-wsgi postgresql postgresql-contrib nodejs libpq-dev python-dev python-virtualenv postfix
sudo a2enmod wsgi
npm install -g grunt-cli


# brass tacks
mkdir /var/www
cd /var/www
git clone https://github.com/wigginslab/lean-workbench
cd lean-workbench
virtualenv virtualenv
. venv/bin/activate
virtualenv
pip install -r "requirements.txt"
