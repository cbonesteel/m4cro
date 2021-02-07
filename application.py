from flask import Flask, render_template
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import requests as req

cloud_config = {
    'secure_connect_bundle': './secure-connect-m4cro-database.zip'
}
auth_provider = PlainTextAuthProvider('m4cro', 'M@VnDu2D7#tc')
cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
session = cluster.connect()

print('Connected to DataStax')

zomato_headers = {'Accept': 'application/json', 'user-key':'8b3dc6c1a42f7efdc2da8c6dab9f8778'}
number = session.execute('select number from userdata.website where id = \'people\';').one()[0]

app = Flask(__name__)

@app.route('/')
def index():
    global number
    number += 1
    session.execute('update userdata.website set number += 1 where id = \'people\';')
    person_number = '{}'.format(number)
    if (number % 100) == 11 or (number % 100) == 12 or (number % 100) == 13:
        person_number += 'th'
    elif number == 1 or (number % 10) == 1:
        person_number += 'st'
    elif number == 2 or (number % 10) == 2:
        person_number += 'nd'
    elif number == 3 or (number % 10) == 3:
        person_number += 'rd'
    else:
        person_number += 'th'
    return render_template('index.html', person_number=person_number)
    
@app.route('/start')
def start():
    return render_template('start.html')

    
@app.route('/login')
def login():
    return render_template('login.html')

    
@app.route('/register')
def register():
    return render_template('register.html')


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

# city is a string, "Athens, GA" for example
def get_restaurants_in_city(city):
    global zomato_headers
    city_id = req.get('https://developers.zomato.com/api/v2.1/cities?q={}'.format(city), headers=zomato_headers).json()['location_suggestions'][0]['id']
    restaurants = req.get('https://developers.zomato.com/api/v2.1/search?entity_id={}&entity_type=city'.format(city_id), headers=zomato_headers).json()['restaurants']
    
    # pertinent information for each restaurant: "name", "location", "menu_url"
    return restaurants
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
