from algorithms.algorithm_popularity import popularity_algorithm
from algorithms.utils import connect_to_db
from flask import Flask, request, session, render_template, redirect, url_for, g
from flask_restful import Api, Resource, reqparse
import os
from pymongo import MongoClient
from dotenv import load_dotenv

import pprint as pp

app = Flask(__name__)
api = Api(app)

# We define these variables to (optionally) connect to an external MongoDB
# instance.
env_vals = ["MNOGODBUSER", "MONGODBPASSWORD", "MONGODBSERVER"]
db_string = 'mongodb+srv://{0}:{1}@{2}/test?retryWrites=true&w=majority'

# Since we are asked to pass a class rather than an instance of the class to the
# add_resource method, we open the connection to the database outside of the 
# Recom class.
load_dotenv()
if os.getenv(env_vals[0]) is not None:
    env_vals = list(map(lambda x: str(os.getenv(x)), env_vals))
    client = MongoClient(db_string.format(*env_vals))
else:
    client = MongoClient()
database = client.huwebshop 

class Recom(Resource):
    """ This class represents the REST API that provides the recommendations for
    the webshop. At the moment, the API simply returns a random set of products
    to recommend."""

    def __init__(self):
        self.cursor = connect_to_db().cursor()

    def get(self, profile_id, count, r_type, page_path):
        """ This function represents the handler for GET requests coming in
        through the API. It currently returns a random sample of products. """
        prod_ids = self.run_recommendations(count, r_type, page_path)
        return prod_ids, 200

    def run_recommendations(self, count, r_type, page_path):
        if r_type == "popular":  # change this plz to popular
            prod_ids = popularity_algorithm(self.cursor, count, page_path)
        else:
            rand_cursor = database.products.aggregate([{'$sample': {'size': count}}])
            prod_ids = list(map(lambda x: x['_id'], list(rand_cursor)))

        return prod_ids

# This method binds the Recom class to the REST API, to parse specifically
# requests in the format described below.
api.add_resource(Recom, "/<string:profile_id>/<int:count>/<string:r_type>/<path:page_path>")
