import json

from flask import Flask
from flask import render_template

from pymongo import MongoClient


app = Flask(__name__)

client = MongoClient('mongodb://localhost:27017/')
db = client.news
collection = db.news


@app.route('/')
def main():
    # need to render template
    # return str(collection.find_one())
    return render_template('index.html')
 

@app.route('/update')
def update():
    # Get request on updating database
    return 'Hi'

@app.route('/add')
def add():
    # post request on adding news via link 
    return 'Hi'

@app.route('/fetch')
def fetch():
    # get request on fetching news (all or specified)
    return 'Hi'



if __name__ == '__main__':
    app.run()