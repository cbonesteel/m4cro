from flask import Flask, render_template

number = 0

app = Flask(__name__)

@app.route('/')
def index():
    global number
    number += 1
    person_number = '{}'.format(number)
    if number == 1:
        person_number += 'st'
    elif number == 2:
        person_number += 'nd'
    elif number == 3:
        person_number += 'rd'
    else:
        person_number += 'th'
    return render_template('index.html', person_number=person_number)
    
@app.route('/something/<thing>')
def thing(thing):
    return 'Wow! What a %s!'.format(thing)
    
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404