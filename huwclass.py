from flask import Flask, request, session, render_template, redirect, url_for, g
import random, os, json, huwutil, urllib.parse
from pymongo import MongoClient
from dotenv import load_dotenv

# We load the environment variables, if they exist, from the .env file in this
# folder.
load_dotenv()
# The secret key used for session encryption is randomly generated every time
# the server is started up. This means all session data (including the 
# shopping cart) is erased between server instances.
app = Flask(__name__)
app.secret_key = os.urandom(16)


class HUWebshop(object):
    """ This class combines all logic behind the HU Example Webshop project. 
    Note that all rendering is performed within the templates themselves."""

    app = None
    client = None
    database = None

    envnames = ["MONGODBUSER","MONGODBPASSWORD","MONGODBSERVER"]
    dbstring = 'mongodb+srv://{0}:{1}@{2}/test?retryWrites=true&w=majority'

    categoryindex = None
    catlevels = ["category","sub_category","sub_sub_category","sub_sub_sub_category"]
    catencode = {}
    catdecode = {}
    mainmenucount = 8
    mainmenuitems = None

    paginationcounts = [6, 12, 24, 0]

    def __init__(self, app):
        """ Within this constructor, we establish a connection with the database
        and perform necessary setup of the database (if applicable) and menu."""
        self.app = app

        # Depending on whether environment variables have been set, we connect
        # to a local or remote instance of MongoDB.
        load_dotenv()
        if os.getenv(self.envnames[0]) is not None:
            self.envnames = list(map(lambda x: str(os.getenv(x)), self.envnames))
            self.client = MongoClient(self.dbstring.format(*self.envnames))
        else:
            self.client = MongoClient()
        self.database = self.client.huwebshop 

        # Once we have a connection to the database, we check to see whether it
        # has a category index prepared; if not, we have a function to make it.
        if "categoryindex" not in self.database.collection_names() or self.database.categoryindex.count_documents({}) == 0:
            self.createcategoryindex()

        # We retrieve the categoryindex from the database when it is set.
        self.categoryindex = self.database.categoryindex.find_one({}, {'_id' : 0})

        # In order to save time in future, we flatten the category index once,
        # and translate all values to and from an encoded, URL-friendly, legible
        # format.
        catlist = self.flattendict(self.categoryindex)
        for cat in catlist:
            enc_cat = self.encodecategory(cat)
            self.catencode[cat] = enc_cat
            self.catdecode[enc_cat] = cat

        # Since the main menu can't show all the category options at once in a
        # legible manner, we choose to display a set number with the greatest 
        # number of associated products.
        countlist = list(map(lambda x, y: (y['_count'], x), self.categoryindex.keys(), self.categoryindex.values()))
        countlist.sort(reverse=True)
        self.mainmenuitems = [x[1] for x in countlist[0:self.mainmenucount]]

    def createcategoryindex(self):
        """ Within this function, we compose a nested dictionary of all 
        categories that occur within the database's products collection, and 
        save it to the categoryindex collection. """
        pcatentries = self.database.products.find({},self.catlevels)
        index = {}
        for entry in pcatentries:
            self.reccatindex(index, entry, 0, len(self.catlevels)-1)
        for k, v in index.items():
            self.reccatcount(k, v, 0, len(self.catlevels)-1)
        self.database.categoryindex.insert_one(index)

    def reccatindex(self,d,e,l,m):
        """ This subfunction of createcategoryindex() sets up the base structure
        (tree) of the categories and subcategories, leaving leaves as empty 
        dicts."""
        if l > m:
            return
        t = self.catlevels[l]
        if t in e and e[t] is not None and type(e[t]) != list and e[t] not in d:
            d[e[t]] = {}
        if t in e and e[t] is not None and type(e[t]) != list and e[t] in d:
            self.reccatindex(d[e[t]],e,l+1,m)

    def reccatcount(self,k,v,l,m):
        """ This subfunction of createcategoryindex() adds the number of 
        documents associated with any (sub)category to its dictionary as the
        _count property. """
        if l > m:
            return
        if isinstance(v, dict):
            for k2, v2 in v.items():
                self.reccatcount(k2, v2, l+1, m)
        if k[:1] != "_":
            v['_count'] = self.database.products.count_documents({self.catlevels[l]:k})

    def flattendict(self,d,s=[]):
        """ This helper function provides a list of all keys that exist within a
        nested dictionary. """
        for k, v in d.items():
            # Note that the condition below prevents the _count property from
            # being added to the list over and over again.
            if k[:1] != "_":
                s.append(k)
                if isinstance(v, dict) and v:
                    s = self.flattendict(v, s)
        return s

    def encodecategory(self,c):
        """ This helper function encodes any category name into a URL-friendly
        string, making sensible and human-readable substitutions. """
        c = c.lower()
        c = c.replace(" ","-")
        c = c.replace(",","")
        c = c.replace("'","")
        c = c.replace("&","en")
        c = c.replace("ë","e")
        c = c.replace("=","-is-")
        c = c.replace("%","-procent-")
        c = c.replace("--","-")
        c = urllib.parse.quote(c)
        return c


huw = HUWebshop(app)

# Decorators to process
'''
@app.before_request
@app.route('/change-profile-id', methods=['POST'])
@app.route('/dynamic-shopping-cart', methods=['POST'])
@app.route('/producten/pagination-change/<int:pagval>', methods=['POST'])
@app.route('/add-to-shopping-cart/<int:productid>', methods=['POST'])
@app.route('/')
@app.route('/producten/')
@app.route('/producten/<cat1>')
@app.route('/producten/<cat1>/<cat2>')
@app.route('/producten/<cat1>/<cat2>/<cat3>')
@app.route('/producten/<cat1>/<cat2>/<cat3>/<cat4>')
@app.route('/productdetail/<int:productid>')
@app.route('/winkelmand')
@app.errorhandler(404)
@app.errorhandler(405)
'''