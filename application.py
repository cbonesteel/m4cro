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

    def cost(self, c, f, p):
        return (int(self.carbs)-c)**2 + (int(self.fat)-f)**2 + (int(self.protein)-p)**2 + (int(self.travel_time.split(' ')[0]))**2

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
@app.route('/start/<name>')
def start(name=None):
    return render_template('start.html', display_name=name)

@app.route('/aboutus')
def aboutus():
    return render_template('about.html')

@app.route('/results', methods=['POST', 'GET'])

def results():
    recommendations = []

    if request.method == 'POST':
        c = int(request.form['carb-input']) if request.form['carb-input'].isnumeric() else 0
        f = int(request.form['fat-input']) if request.form['fat-input'].isnumeric() else 0
        p = int(request.form['protein-input']) if request.form['protein-input'].isnumeric() else 0
        recommendations.append(recommendation("McDonalds", "5 min", "Big Mac", "45", "30", "25", "550"))
        recommendations.append(recommendation("McDonalds", "5 min", "10pc Chicken McNuggets", "25", "25", "23", "420"))
        recommendations.append(recommendation("Zoe's Kitchen", "15 min", "Chicken Kabob", "45", "20", "44", "510"))
        recommendations.append(recommendation("Zoe's Kitchen", "15 min", "Chicken Rollups", "85", "29", "43", "780"))
        recommendations.append(recommendation("Zoe's Kitchen", "15 min", "Chicken Salad Sandwich", "77", "54", "38", "920"))
        recommendations.append(recommendation("Zoe's Kitchen", "15 min", "Falafel Pita", "98", "26", "20", "680"))
        recommendations.append(recommendation("Zoe's Kitchen", "15 min", "Greek Chicken Pita", "74", "23", "48", "680"))
        recommendations.append(recommendation("Zoe's Kitchen", "15 min", "Spicy Chicken Kabobs", "40", "21", "44", "530"))
        recommendations.append(recommendation("Zoe's Kitchen", "15 min", "Steak Kabob", "42", "25", "44", "690"))
        recommendations.append(recommendation("Zoe's Kitchen", "15 min", "Steak Pita", "56", "35", "34", "740"))
        recommendations.append(recommendation("Zoe's Kitchen", "15 min", "Steak Rollup", "86", "48", "46", "940"))
        recommendations.append(recommendation("Zoe's Kitchen", "15 min", "Turkey Avocado Sandwich", "87", "20", "36", "650"))
        recommendations.append(recommendation("Chick-Fil-A", "7 min", "Chicken Biscuit", "50", "21", "17", "450"))
        recommendations.append(recommendation("Chick-Fil-A", "7 min", "Sausage, Egg & Cheese Biscuit", "41", "40", "20", "600"))
        recommendations.append(recommendation("Chick-Fil-A", "7 min", "Chicken Sandwich", "40", "19", "28", "440"))
        recommendations.append(recommendation("Chick-Fil-A", "7 min", "Spicy Chicken Sandwich", "41", "19", "29", "450"))
        recommendations.append(recommendation("Chick-Fil-A", "7 min", "Nuggets (8-count)", "9", "12", "28", "260"))
        recommendations.append(recommendation("Chick-Fil-A", "7 min", "Nuggets (12-count)", "14", "18", "41", "390"))
        recommendations.append(recommendation("Chick-Fil-A", "7 min", "Grilled Chicken Cool Wrap", "29", "14", "37", "350"))
        recommendations.append(recommendation("Chick-Fil-A", "7 min", "Cobb Salad w/Toppings", "37", "19", "34", "450"))
        recommendations.append(recommendation("Taco Bell", "5 min", "Bacon Club Chalupa", "31", "27", "20", "440"))
        recommendations.append(recommendation("Taco Bell", "5 min", "Beef Quesarito", "67", "33", "22", "650"))
        recommendations.append(recommendation("Taco Bell", "5 min", "Beefy 5-Layer Burrito", "63", "18", "18", "490"))
        recommendations.append(recommendation("Taco Bell", "5 min", "Black Bean Chalupa", "39", "15", "10", "330"))
        recommendations.append(recommendation("Taco Bell", "5 min", "Black Bean Crunchwrap Supreme", "77", "17", "13", "510"))
        recommendations.append(recommendation("Taco Bell", "5 min", "Black Beans and Rice", "31", "3", "4", "170"))
        recommendations.append(recommendation("Taco Bell", "5 min", "Breakfast Crunchwrap", "51", "47", "21", "720"))
        recommendations.append(recommendation("Taco Bell", "5 min", "Burrito Supreme- Steak", "49", "12", "18", "370"))
        recommendations.append(recommendation("Taco Bell", "5 min", "Burrito Supreme- Beef", "51", "14", "16", "390"))
        recommendations.append(recommendation("Taco Bell", "5 min", "Burrito Supreme- Chicken", "49", "11", "19", "370"))
        recommendations.append(recommendation("Taco Bell", "5 min", "Cheese Quesadilla", "37", "25", "19", "470"))
        recommendations.append(recommendation("Taco Bell", "5 min", "Hash Brown Toasted Breakfast Burrito - Sausage", "49", "34", "18", "570"))
        recommendations.append(recommendation("Taco Bell", "5 min", "Power Menu Bowl- Steak", "51", "20", "25", "490"))
        recommendations.append(recommendation("Taco Bell", "5 min", "Quesarito- Speacialties", "67", "33", "22", "650"))
        recommendations.append(recommendation("Taco Bell", "5 min", "Chicken Quesarito", "66", "29", "25", "620"))
        recommendations.append(recommendation("Taco Bell", "5 min", "Soft Taco Supreme- Beef", "20", "10", "10", "210"))
        recommendations.append(recommendation("Taco Bell", "5 min", "Soft Taco Supreme- Chicken", "18", "7", "13", "180"))
        recommendations.append(recommendation("Red Lobster", "20 min", "6oz Filet Mingnon", "26", "23", "38", "460"))
        recommendations.append(recommendation("Red Lobster", "20 min", "7oz Sirloin", "26", "22", "45", "480"))
        recommendations.append(recommendation("Red Lobster", "20 min", "Admirals Feast", "129", "98", "64", "1650"))
        recommendations.append(recommendation("Red Lobster", "20 min", "Bar Harbor Lobster Bake", "106", "56", "76", "1250"))
        recommendations.append(recommendation("Red Lobster", "20 min", "Classic Ceaser Salad", "18", "46", "10", "520"))
        recommendations.append(recommendation("Red Lobster", "20 min", "Crab-Stuffed Shrimp Rangoon", "48", "45", "15", "660"))
        recommendations.append(recommendation("Red Lobster", "20 min", "Garlic Linguini Alfredo with Cajun Chicken", "116", "60", "81", "1340"))
        recommendations.append(recommendation("Red Lobster", "20 min", "Hand Breaded Calamari", "63", "65","44","1010"))
        recommendations.append(recommendation("Red Lobster", "20 min", "Lobster and Langostino Pizza", "59", "35", "39", "700"))

        recommendations.sort(key=lambda x: x.cost(c,f,p))
    return render_template('results.html', recommendations=recommendations[:10])

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
            error = 'Email already in use. Please use another email.'
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
    checkEmail = session.execute('SELECT email FROM userdata.users WHERE email = \'{}\''.format(email)).one()
    if not checkEmail:
        session.execute('insert into userdata.users (email, password, firstname, lastname) values (\'{}\', \'{}\', \'{}\', \'{}\');'.format(email, password, firstname, lastname))
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
