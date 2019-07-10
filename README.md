# huwebshop
Git for the HU Webshop project.

## Todo

- [x] Session IDs to Profile IDs (by object ID)
- [x] Reinstate pagination
- [x] Improve the methods, structure and comments of the dynamic elements
- [x] Restructure and clean up the CSS code
- [ ] Add commentary subsections to the huwclass.py
- [ ] Rewrite the huwclass.py to set up URL mappings from within
- [ ] Reinstate a better written dynamic shopping cart mechanism
- [ ] Add error message for incorrect profile IDs
- [ ] Product page layout improvements
- [ ] Design improvements and tweaks (closer to the real thing)
- [ ] Documentation
- [ ] UML diagram
- [ ] Set up local REST service for recommendations
- [ ] Structural review and rewrite of code if needed
- [ ] Optional: image generator
- [ ] Optional: search function
- [ ] Optional: offset and page relocation pagination
- [ ] Optional: responsive design
- [ ] Optional: price calculation and discount rule implementation

## Notes On Future Improvements

MongoDB - alles draaien via mongoimport op het eigen systeem
Recommendation - SQL database

Voorkeur recommendation dummy: REST API - plaatselijk draaien
	- "Stuur alleen IDs terug!"

## Notes On The Project

When testing this project, the following issues arose when trying to work with the full dataset provided:

- The MongoDB Community Edition program, which runs the database service locally, had significant trouble with importing large files on my device.
	- While returning an error ("Unexpected end of JSON file"), it ceased after importing between 10k and 20k documents.
	- The documents that were indeed imported were received correctly, but they were far fewer in number than was to be expected. 
	- When trying the import process multiple times, it failed each time with the same error - but every time with a different number of documents reached. This shows that the error is not in the JSON, regardless of what MongoDB might say.
	- If students were to use local instances of the datasets and unexpectedly get completely different databases as a result, the risk of confusion and subpar products would be massive.
- The MongoDB Free Tier Cloud Cluster, which is provided by MongoDB directly, ran into the limits of its Free Tier when trying to handle the full dataset.
	- The Free Tier allows for 512 MB of storage; the full dataset is approximately 16 GB in size.
	- The cheapest option MongoDB provides that loads the full dataset (M10 Dedicated Cluster, with 20 GB of storage) costs $0,10/hr to run.
	- The cost of setting up such a cluster for the duration of the course (10 weeks) would be 10 * 7 * 24 * $0,10 = $168,- = approx. €150,-.
	- For development and testing purposes, and without agreed-upon compensation, this is fairly costly to run for the employees developing the website - and without a doubt unaffordable for our students individually.

It deserves the consideration of the Hogeschool to pay for a centrally hosted Cloud cluster when this course is actually taught; this Cluster can then be hailed from both the running example website, and the recommendation engines working with the data, functioning as a single source of truth. However, in the meantime, this repository will be updated to contain a testing subset of all data. This data will be constructed separately, once, based on the following criteria:

- A random selection of visitors (i.e. profiles), < 100 MB in size, that are known to have at least one associated existing session.
- The subset of sessions associated with the visitors selected, <= 100 MB in size.
- The file containing all products, which is 357 MB in size.

These restrictions are inspired by the following aspects:

- When compressing the products file in a .zip archive, all of the files can also be included in the Github repository for this project, collecting all necessary data in one place;
- If the products subset remains its original size, the total size of all files is very likely to remain within the MongoDB Free Tier Cluster range (512 MB).

The first testing subset has been composed according to the following additional requirements:

- Based on a back-of-the-envelope estimation of the number of sessions that fit into 100 MB, we find that about 21606 sessions can fit into the file.
- Out of these, we want 15000 of the sessions to have been added by frequent users - i.e. users that have 10 or more sessions attributed to one of their browser configurations. This assures that the sample set contains profiles with "heavy" parameters to test on.
- The remaining 6606, we want to fill with infrequent users - i.e. browser configurations that have 3 or fewer sessions attributed to them. (Note that since one user may have multiple browser configurations, the user itself may still be frequent, but given the general sparseness of the data, this is presumed to be sufficiently unlikely.) This assures that the sample set contains profiles with "light" parameters to test on.

This first testing subset can now be found in the folder datasets_sample_1/.

## Requirements

- Python 3
- Flask (includes Jinja and Werkzeug)
- python-dotenv package (pip install -U python-dotenv)
- Pymongo package
- MongoDB Community Edition (for local installs)

## Included Sources

- jQuery
- Roboto Font (Google Fonts)
- Some cool buttons (https://fdossena.com/?p=html5cool/buttons/i.frag)

<!--
## Development Questions

- How can I autodeploy my script to the cloud?
	- Through a fairly complicated shell script, but there is a draft version of the pre-project packaging version in the helloworld folder of the project.
- How does the database operate when I run it on my local machine?
	- Fine, actually, and fairly quickly too.
- How can I package my code such that I can easily push it to the App Engine - or any other platform?
	- Command line variables that allow you to specify where the database/collection is you are trying to connect to, a YAML file to provide the configuration, a requirements.txt to automate getting the libraries through pip and a shell script to execute the deployment automatically from the cloud shell. But this, at the moment, is not yet required.
- Can the shop actually be crawled for images?
	- Not since the 18th of June, it can't. The site appears to have been locked behind a rudimentary login prompt.
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

-->