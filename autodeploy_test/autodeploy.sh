#!/bin/sh
echo "Shell script for automatically deploying this project to App Engine."
echo "Please respond to the prompts as they come up."

# Default project name
HUPROJECTNAME=`date +"%Y%m%d%H%M%S"`
HUPROJECTNAME="huwebshop-$HUPROJECTNAME"

# Project creation
gcloud projects create $HUPROJECTNAME --set-as-default
gcloud app create --project=$HUPROJECTNAME --region=europe-west

# Billing account and API enabling section - makes use of functions in beta!
# TODO: replace with stable versions as they arise
echo "In order to deploy this application, you have to link a billing account."
echo "Note that the gcloud methods used here are in beta, and may fail over time."
echo "The following billing accounts are associated with this user:"
gcloud beta billing accounts list
echo "Please input the full ACCOUNT_ID of the billing account you want to use:"
read BILLINGACCOUNT
gcloud beta billing projects link $HUPROJECTNAME --billing-account $BILLINGACCOUNT
gcloud services enable cloudbuild.googleapis.com

# Deploying to app engine
gcloud app deploy

# Script completed
echo "Script completed."