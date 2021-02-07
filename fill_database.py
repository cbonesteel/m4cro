from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import requests as req

import re
import io
import pytesseract
from PIL import Image

# cloud_config = {
    # 'secure_connect_bundle': './secure-connect-m4cro-database.zip'
# }
# auth_provider = PlainTextAuthProvider('m4cro', 'M@VnDu2D7#tc')
# cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
# session = cluster.connect()

zomato_headers = {'Accept': 'application/json', 'user-key':'8b3dc6c1a42f7efdc2da8c6dab9f8778'}

# city is a string, "Athens, GA" for example
def get_restaurants_in_city(city):
    global zomato_headers
    city_id = req.get('https://developers.zomato.com/api/v2.1/cities?q={}'.format(city), headers=zomato_headers).json()['location_suggestions'][0]['id']
    restaurants = req.get('https://developers.zomato.com/api/v2.1/search?entity_id={}&entity_type=city'.format(city_id), headers=zomato_headers).json()['restaurants']
    
    # pertinent information for each restaurant: "name", "location", "menu_url"
    return restaurants
    
def parse_menu(restaurant):
    # download menu images
    content = req.get(restaurant['menu_url']).text
    url_pattern = re.compile(r'https:\\/\\/b\\.zmtcdn\\.com\\/data\\/menus\\/[0-9]*\\/[0-9]*\\/.*?\\.(png|jpg|jpeg)')
    menu_urls = set(url_pattern.findall(content))
    
    # parse text in all the images
    menu_pages = []
    for menu_url in menu_urls:
        resp = req.get(menu_url)
        img = Image.open(io.BytesIO(resp.content))
        text = pytesseract.image_to_string(img)
        menu_pages.append(text)
    
    # list of OCRed strings
    return menu_pages
    

def fill_database():
    # get restaurants in athens
    rests = get_restaurants_in_city('Athens, GA')
    for rest in rests:
        rest = rest['restaurant']
        items = []
        obj = {
            'name': rest['name'],
            'website': rest['url'],
            'latitude': float(rest['location']['latitude']),
            'longitude': float(rest['location']['longitude']),
            'items': items
        }
        
        # parse the menu
        pages = parse_menu(rest)
        
        print(obj['name'])
        print(pages)
        print('----------------------------\n')
        
        # nutrition for each menu item
        pass
        # throw the restaurant into the database
        pass
    
    # done :)

if __name__ == '__main__':
    fill_database()