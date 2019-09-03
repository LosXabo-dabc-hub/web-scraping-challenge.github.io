from flask import Flask, render_template, redirect, request
from flask_pymongo import PyMongo
import scrape_craigslist

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/craigslist_app"
mongo = PyMongo(app)

# Or set inline
# mongo = PyMongo(app, uri="mongodb://localhost:27017/craigslist_app")

@app.route("/")
def index():
    listings = mongo.db.listings.find_one()
    print(listings)
    return render_template("index.html", listings=listings)

@app.route("/scrape")
def scraper():
    listings = mongo.db.listings
    print(listings.find())
    listings_data = scrape_craigslist.scrape()
    print(listings_data)
    listings.update({}, listings_data, upsert=True)
    return redirect("/", code=302)


@app.route('/shutdown')
def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    return 'Shutting down Flask server...'


if __name__ == "__main__":
    app.run(debug=True)