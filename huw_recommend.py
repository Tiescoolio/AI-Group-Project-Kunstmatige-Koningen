from algorithms.simple_algorithm.algorithm_popularity import PopularityAlgorithm
from algorithms.utils import connect_to_db
from flask import Flask, request, session, render_template, redirect, url_for, g, jsonify
from flask_restful import Api, Resource, reqparse
import os
from pymongo import MongoClient
from dotenv import load_dotenv
import urllib.parse
import pprint

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

decode_args = reqparse.RequestParser()
decode_args.add_argument("codes", type=dict, help="plz work")

class Recom(Resource):
    """ This class represents the REST API that provides the recommendations for
    the webshop. At the moment, the API simply returns a random set of products
    to recommend."""
    url = "http://127.0.0.1:5000"

    def __init__(self):
        self.cursor = connect_to_db().cursor()

    def decode_category(self, c) -> str:
        """ This helper function decodes any category with urllib"""
        return urllib.parse.unquote_plus(c)

    def format_page_path(self, path) -> tuple:
        """Formats the page path into a tuple of up to four categories.

        Args:
            path (str): The path of the page.

        Returns:
            tuple: Tuple containing up to four categories, with missing categories filled with None.
        """
        # paths = path.replace("producten/", "")[:-1]
        cats = path.split("/")[:-1]
        cats = [self.decode_category(c) for c in cats[1:]]
        for i in range(4 - len(cats)):
            cats.append(None)
        return tuple(cats)

    def get(self, profile_id, count, r_type, page_path):
        """ This function represents the handler for GET requests coming in
        through the API. It currently returns a random sample of products.

        Args:
            profile_id (int): The ID of the user's profile.
            count (int): The number of products to return.
            r_type (str): The type of recommendation.
            page_path (str): The path of the page.

        Returns:
            tuple : Depending on the recommendation type, it returns different values.
                A tuple containing product IDs (amount defined by count) and status code 200
        """
        cats = self.format_page_path(page_path)
        if r_type == "popular":  # simple alg for the products categories
            pop_app = PopularityAlgorithm(count, self.cursor, cats)
            return pop_app.popularity_algorithm(cats[0], cats[1]), 200
        elif r_type == "similar":  # alg 1 for the product details
            # Not implemented
            return "Not Implemented", 501
        elif r_type == "combination":  # alg 2 for the shopping cart
            # Not implemented
            return "Not Implemented", 501
        elif r_type == "personal":  # alg 3 for the homepage
            # Not implemented
            return "Not Implemented", 501

        # Return random products IDs for testing pages.
        rand_cursor = database.products.aggregate([{'$sample': {'size': count}}])
        prod_ids = list(map(lambda x: x['_id'], list(rand_cursor)))
        return prod_ids, 200

# This method binds the Recom class to the REST API, to parse specifically
# requests in the format described below.
api.add_resource(Recom, "/<string:profile_id>/<int:count>/<string:r_type>/<path:page_path>")
