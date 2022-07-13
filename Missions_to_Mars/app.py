# Import dependancies
from flask import Flask, render_template, redirect, session
from flask_pymongo import PyMongo
import os
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_database"
mongo = PyMongo(app)

# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    # Find record of data from mongo database
    mars_data = mongo.db.mars_data.find_one()

    # Return template and data
    return render_template("index.html", mars_data=mars_data)

# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    mars_data = mongo.db.mars_data
    mars_scrape = scrape_mars.scrape_all()
    mars_data.update_many({}, {"$set" : mars_scrape}, upsert=True)

    # Redirect back to home page
    return redirect("/", code=302)

# Set debug to false to prevent web scrape inturruptions
if __name__ == "__main__":
    app.run(debug=True, use_reloader=False, passthrough_errors=True)
    