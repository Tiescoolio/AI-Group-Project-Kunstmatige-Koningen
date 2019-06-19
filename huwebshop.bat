rem this file doesn't work because the files are on a network drive
rem only used for reference when deploying to a different system
mongoimport --db huwebshop --collection products --file .\datasets\bslps.json --jsonArray
set FLASK_APP=huwebshop.py
python -m flask run