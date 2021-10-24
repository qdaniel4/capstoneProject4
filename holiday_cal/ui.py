""" Performs API requests and generates holidays celebrated in a given country during that month. """

import os
from credentials import api_key,url_countries, url_holiday
import requests
import json
import logging as log
from exceptions import NoStateRegion
import time
from datetime import datetime
 

#countries end point
def country_code_handler(country_code):
    """  verifies if the provided country_code matches to any of the countries supported by the API.
    :param:  The country code to verify.
    :returns: True if a country exists with the provided country_code, else raises NoStateRegion. """
    try:
        res = req_countries()
        countries = extract_countries(res)
        for c in countries:
            if c['iso-3166'] == country_code:
                return country_code
            
        raise NoStateRegion
    except NoStateRegion:
        print('error, No country matches the provided country code,try again!\n')
        return None
    

def req_countries():
    """ Call countries API """
    query = {'api_key': api_key}
    res = requests.get(url_countries,params=query)
    try:
        res.raise_for_status()
    except requests.exceptions.RequestException as err:
        print(err)
        return None
    return res.json()


def extract_countries(res):
    countries = res['response']['countries']
    if countries != None:
        lis_of_countries(countries)
        return countries
        
    
            
 #holiday endpoint           
def get_holiday_data(country,year,month):
    """ call holiday api with the provided data.
    :params:  user data to request holiday.
    :returns: holiday data if there is a holiday, otherwise returns None """
    try:
        query = {'country': country, 'year': year, 'month': month, 'type':'national','api_key':api_key}
        req = req_holiday(query)
        response = check_holiday_data_not_null(req)
        return response
    except requests.exceptions.HTTPError as err:
        response.raise_for_status()
        print(err.response.text)
        
        
def req_holiday(query):
    try:
        req = requests.get(url_holiday,params=query).json()
        return req
    except requests.RequestException as e:
        req.raise_for_status()
        print(e.response.text)
    

def check_holiday_data_not_null(res):
    """ check if there is no holiday found
    :param: response from api
    :returns: none if there is no holiday """
    holiday_json = res['response']['holidays']
    return None if holiday_json == [] else holiday_json 

    
def extract_holiday(holiday_data):
    """ extract holiday data.
    :param: holiday api response
    :returns: dictionary of the holiday data to render to the user.  """
    for hol in holiday_data:
        print()
        holiday_name = hol['name']
        description = hol['description']
        country_name = hol['country']['name']
        holiday_date = hol['date']['iso']
        print(f'Holiday name: {holiday_name}\ndescription: {description}\ncountry: {country_name}\ndate: {holiday_date}')
        
        holiday_dict = {
            'holiday_name':holiday_name,
            'description':description,
            'country':country_name,
            'date':holiday_date
        }
        send_json(holiday_dict)
    return holiday_dict

def display_holiday(holiday):
    """ displays all holidays with the provided data.
    :returns: holiday_data dictionary to display in the template.  """
    try:
        holiday_data = extract_holiday(holiday)
        return holiday_data
    except Exception as e:
        print(e)
        print('This data is not in the format expected')
        return 'Unknown'


def send_json(user_data):
    """ To check the data types holiday api returns. """
    # NOTE verifying purposes 
    with open("scratch.json", "w") as f:
        json.dump(user_data,f, indent=2)

#USE FOR DROP DOWN
def lis_of_countries(countries):
    """ returns all of the countries and countr code (ISO) supported by api """
    #NOTE this function for testing, using countries_scratch.json file instead of api calls
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