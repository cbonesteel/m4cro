from flask import Flask, render_template, request
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
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
    
@app.route('/start')
def start():
    return render_template('start.html')

@app.route('/results')
def results():
    recommendations = []
    recommendations.append(recommendation("McDonalds", "10 min", "Chicken", "50", "20", "30", "500"))
    recommendations.append(recommendation("Burger King", "10 min", "Other Chicken", "40", "30", "28", "542"))
    return render_template('results.html', recommendations=recommendations)
    
@app.route('/login', methods=['POST', 'GET'])
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
    check = session.execute('SELECT password FROM userdata.users WHERE email = {}'.format(email)).one()
    if check:
        return check[0] == password
    return False

def valid_registration(email, password, firstname, lastname):
    global session
    checkEmail = len(session.execute('SELECT email FROM userdata.users WHERE email = {}'.format(email)))
    if checkEmail != 0:
        session.execute('insert into userdata.users (email, password, firstname, lastname) values (\'{}\', \'{}\', \'{}\', \'{}\');'.format(username, password, firstname, lastname))
        return True
    return False

def user_login(email):
    pass


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
