from flask import Flask, request, session, render_template, redirect, url_for, g, jsonify
import random, os, json, urllib.parse, requests
from flask_restful import Api, Resource
from pymongo import MongoClient
from dotenv import load_dotenv
from bson.objectid import ObjectId
# from urllib.parse import quote
import pprint

# id: "33698-bl39/42" doesn't work cursed _id how! all Bon Giorno products

# The secret key used for session encryption is randomly generated every time
# the server is started up. This means all session data (including the 
# shopping cart) is erased between server instances.
app = Flask(__name__)
api = Api(app)
app.secret_key = os.urandom(16)

class HUWebshop(object):
    """ This class combines all logic behind the HU Example Webshop project. 
    Note that all rendering is performed within the templates themselves."""

    app = None
    client = None
    database = None

    env_vals = ["MONGODBUSER", "MONGODBPASSWORD", "MONGODBSERVER", "RECOMADDRESS"]
    db_string = 'mongodb+srv://{0}:{1}@{2}/test?retryWrites=true&w=majority'
    rec_ser_address = "http://127.0.0.1:5001"

    category_index = None
    fall_back_threshold = 2
    cat_levels = ["category", "sub_category", "sub_sub_category", "sub_sub_sub_category"]
    cat_encode = {}
    cat_decode = {}
    main_menu_count = 8
    main_menu_items = None

    pagination_counts = [8, 16, 32, 0]

    product_fields = ["name", "price.selling_price", "properties.discount", "images"]

    recommendation_types = {
        'popular': "Meest verkochte producten in de categorie ",
        'similar': "Soortgelijke producten van",
        'combination': 'Combineert goed met',
        'behaviour': 'Passend bij uw gedrag',
        'personal': 'Soortelijke producten die je al eerder hebt bekeken',
        "popular_all": "Meest gekochte producten"
    }

    """ ..:: Initialization and Category Index Functions ::.. """

    def __init__(self, app):
        """ Within this constructor, we establish a connection with the database
        and perform necessary setup of the database (if applicable) and menu."""
        self.app = app
        # Depending on whether environment variables have been set, we connect
        # to a local or remote instance of MongoDB, and a default or non-default
        # external recommendation service.
        load_dotenv()
        env_dict = {}
        if os.getenv(self.env_vals[0]) is not None:
            for val in self.env_vals:
                env_dict[val] = str(os.getenv(val))
            if env_dict["MONGODBUSER"] and env_dict["MONGODBPASSWORD"] and env_dict["MONGODBSERVER"]:
                self.client = MongoClient(self.db_string.format(env_dict["MONGODBUSER"], env_dict["MONGODBPASSWORD"], env_dict["MONGODBSERVER"]))
            else:
                self.client = MongoClient()
            if env_dict["RECOMADDRESS"]:
                self.rec_ser_address = env_dict["RECOMADDRESS"]
        else:
            self.client = MongoClient()
        self.database = self.client.huwebshop 

        # Once we have a connection to the database, we check to see whether it
        # has a category index prepared; if not, we have a function to make it.
        if "category_index" not in self.database.list_collection_names() or self.database.category_index.count_documents({}) == 0:
            self.create_category_index()

        # We retrieve the categoryindex from the database when it is set.
        self.category_index = self.database.category_index.find_one({}, {'_id' : 0})
        # In order to save time in future, we flatten the category index once,
        # and translate all values to and from an encoded, URL-friendly, legible
        # format.
        cat_list = self.flatten_dict(self.category_index)
        for cat in cat_list:
            enc_cat = self.encode_category(cat)
            self.cat_encode[cat] = enc_cat
            self.cat_decode[enc_cat] = cat

        # Since the main menu can't show all the category options at once in a
        # legible manner, we choose to display a set number with the greatest 
        # number of associated products.
        count_list = list(map(lambda x, y: (y['_count'], x), self.category_index.keys(), self.category_index.values()))
        count_list.sort(reverse=True)
        self.main_menu_items = [x[1] for x in count_list[0:self.main_menu_count]]

        # Finally, we here attach URL rules to all pages we wish to render, to
        # make the code self-contained; although the more common decorators do
        # the same thing, we wish to have this class contain as much logic as
        # possible.
        self.app.before_request(self.check_session)
        self.app.add_url_rule('/', 'index', self.render_packet_template)
        self.app.add_url_rule('/producten/', 'producten-0', self.product_page)
        self.app.add_url_rule('/producten/<cat1>/', 'producten-1', self.product_page)
        self.app.add_url_rule('/producten/<cat1>/<cat2>/', 'producten-2', self.product_page)
        self.app.add_url_rule('/producten/<cat1>/<cat2>/<cat3>/', 'producten-3', self.product_page)
        self.app.add_url_rule('/producten/<int:page>/', 'producten-4', self.product_page)
        self.app.add_url_rule('/producten/<cat1>/<int:page>/', 'producten-5', self.product_page)
        self.app.add_url_rule('/producten/<cat1>/<cat2>/<int:page>/', 'producten-6', self.product_page)
        self.app.add_url_rule('/producten/<cat1>/<cat2>/<cat3>/<int:page>/', 'producten-7', self.product_page)
        self.app.add_url_rule('/producten/<cat1>/<cat2>/<cat3>/<cat4>/<int:page>/', 'producten-8', self.product_page)
        self.app.add_url_rule('/productdetail/<product_id>/', 'productdetail', self.product_detail)
        self.app.add_url_rule('/winkelmand/', 'winkelmand', self.shoppingcart)
        self.app.add_url_rule('/categorieoverzicht/', 'categorieoverzicht', self.category_overview)
        self.app.add_url_rule('/change-profile-id', 'profielid', self.change_profile_id, methods=['POST'])
        self.app.add_url_rule('/add-to-shopping-cart', 'toevoegenaanwinkelmand', self.add_to_shopping_cart, methods=['POST'])
        self.app.add_url_rule('/producten/pagination-change', 'aantalperpaginaaanpassen', self.change_pagination_count, methods=['POST'])

    def create_category_index(self):
        """ Within this function, we compose a nested dictionary of all 
        categories that occur within the database's products collection, and 
        save it to the categoryindex collection. """
        pcat_entries = self.database.products.find({}, self.cat_levels)
        index = {}
        for entry in pcat_entries:
            self.rec_cat_index(index, entry, 0, len(self.cat_levels) - 1)
            # pprint.pp(self.rec_cat_index(index, entry, 0, len(self.cat_levels) - 1))
        for k, v in index.items():
            self.rec_cat_count(k, v, 0, len(self.cat_levels) - 1)
        self.database.category_index.insert_one(index)

    def rec_cat_index(self, d, e, l, m):
        """ This subfunction of createcategoryindex() sets up the base structure
        (tree) of the categories and subcategories, leaving leaves as empty 
        dicts."""
        if l > m:
            return
        t = self.cat_levels[l]
        if t in e and e[t] is not None and type(e[t]) != list and e[t] not in d:
            d[e[t]] = {}
        if t in e and e[t] is not None and type(e[t]) != list and e[t] in d:
            self.rec_cat_index(d[e[t]], e, l + 1, m)

    def rec_cat_count(self, k, v, l, m):
        """ This subfunction of createcategoryindex() adds the number of 
        documents associated with any (sub)category to its dictionary as the
        _count property. """
        if l > m:
            return
        if isinstance(v, dict):
            for k2, v2 in v.items():
                self.rec_cat_count(k2, v2, l + 1, m)
        if k[:1] != "_":
            v['_count'] = self.database.products.count_documents({self.cat_levels[l]:k})

    """ ..:: Helper Functions ::.. """

    def flatten_dict(self, d, s=[]):
        """ This helper function provides a list of all keys that exist within a
        nested dictionary. """
        for k, v in d.items():
            # Note that the condition below prevents the _count property from
            # being added to the list over and over again.
            if k[:1] != "_":
                s.append(k)
                if isinstance(v, dict) and v:
                    s = self.flatten_dict(v, s)
        return s

    def encode_category(self, c):
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

    def encode_category_urllib(self, c) -> str:
        """ This helper function encodes any category with urllib,
        so it can later be decoded"""
        return urllib.parse.quote_plus(c)

    def prep_product(self, p):
        """ This helper function flattens and rationalizes the values retrieved
        for a product block element. """
        # pp.pp(p)

        r = {}
        r['name'] = p['name']
        r['price'] = p['price']['selling_price']
        r['price'] = str(r['price'])[0:-2]+",-" if r['price'] % 100 == 0 else str(r['price'])[0:-2]+","+str(r['price'])[-2:]
        if r['price'][0:1] == ",":
            r['price'] = "0"+r['price']
        if p['properties']['discount'] is not None:
            r['discount'] = p['properties']['discount'] 
        r['smallimage'] = p['images'][0][0] # TODO: replace this with actual images!
        r['bigimage'] = p['images'][0][1]  # TODO: replace this with actual images!
        r['id'] = p['_id']
        return r

    def shopping_cart_count(self):
        """ This function returns the number of items in the shopping cart. """
        return sum(list(map(lambda x: x[1], session['shopping_cart'])))

    """ ..:: Session and Templating Functions ::.. """

    def check_session(self):
        """ This function sets certain generally used session variables when
        those have not yet been set. This executes before every request, but
        will most likely only make changes once. """
        if ('session_valid' not in session) or (session['session_valid'] != 1):
            session['shopping_cart'] = []
            session['items_per_page'] = self.pagination_counts[0]
            session['session_id'] = self.database.sessions.find_one({})['buid'][0]
            session['profile_id'] = str(self.database.profiles.find_one({})['_id'])
            session['session_valid'] = 1

    def render_packet_template(self, template="homepage.html", packet={}):
        """ This helper function adds all generally important variables to the
        packet sent to the templating engine, then calss upon Flask to forward
        the rendering to Jinja. """
        packet['categoryindex'] = self.category_index
        packet['mainmenulist'] = self.main_menu_items
        packet['categories_encode'] = self.cat_encode
        packet['categories_decode'] = self.cat_decode
        packet['paginationcounts'] = self.pagination_counts
        packet['items_per_page'] = session['items_per_page']
        packet['session_id'] = session['session_id']
        packet['profile_id'] = session['profile_id']
        packet['shopping_cart'] = session['shopping_cart']
        packet['shopping_cart_count'] = self.shopping_cart_count()
        if template == "homepage.html":
            r_products = self.recommendations(4, list(self.recommendation_types.keys())[4],
                                              "viewed-before/")
            r_string = list(self.recommendation_types.values())[4]
            if len(r_products) <= self.fall_back_threshold:
                r_products, r_string = self.fall_back()
            packet['r_type'] = list(self.recommendation_types.keys())[4]
            packet['r_string'] = r_string
            packet['r_products'] = r_products
        return render_template(template, packet=packet)

    """ ..:: Recommendation Functions ::.. """

    def recommendations(self, count, r_type, page_path=None):
        """ This function returns the recommendations from the provided page
        and context, by sending a request to the designated recommendation
        service. At the moment, it only transmits the profile ID and the number
        of expected recommendations; to have more user information in the REST
        request, this function would have to change."""
        shopping_cart_ids = [i[0] for i in session['shopping_cart']]
        if len(shopping_cart_ids) >= 1:
            shopping_cart_path = "ids-"+("-".join(shopping_cart_ids))
        else:
            shopping_cart_path = "ids"
        url = (f"{self.rec_ser_address}/{session['profile_id']}/{count}/{r_type}/{page_path}/{shopping_cart_path}/")
        resp = requests.get(url)
        if resp.status_code == 200:
            recs = eval(resp.content.decode())
            queryfilter = {"_id": {"$in": recs}}
            query_cursor = self.database.products.find(queryfilter, self.product_fields)
            result_list = list(map(self.prep_product, list(query_cursor)))
            return result_list
        return []

    def fall_back(self, page_path="producten/"):
        """ This function fall back on the given alg i"""
        r_products = self.recommendations(4, list(self.recommendation_types.keys())[0], page_path)
        r_string = f"{list(self.recommendation_types.values())[5]}"
        return r_products, r_string

    """ ..:: Full Page Endpoints ::.. """

    def product_page(self, cat1=None, cat2=None, cat3=None, cat4=None, page=1):
        """ This function renders the product page template with the products it
        can retrieve from the database, based on the URL path provided (which
        corresponds to product categories). """
        cat_list = [cat1, cat2, cat3, cat4]
        queryfilter = {}
        no_nones_cats = []
        for k, v in enumerate(cat_list):
            if v is not None:
                queryfilter[self.cat_levels[k]] = self.cat_decode[v]
                no_nones_cats.append(self.cat_decode[v])

        query_cursor = self.database.products.find(queryfilter, self.product_fields)
        prod_count = self.database.products.count_documents(queryfilter)
        skip_index = session['items_per_page']*(page-1)
        query_cursor.skip(skip_index)
        query_cursor.limit(session['items_per_page'])

        prod_list = list(map(self.prep_product, list(query_cursor)))
        recommendation_type = list(self.recommendation_types.keys())[0]

        if len(no_nones_cats) >= 2:
            r_string_cats = f"{no_nones_cats[0]}, {no_nones_cats[1]}"
        else:
            r_string_cats = f"{no_nones_cats[0]}"

        if len(no_nones_cats) >= 1:
            page_path = "producten/"+("/".join(no_nones_cats))+"/"
        else:
            page_path = "producten/"

        r_products = self.recommendations(4, recommendation_type, page_path)
        r_string = list(self.recommendation_types.values())[0] + r_string_cats
        if r_products[0]["id"] == "25960":  # man what is this
            r_string = list(self.recommendation_types.values())[5]

        return self.render_packet_template('products.html', {
            'products': prod_list,
            'productcount': prod_count, \
            'pstart': skip_index + 1, \
            'pend': skip_index + session['items_per_page'] if session['items_per_page'] > 0 else prod_count, \
            'prevpage': page_path+str(page-1) if (page > 1) else False, \
            'nextpage': page_path+str(page+1) if (session['items_per_page']*page < prod_count) else False, \
            'r_products':r_products, \
            'r_type':recommendation_type,\
            'r_string':f"{r_string}"
            })

    def product_detail(self, product_id):
        """ This function renders the product detail page based on the product
        id provided. """
        product = self.database.products.find_one({"_id": str(product_id)})
        brand = product.get('brand', None)
        cat = product.get('category', None)
        sub_cat = product.get('sub_category', None)
        sub_sub_cat = product.get('sub_sub_category', None)

        cat_list = [cat, sub_cat, sub_sub_cat]
        no_nones_cats = [cat for cat in cat_list if cat is not None]
        recommendation_type = list(self.recommendation_types.keys())[1]
        r_string = f"{list(self.recommendation_types.values())[1]} {brand}"
        if len(no_nones_cats) >= 1:
            page_path = f"productdetail/{product_id}/{brand}/" + ("/".join(no_nones_cats)) + "/"
        else:
            page_path = f"productdetail/{product_id}/{brand}/"

        r_products = self.recommendations(4, recommendation_type, page_path)
        if len(r_products) <= self.fall_back_threshold:
            r_products, r_string = self.fall_back()

        return self.render_packet_template('productdetail.html', {
            'product':product,\
            'prepproduct':self.prep_product(product),\
            'r_products':r_products, \
            'r_type':recommendation_type,\
            'r_string': r_string
        })

    def shoppingcart(self):
        """ This function renders the shopping cart for the user."""
        i = []
        page_path = "winkelmand/"
        recommendation_type = list(self.recommendation_types.keys())[2]
        r_string = list(self.recommendation_types.values())[2]
        for tup in session['shopping_cart']:
            product = self.prep_product(self.database.products.find_one({"_id":str(tup[0])}))
            product["itemcount"] = tup[1]
            i.append(product)

        r_products = self.recommendations(4, recommendation_type, page_path)
        if len(r_products) <= self.fall_back_threshold:
            print(random.choice(list(self.category_index.keys())))
            r_products, r_string = self.fall_back(f"producten/{random.choice(list(self.category_index.keys()))}/")

        return self.render_packet_template('shoppingcart.html', {
            'itemsincart':i,\
            'r_products':self.recommendations(4, recommendation_type, page_path), \
            'r_type':recommendation_type,\
            'r_string':r_string
            })

    def category_overview(self):
        """ This subpage shows all top-level categories in its main menu. """
        return self.render_packet_template('categoryoverview.html')

    """ ..:: Dynamic AJAX Endpoints ::.. """

    def change_profile_id(self):
        """ This function checks whether the provided session ID actually exists
        and stores it in the session if it does. """
        try:
            new_profile_id = request.form.get('profile_id')
            prof_id_exists = self.database.profiles.find_one({'_id': ObjectId(new_profile_id)})
            if prof_id_exists:
                session['profile_id'] = new_profile_id
                return '{"success":true}'
            return '{"success":false}'
        except:
            return '{"success":false}'

    def add_to_shopping_cart(self):
        """ This function adds one object to the shopping cart. """
        product_id = request.form.get('product_id')
        cart_ids = list(map(lambda x: x[0], session['shopping_cart']))
        if product_id in cart_ids:
            ind = cart_ids.index(product_id)
            session['shopping_cart'][ind] = (session['shopping_cart'][ind][0], session['shopping_cart'][ind][1]+1)
        else:
            session['shopping_cart'].append((product_id, 1))
        session['shopping_cart'] = session['shopping_cart']
        return '{"success":true, "itemcount":'+str(self.shopping_cart_count())+ '}'

    def change_pagination_count(self):
        """ This function changes the number of items displayed on the product 
        listing pages. """
        session['items_per_page'] = int(request.form.get('items_per_page'))
        # TODO: add method that returns the exact URL the user should be 
        # returned to, including offset
        return '{"success":true, "refurl":"'+request.form.get('refurl')+'"}'

    # TODO: add @app.errorhandler(404) and @app.errorhandler(405)

huw = HUWebshop(app)