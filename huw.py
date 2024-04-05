from flask import Flask, request, session, render_template, redirect, url_for, g
import random, os, json, urllib.parse, requests
from pymongo import MongoClient
from dotenv import load_dotenv
from bson.objectid import ObjectId
import pprint as pp

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

    env_vals = ["MONGODBUSER", "MONGODBPASSWORD", "MONGODBSERVER", "RECOMADDRESS"]
    db_string = 'mongodb+srv://{0}:{1}@{2}/test?retryWrites=true&w=majority'
    rec_ser_address = "http://127.0.0.1:5001"

    categoryindex = None
    cat_levels = ["category", "sub_category", "sub_sub_category", "sub_sub_sub_category"]
    cat_encode = {}
    cat_decode = {}
    main_menu_count = 8
    main_menu_items = None

    pagination_counts = [8, 16, 32, 0]

    product_fields = ["name", "price.selling_price", "properties.discount", "images"]

    recommendation_types = {
        'popular':"populaire producten zoals deze",
        'similar':"Soortgelijke producten",
        'combination':'Combineert goed met',
        'behaviour':'Passend bij uw gedrag',
        'personal':'Persoonlijk aanbevolen'
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
        if "categoryindex" not in self.database.list_collection_names() or self.database.categoryindex.count_documents({}) == 0:
            self.create_category_index()

        # We retrieve the categoryindex from the database when it is set.
        self.categoryindex = self.database.categoryindex.find_one({}, {'_id' : 0})

        # In order to save time in future, we flatten the category index once,
        # and translate all values to and from an encoded, URL-friendly, legible
        # format.
        catlist = self.flatten_dict(self.categoryindex)
        for cat in catlist:
            enc_cat = self.encode_category(cat)
            self.cat_encode[cat] = enc_cat
            self.cat_decode[enc_cat] = cat

        # Since the main menu can't show all the category options at once in a
        # legible manner, we choose to display a set number with the greatest 
        # number of associated products.
        countlist = list(map(lambda x, y: (y['_count'], x), self.categoryindex.keys(), self.categoryindex.values()))
        countlist.sort(reverse=True)
        self.main_menu_items = [x[1] for x in countlist[0:self.main_menu_count]]

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
            self.reccat_index(index, entry, 0, len(self.cat_levels) - 1)
        for k, v in index.items():
            self.reccat_count(k, v, 0, len(self.cat_levels) - 1)
        self.database.categoryindex.insert_one(index)

    def reccat_index(self, d, e, l, m):
        """ This subfunction of createcategoryindex() sets up the base structure
        (tree) of the categories and subcategories, leaving leaves as empty 
        dicts."""
        if l > m:
            return
        t = self.cat_levels[l]
        if t in e and e[t] is not None and type(e[t]) != list and e[t] not in d:
            d[e[t]] = {}
        if t in e and e[t] is not None and type(e[t]) != list and e[t] in d:
            self.reccat_index(d[e[t]], e, l + 1, m)

    def reccat_count(self, k, v, l, m):
        """ This subfunction of createcategoryindex() adds the number of 
        documents associated with any (sub)category to its dictionary as the
        _count property. """
        if l > m:
            return
        if isinstance(v, dict):
            for k2, v2 in v.items():
                self.reccat_count(k2, v2, l + 1, m)
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
        packet['categoryindex'] = self.categoryindex
        packet['mainmenulist'] = self.main_menu_items
        packet['categories_encode'] = self.cat_encode
        packet['categories_decode'] = self.cat_decode
        packet['paginationcounts'] = self.pagination_counts
        packet['items_per_page'] = session['items_per_page']
        packet['session_id'] = session['session_id']
        packet['profile_id'] = session['profile_id']
        packet['shopping_cart'] = session['shopping_cart']
        packet['shopping_cart_count'] = self.shopping_cart_count()
        return render_template(template, packet=packet)

    """ ..:: Recommendation Functions ::.. """

    def recommendations(self, count, r_type, page_path=None):
        """ This function returns the recommendations from the provided page
        and context, by sending a request to the designated recommendation
        service. At the moment, it only transmits the profile ID and the number
        of expected recommendations; to have more user information in the REST
        request, this function would have to change."""
        pp.pp(session)
        id_count = session['profile_id'] + "/" + str(count)
        resp = requests.get(
            self.rec_ser_address + "/" + id_count + "/" + r_type + "/" + str(page_path))
        if resp.status_code == 200:
            recs = eval(resp.content.decode())
            queryfilter = {"_id": {"$in": recs}}
            query_cursor = self.database.products.find(queryfilter, self.product_fields)
            result_list = list(map(self.prep_product, list(query_cursor)))
            return result_list
        return []

    """ ..:: Full Page Endpoints ::.. """

    def product_page(self, cat1=None, cat2=None, cat3=None, cat4=None, page=1):
        """ This function renders the product page template with the products it
        can retrieve from the database, based on the URL path provided (which
        corresponds to product categories). """
        cat_list = [cat1, cat2, cat3, cat4]
        queryfilter = {}
        nononescats = []
        for k, v in enumerate(cat_list):
            if v is not None:
                queryfilter[self.cat_levels[k]] = self.cat_decode[v]
                nononescats.append(v)
        query_cursor = self.database.products.find(queryfilter, self.product_fields)
        prod_count = self.database.products.count_documents(queryfilter)
        skip_index = session['items_per_page']*(page-1)
        query_cursor.skip(skip_index)
        query_cursor.limit(session['items_per_page'])

        print(nononescats, cat_list)

        prod_list = list(map(self.prep_product, list(query_cursor)))
        recommendation_type = list(self.recommendation_types.keys())[0]
        # pp.pp(prod_list)
        if len(nononescats) >= 1:
            page_path = "/producten/"+("/".join(nononescats))+"/"
        else:
            page_path = "/producten/"
        return self.render_packet_template('products.html', {
            'products': prod_list,
            'productcount': prod_count, \
            'pstart': skip_index + 1, \
            'pend': skip_index + session['items_per_page'] if session['items_per_page'] > 0 else prod_count, \
            'prevpage': page_path+str(page-1) if (page > 1) else False, \
            'nextpage': page_path+str(page+1) if (session['items_per_page']*page < prod_count) else False, \
            'r_products':self.recommendations(4, recommendation_type, page_path), \
            'r_type':recommendation_type,\
            'r_string':list(self.recommendation_types.values())[0]\
            })

    def product_detail(self, product_id):
        """ This function renders the product detail page based on the product
        id provided. """
        product = self.database.products.find_one({"_id":str(product_id)})
        recommendation_type = list(self.recommendation_types.keys())[1]
        return self.render_packet_template('productdetail.html', {
            'product':product,\
            'prepproduct':self.prep_product(product),\
            'r_products':self.recommendations(4, recommendation_type), \
            'r_type':recommendation_type,\
            'r_string':list(self.recommendation_types.values())[1]
        })

    def shoppingcart(self):
        """ This function renders the shopping cart for the user."""
        i = []
        recommendation_type = list(self.recommendation_types.keys())[2]
        for tup in session['shopping_cart']:
            product = self.prep_product(self.database.products.find_one({"_id":str(tup[0])}))
            product["itemcount"] = tup[1]
            i.append(product)
        return self.render_packet_template('shoppingcart.html', {
            'itemsincart':i,\
            'r_products':self.recommendations(4, recommendation_type), \
            'r_type':recommendation_type,\
            'r_string':list(self.recommendation_types.values())[2]
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