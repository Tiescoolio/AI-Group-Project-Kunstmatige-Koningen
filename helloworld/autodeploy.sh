#!/bin/sh
echo "Shell script for automatically deploying this project to App Engine."
echo "Please respond to the prompts as they come up."

HUPROJECTNAME=`date +"%Y%m%d%H%M%S"`
HUPROJECTNAME="huwebshop-$HUPROJECTNAME"
# echo $HUPROJECTNAME
gcloud projects create $HUPROJECTNAME --set-as-default
gcloud app create --project=$HUPROJECTNAME --region=europe-west
gcloud app deploy

echo "Script completed."