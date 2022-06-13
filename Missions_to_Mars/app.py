# Import dependancies
from flask import Flask, render_template, redirect, session
from flask_pymongo import PyMongo
import os
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_database")

# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    # Find record of data from mongo database
    mars_data = mongo.db.collection.find_one()

    # Return template and data
    return render_template("index.html", mars_info=mars_data)

# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():
    
    # Run the scrape function
    planet_mars = scrape_mars.scrape()

    # Update the Mongo database using update and upsert=True
    mongo.db.collection.update_one({}, {"$set": planet_mars}, upsert=True)

    # Redirect back to home page
    return redirect("/")

# Set debug to false to prevent web scrape inturruptions
if __name__ == "__main__":
    app.run(debug=False, use_reloader=False, passthrough_errors=True)
    