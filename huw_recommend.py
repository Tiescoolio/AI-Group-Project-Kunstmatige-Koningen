from algorithms.simple_algorithm.algorithm_popularity import PopularityAlgorithm
from algorithms.similar_costumer_products_algorithm.most_comparable_products import most_comparable_products as combination_alg
from algorithms.similar_brand_algorithm.algorithm_similiar import SimilarBrand
from algorithms.discount_algorithm.algortihm_discount import get_recommendation
from algorithms.utils import connect_to_db, time_function
from algorithms.algorithms_analysis.plot_performance import plot_avg
from flask import Flask, request, session, render_template, redirect, url_for, g, jsonify
from flask_restful import Api, Resource, reqparse
import os, urllib.parse, pprint, timeit, time
from pymongo import MongoClient
from dotenv import load_dotenv


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

    def __init__(self):
        self.cursor = connect_to_db().cursor()
        self.pop_app = PopularityAlgorithm()
        self.brand_app = SimilarBrand()
        self.shopping_cart_ids = []

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
        split_path = path.split("/")
        page_type = split_path[0]

        # Return all the categories if the page "producten/"
        if page_type == "producten":
            cats = [self.decode_category(c) for c in split_path[:-1][1:]]
            for i in range(4 - len(cats)):
                cats.append(None)
            return tuple(cats)
        # Return the product ID if the page "productdetail/"
        elif page_type == "productdetail":
            page_data = [self.decode_category(c) for c in split_path[1:-1]]
            for i in range(5 - len(page_data)):
                page_data.append(None)
            return tuple(page_data)

    def get(self, profile_id, count, r_type, page_path, shopping_cart):
        """ This function represents the handler for GET requests coming in
        through the API. It currently returns a random sample of products.

        Args:
            profile_id (int): The ID of the user's profile.
            count (int): The number of products to return.
            r_type (str): The type of recommendation.
            page_path (str): The path of the page.
            shopping_cart (str): The path with the IDs form the shoppingcart.
        Returns:
            tuple : Depending on the recommendation type, it returns different values.
                A tuple containing product IDs (amount defined by count) and status code 200
        """

        self.shopping_cart_ids = shopping_cart.split("-")[1:]
        page_data = self.format_page_path(page_path)
        if r_type == "popular":  # simple alg for the products categories
            return self.pop_app.popularity_algorithm(page_data, self.cursor, count), 200
        elif r_type == "similar":  # alg 1 for the product details
            return self.brand_app.similar_brand(page_data, self.cursor, count), 200
        elif r_type == "combination":  # alg 2 for the shopping cart
            return combination_alg(self.shopping_cart_ids, self.cursor), 200
        elif r_type == "personal":  # alg 3 for the homepage
            return get_recommendation(profile_id, self.cursor), 200
        else:
            return None, 404


# This method binds the Recom class to the REST API, to parse specifically
# requests in the format described below.
api.add_resource(Recom, "/<string:profile_id>/<int:count>/<string:r_type>/<path:page_path>/<string:shopping_cart>/")
