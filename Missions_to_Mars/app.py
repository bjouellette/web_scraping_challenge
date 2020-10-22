from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import pymongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection

mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")


# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    # Find one record of data from the mongo database
    mars_dataDB = mongo.db.mars_data_collection.find_one()
    # mars_dataDB = {}
    # Return template and data
    return render_template("index.html", planet=mars_dataDB)


# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    # Run the scrape function
    mars_dataDB = mongo.db.mars_data_collection
    mars_data = scrape_mars.scrape_info()
    print(mars_data)
    # Update the Mongo database using update and upsert=True
    mars_dataDB.update({}, mars_data, upsert=True)

    # Redirect back to home page
    return redirect("/", code = 302)


if __name__ == "__main__":
    app.run(debug=True, port = 5003)
