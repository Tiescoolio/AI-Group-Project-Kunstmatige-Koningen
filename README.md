# huwebshop
Git for the HU Webshop project.

Todo:

- Test this code on a local deployment.

--------------------

Requirements:

- Python 3
- Flask (includes Jinja and Werkzeug)
- python-dotenv met command line interface support
- MongoDB (installer)
- Pymongo package
- jQuery
- Some cool buttons (https://fdossena.com/?p=html5cool/buttons/i.frag)

--------------------

Answered:

- How can I autodeploy my script to the cloud?
	- Through a fairly complicated shell script, but there is a draft version of the pre-project packaging version in the helloworld folder of the project.

--------------------

- How does the database operate when I run it on my local machine?
	- Fine, actually, and fairly quickly too.
- How many entries have no appropriate images?
	- 4535 out of 12800 entries have no pictures (search terms: {'images.0.0' : null}); but seeing as the data is (at least partially) intentionally faulty, it stands to reason that a default image would be better than explicitly looking up alternatives.
- How can I package my code such that I can easily push it to the App Engine - or any other platform?
	- Command line variables that allow you to specify where the database/collection is you are trying to connect to, a YAML file to provide the configuration, a requirements.txt to automate getting the libraries through pip and a shell script to execute the deployment automatically from the cloud shell. But this, at the moment, is not yet required.
- What is the average size of the images involved, and subsequently, what is the estimated size of all images collected?
	- 17.75 KB for the small ones (oom.: 20), and 440 KB for the big ones (oom.: 500 KB).
	Say that one pairing is about 550 KB. Times 8265 (the number of entries with images) that comes out to approximately four-and-a-half GB.
- Can the shop actually be crawled for images?
	- Not since the 18th of June, it can't. The site appears to have been locked behind a rudimentary login prompt.

--------------------

- How can I use dynamic and optional attributes in the URLs?
	- To retrieve GET parameters, you can use an import (from flask import request) and its subsequent object request.args.get("parameter name") to get the value. You can also use dynamic values in the URLs themselves 
- How can I generate a random "shopper name" from a session ID?
	- No need to use the session ID; Flask automatically supports maintaining a session that allows you to store any amount of data.
- What would be the most sensible place to store the shopping cart information for any given user?
	- In the session object.
- How can I get templates to work within this structure?
	- Damn near instantly, using the render_template function as well as referring directly to the session object from there.
- How can I get one function to execute before every route?
	- By using the @app.before_request decorator.
- How can I handle errors (such as 404s) in this application?
	- Redirect users to different endpoint with redirect(url_for), abort with an error code with abort(404) (or another numeric code), and use the @app.errorhandler(404) decorator (or another code) to handle errors.
- How can I recursively refer to templates from within templates? Or does this need to happen on the code level?
	- Templates can be extended, which allow the replacement of certain blocks; there's an example of this now in the code folder. Recursively, it makes more sense to just use for functions found in Jinja.
- How can I escape the HTML used, preferably automatically?
	- This is already done automatically by Flask in the render_template function.
- How would I store an item in the shopping cart, if changing the shopping cart requires sending a request to the server?
	- A basic URL-based method definitely works, without much of a hitch. But I don't think this is reflective of current web standards. An AJAX approach would be more appropriate - at which point, jQuery is the next logical move. To be further developed, once the templates are setup in a logical way in the project proper.

--------------------