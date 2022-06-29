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
    #if mars_data.hemisphere_image_urls is None:
    #    return redirect("/scrape")

    print("mars data: ", mars_data)
    print("keys: ", mars_data.keys())

    # Return template and data
    return render_template("index.html", mars_data=mars_data)

# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    mars_app = mongo.db.mars_data
    mars_scrape = scrape_mars.scrape()
    #mars_app.update_one({}, mars_scrape, upsert=True)
    
    # # Run the scrape function
    #planet_mars = scrape_mars.scrape()

    # # Update the Mongo database using update and upsert=True
    mongo.db.collection.update_one({}, {"$set": mars_scrape}, upsert=True)

    # Redirect back to home page
    return redirect("/")

# Set debug to false to prevent web scrape inturruptions
if __name__ == "__main__":
    app.run(debug=True, use_reloader=False, passthrough_errors=True)
    