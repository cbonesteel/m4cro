from flask import Flask, render_template
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

cloud_config = {
    'secure_connect_bundle': './secure-connect-m4cro-database.zip'
}
auth_provider = PlainTextAuthProvider('m4cro', 'M@VnDu2D7#tc')
cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
session = cluster.connect()

print('Conencted to DataStax')

number = 0

app = Flask(__name__)

@app.route('/')
def index():
    global number
    number += 1
    person_number = '{}'.format(number)
    if number == 1 or (n % 10) == 1;
        person_number += 'st'
    elif number == 2 or (n % 10) == 2;
        person_number += 'nd'
    elif number == 3 or (n % 10) == 3;
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
    
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)