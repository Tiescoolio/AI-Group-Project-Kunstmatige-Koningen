#!/bin/sh
echo "Shell script for automatically running this project on a local environment."
echo "Please respond to the prompts as they come up."
echo "Please provide the name of the cluster you want to connect to (e.g. huwebshoptest-neick.mongodb.net):"
read -p 'Cluster name: ' MONGODBSERVER
echo "Please provide your username for this cluster (e.g. accessUser):"
read -p 'Username: ' MONGODBUSER
echo "Please provide your password for this cluster:"
read -sp 'Password: ' MONGODBPASSWORD
rm -f .env
echo "MONGODBSERVER=$MONGODBSERVER" >> .env
echo "MONGODBUSER=$MONGODBUSER" >> .env
echo "MONGODBPASSWORD=$MONGODBPASSWORD" >> .env
export FLASK_APP=huwclass.py
python -m flask run