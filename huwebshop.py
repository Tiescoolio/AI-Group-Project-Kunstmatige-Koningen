from flask import Flask, request, session, render_template, redirect, url_for, g
import random, os, json, huw_utilities
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
# The client is the object that connects with the MongoDB database. This is used
# centrally throughout the code below.
if os.getenv("MONGODBUSER") is not None:
	clientstring = 'mongodb+srv://'+str(os.getenv("MONGODBUSER"))+':'+str(os.getenv("MONGODBPASSWORD"))+'@'+str(os.getenv("MONGODBSERVER"))+'/test?retryWrites=true&w=majority'
	client = MongoClient(clientstring)
else:
	client = MongoClient()
products = client.huwebshop.products
productcount = products.count_documents({})
# Once the client is booted up, we check whether it already has a category 
# index. If not, we create it here once.
colnames = client.huwebshop.collection_names()
if "categoryindex" not in colnames:
	huw_utilities.createcategoryindex(client)
productindex = client.huwebshop.categoryindex.find_one({})

'''
..:: Global Variables ::..
Variables used across the application, kept in one place for reference.
'''
pagination_counts = [3, 6, 12, 0]
fake_first_names = ["Steve", "Jean", "Paean", "Mirabelle", "Alma", "Xanthippe", "Salazar", "Gem", "Ornacia", "Ben"]
fake_last_names = ["Shimmertwig", "Trapezoid", "Gauntyl", "Wasserwald", "Smith", "Johnson", "Womble", "Octagon", "Framboise", "von Tuile"]

'''
..:: Session Functions ::..
Functions that maintain and modify the session data contents.
'''
@app.before_request
def check_session():
	if ('session_valid' not in session) or (session['session_valid'] != 1):
		session['first_name'] = random.choice(fake_first_names)
		session['last_name'] = random.choice(fake_last_names)
		session['shopping_cart'] = []
		session['items_per_page'] = pagination_counts[0]
		# It's a little hacky to store this in session data, but you can 
		# reasonably expect this to be a short array, and otherwise, a whole 
		# other mechanism is required to get this done!
		session['pagination_counts'] = pagination_counts 
		session['session_valid'] = 1

'''
..:: Post Functions ::..
Functions that are hailed through AJAX, and which only refresh the page when
explicitly specified.
'''
@app.route('/dynamic-shopping-cart', methods=['POST'])
def dynamic_shopping_cart():
	# TODO: expand upon this method, ensuring it actually transfers all relevant
	# information.
	itemcount = 0
	for tup in session['shopping_cart']:
		itemcount += tup[1]
	retval = {}
	retval['itemcount'] = itemcount
	return json.dumps(retval)

@app.route('/producten/pagination-change/<int:pagval>', methods=['POST'])
def pagination_change(pagval):
	session['items_per_page'] = pagval
	# TODO: add method that returns the exact URL the user should be returned to
	return "/producten"

@app.route('/add-to-shopping-cart/<int:productid>', methods=['POST'])
def add_to_shopping_cart(productid):
	cartids = list(map(lambda x: x[0], session['shopping_cart']))
	if productid in cartids:
		ind = cartids.index(productid)
		session['shopping_cart'][ind] = (session['shopping_cart'][ind][0], session['shopping_cart'][ind][1]+1)
	else:
		session['shopping_cart'].append((productid, 1))
	# Apparently, explicit assignment is required? If it works...
	session['shopping_cart'] = session['shopping_cart']
	return dynamic_shopping_cart()

'''
..:: Actual Pages ::..
The pages that contain actual, non-debug functionality.
'''
# This page is the homepage of the actual site.
@app.route('/')
def homepage():
	return render_template('homepage.html')

# This page is the user's shopping cart.
@app.route('/winkelwagen')
def winkelwagen():
	return render_template('shoppingcart.html', shoppingcart=get_shopping_cart())

def get_shopping_cart():
	retval = []
	for tup in session['shopping_cart']:
		product = products.find_one({"productid":tup[0]})
		product["itemcount"] = tup[1]
		retval.append(product)
	return retval

# This page is the list of products in the shop.
@app.route('/producten')
@app.route('/producten/<int:pagina>')
def producten(pagina=1, start=0):
	if request.args.get('start') is not None:
		start = int(request.args.get('start'))
	firstelement = (pagina-1)*session['items_per_page']+start
	while firstelement >= productcount and firstelement >= 0:
		firstelement -= session['items_per_page']
		pagina -= 1
	endelement = firstelement+session['items_per_page']
	if session['items_per_page'] == 0:
		firstelement = 0
		endelement = productcount
	elements = products.find({"_id": {"$gte":firstelement, "$lt":endelement}}).sort("_id")
	productlist = []
	for element in elements:
		productlist.append(element)
	return render_template('products.html', productlist=productlist, productcount=productcount, countfirst=firstelement+1, countlast=min(productcount,endelement), page=pagina, moretoshow=productcount>endelement)

# This page is the detail page for a specific product.
@app.route('/detail/<int:productid>')
def detailpagina(productid):
	product = products.find_one({"productid":productid})
	return render_template('detail.html', product=product)


'''
..:: Error Routes ::..
Routes that catch the inevitable error pages generated by erroneous requests.
'''
# TODO: expand the following:
#@app.errorhandler(404)
#@app.errorhandler(405)

''' 
..:: Test Routes ::..
Routes that lead to pages which are exclusively used for debugging and testing
purposes.
'''
@app.route('/showcount')
def showcount():
	return str(productcount)

@app.route('/showstring')
def showstring():
	return clientstring

@app.route('/showcolnames')
def showcolnames():
	return str(colnames)

@app.route('/showproductindex')
def showproductindex():
	return str(productindex)