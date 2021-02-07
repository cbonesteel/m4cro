from flask import Flask, render_template, request, redirect, url_for
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import requests as req
import re

class recommendation:
    def __init__(self, restaurant, travel_time, meal, carbs, fat, protein, kcals):
        self.restaurant = restaurant
        self.travel_time = travel_time
        self.meal = meal
        self.carbs = carbs
        self.fat = fat
        self.protein = protein
        self.kcals = kcals

cloud_config = {
    'secure_connect_bundle': './secure-connect-m4cro-database.zip'
}
auth_provider = PlainTextAuthProvider('m4cro', 'M@VnDu2D7#tc')
cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
session = cluster.connect()

print('Connected to DataStax')

number = session.execute('select number from userdata.website where id = \'people\';').one()[0]

app = Flask(__name__)

@app.route('/')
@app.route('/index')
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

@app.route('/start/<name>')
def start(name=None):
    return render_template('start.html', display_name=name)

@app.route('/results')
def results():
    recommendations = []
    recommendations.append(recommendation("McDonalds", "10 min", "Chicken", "50", "20", "30", "500"))
    recommendations.append(recommendation("Burger King", "10 min", "Other Chicken", "40", "30", "28", "542"))
    return render_template('results.html', recommendations=recommendations)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if valid_login(request.form['email'], request.form['password']):
            return user_login(request.form['email'])
        else:
            error = 'Invalid email/password'
    return render_template('login.html', error=error)

@app.route('/register', methods=['POST', 'GET'])
def register():
    error = None
    if request.method == 'POST':
        if valid_registration(request.form['email'], request.form['password'], request.form['firstname'], request.form['lastname']):
            return user_login(request.form['email'])
        else:
            error = 'Email already taken. Please use another email.'
    return render_template('register.html', error=error)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

def valid_login(email, password):
    global session
    check = session.execute('SELECT password FROM userdata.users WHERE email = \'{}\''.format(email)).one()
    if check:
        return check[0] == password
    return False

def valid_registration(email, password, firstname, lastname):
    global session
    checkEmail = len(session.execute('SELECT email FROM userdata.users WHERE email = \'{}\''.format(email)))
    if checkEmail != 0:
        session.execute('insert into userdata.users (email, password, firstname, lastname) values (\'{}\', \'{}\', \'{}\', \'{}\');'.format(username, password, firstname, lastname))
        return True
    return False

def user_login(email):
    set = session.execute('SELECT firstname FROM userdata.users WHERE email = \'{}\''.format(email)).one()
    return redirect(url_for('start', name=set[0]))

def get_distance(latitude, longitude):
    # get user location
    # TODO
    
    # throw into radar.io request (see https://radar.io/documentation/api#distance)
    radar_header = { 'Authorization': 'prj_test_sk_1390526d2da070f76d1b9420976d91119fea3158' }
    data = req.get('https://api.radar.io/v1/route/distance?origin={},{}&destination={},{}&modes=foot,car&units=imperial', header=radar_header).json()
    
    # do stuff with data
    # TODO
    pass

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
