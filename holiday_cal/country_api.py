import os
import requests
import json
from exceptions import NoStateRegion
from credentials import api_key,url_countries
import redis
from functools import lru_cache
import time

redi = redis.Redis(host='localhost', port=6379, db=0)

""" Returns all the supported countries and country_code. """

def country_code_handler():
    """ request and return countries supported by API. """
    country_list = req_res_country()
    return country_list


def req_res_country():
    country_res = redi.get('countries')
    if country_res is None: #if list of countries not in cache get it from api
        print('Could not find country codes in cache, retrieving from the API')
        req = req_countries()
        res = extract_countries(req)
        results = lis_of_countries(res)
        return results
    else:
        print('Found country codes in cache, retrieving from redis')
        return country_res
    

@lru_cache(maxsize=50) # start clearing the least recently used items after 50 entries 
def req_countries():
    """ Call countries API """
    query = {'api_key': api_key}
    req = requests.get(url_countries,params=query)
    try:
        req.raise_for_status() #raises 404 client error
    except requests.exceptions.HTTPError as httperror:
        print(f'Http error,check if the url is correct: {httperror}')
    except requests.exceptions.RequestException as err:
        print(f'Error: Something else went wrong{err}')
    return req.json()


def extract_countries(res):
    country_list = res['response']['countries']
    if country_list != None:
        return country_list


def lis_of_countries(countries):
    """ dump all of the countries and countr code (ISO) in json"""
    results = []
    for c in countries:
        country_name = c['country_name']
        country_code = c['iso-3166']
        name_code = {
            'country_name':country_name,
            'country_code':country_code
        }
        results.append(name_code)
        redi.set('countries',json.dumps(results)) #timedelta(seconds=3600)
    return results
from datetime import timedelta



# t1 = time.time()
# print(country_code_handler())
# t2 = time.time()
# print(t2-t1)
# info = req_countries.cache_info()
#0.002855062484741211 when retrieved from cache
#0.2691211700439453 when retrieved from api
# total= 0.0021638870239257812
