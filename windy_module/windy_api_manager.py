"""module for windy api requests--can be used to get images, livestreams, and videos by location (coordinates), date, and category"""

import requests
import os
from functools import lru_cache



key = os.environ.get('WINDY_KEY')
header = {'x-windy-key': key}

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


"""gets a list of daylight and current time image links from the api, 
list depends on the users preferences (location, category, sorted, how many they want to see)"""
def get_image_list(coordinates, category):

    daylight_links = []
    current_links = []
    limit = '5'
    data = get_windy_response(coordinates, category, limit)

    if len(data.get('result').get('webcams')) == 0:
        return None
    else:
        webcams = data.get('result').get('webcams')
        for link in webcams:
            daylight_links.append(link.get('image').get('daylight').get('preview'))
            current_links.append(link.get('image').get('current').get('preview'))
        return daylight_links


def get_windy_response(coordinates, category, limit): #function to be mocked
    key = os.environ.get('WINDY_KEY')
    header = {'x-windy-key': key}
    url = f'https://api.windy.com/api/webcams/v2/list/nearby={coordinates},300/category={category}/orderby=distance/limit={limit}?show=webcams:location,image'
    data = requests.get(url, headers=header).json()
    return data


def get_video_link(nearby, category):
    limit = '5'
    data = get_windy_response(nearby, category, limit)
    month_video = []
    live_video = []
    webcams = data.get('result').get('webcams')
    for link in webcams:
        month_video.append(link.get('player').get('month').get('embed'))
        live_video.append(link.get('image').get('current').get('preview'))
    return month_video
