import os
import requests
import json
from exceptions import NoStateRegion
from credentials import api_key,url_countries

""" Returns all the supported countries and country_code. """

def country_code_handler():
    """ request and return countries supported by API. """
    res = req_countries()
    countries = extract_countries(res)
    lis_of_countries(countries)
    return countries

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

#TODO cache
#USE FOR DROP DOWN
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
    with open("countries_scratch.json", "w") as f:
        json.dump(results,f, indent=2)