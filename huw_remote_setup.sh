#!/bin/sh
echo "Shell script for automatically running this project on a local environment."
echo "Please respond to the prompts as they come up."
echo "Please provide the name of the cluster you want to connect to (e.g. huwebshoptest-neick.mongodb.net):"
read -p 'Cluster name: ' MONGODBSERVER
echo "Please provide your username for this cluster (e.g. accessUser):"
read -p 'Username: ' MONGODBUSER
echo "Please provide your password for this cluster:"
read -sp 'Password: ' MONGODBPASSWORD
echo "Please provide the web address for the external recommendation service (e.g. http://127.0.0.1:5001):"
read -p 'External service: ' RECOMADDRESS
rm -f .env
echo "MONGODBSERVER=$MONGODBSERVER" >> .env
echo "MONGODBUSER=$MONGODBUSER" >> .env
echo "MONGODBPASSWORD=$MONGODBPASSWORD" >> .env
echo "RECOMADDRESS=$RECOMADDRESS" >> .env
export FLASK_APP=huw.py
python -m flask run