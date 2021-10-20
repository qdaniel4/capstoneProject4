"""module for windy api requests--can be used to get images, livestreams, and videos by location (coordinates), date, and category"""

import requests
import os
from pprint import pprint
from functools import lru_cache
from io import BytesIO
from PIL import Image, ImageShow

key = os.environ.get('WINDY_KEY')
header = {'x-windy-key': key}

"""examples so I can remember paths"""
#url = 'https://api.windy.com/api/webcams/v2/list/country=IT/category=beach/orderby=popularity/limit=20?show=webcams:location,image,player'
#url = 'https://api.windy.com/api/webcams/v2/list/nearby=38.732534,0.217634,100/category=beach/orderby=distance/limit=1?show=webcams:location,image'
#url = 'https://api.windy.com/api/webcams/v2/list?show=categories'

"""caches category list"""
@lru_cache(maxsize=1)
def show_categories():
    categories = []

    url = 'https://api.windy.com/api/webcams/v2/list?'
    parameters = {'show': 'categories'}

    data = requests.get(url, headers=header, params=parameters).json()

    category_list = data.get('result').get('categories')
    for category in category_list:
        categories.append(category.get('id'))
    return categories

"""formats parameters/path before getting a response from the api"""
def format_params(coordinates, radius, category_choice, order, amount):
    coordinates = coordinates.replace(' ', '')
    nearby = f'nearby={coordinates},{radius}'
    category = f'category={category_choice}'
    orderby = f'orderby={order}'
    limit = f'limit={amount}'
    return nearby, category, orderby, limit

"""gets a list of daylight and current time image links from the api, list depends on the users preferences (location, category, sorted, how many they want to see)"""
def get_image_list(nearby, category, orderby, limit):

    url = f'https://api.windy.com/api/webcams/v2/list/{nearby}/{category}/{orderby}/{limit}?show=webcams:location,image'
    daylight_links = []
    current_links = []
    data = requests.get(url, headers=header).json()

    webcams = data.get('result').get('webcams')
    for link in webcams:
        daylight_links.append(link.get('image').get('daylight').get('preview'))
        current_links.append(link.get('image').get('current').get('preview'))
    return daylight_links, current_links

"""saves a list of daylight and current time images"""
def save_images(daylight_links, current_links):
    daylight_images = []
    current_images = []

    for day_url in daylight_links:
        r = requests.get(day_url)
        image = Image.open(BytesIO(r.content))
        daylight_images.append(image)

    for current_url in current_links:
        r = requests.get(current_url)
        image = Image.open(BytesIO(r.content))
        current_images.append(image)
    return daylight_images, current_images
