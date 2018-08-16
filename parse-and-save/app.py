import json
import time
from flask import Flask, Response,render_template
from flask_socketio import SocketIO, emit

import pymongo


from updates import check_and_filter_updates, parse_and_add_updates_to_db

app = Flask(__name__)

app.debug = True

client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client.news
collection = db.news

socketio = SocketIO(app)


@app.route('/')
def main():
    return render_template('index.html')

# @app.route('/update')
@socketio.on('update')
def progress():

    emit('update_response',
        {'message': 'Checking articles...'}
    )
    articles = check_and_filter_updates(collection)
    emit('update_response',{
        'articles': len(articles)
    })

    # parse_and_add_updates_to_db(articles)



    

@app.route('/add')
def add():
    # post request on adding news via link 
    return 'Hi'

@app.route('/fetch')
def fetch():
    # get request on fetching news (all or specified)
    return 'Hi'



if __name__ == '__main__':
    # app.run(debug=True)
    socketio.run(app)