""" Performs API requests and generates holidays celebrated in a given country during that month. """

import os
from credentials import api_key,url_countries, url_holiday
import requests
import json
import logging as log
from exceptions import NoStateRegion
import time 
# log config
log.basicConfig(filename='country.log', level=log.DEBUG,format='%(funcName)s')

def country_code_handler(country_code):
    """  verifies if the provided country_code matches to any of the countries supported by the API.
    :param:  The country code to verify.
    :returns: True if a country exists with the provided country_code, else raises NoStateRegion. """
    try:
        res = req_countries()
        for c in res['response']['countries']: 
            if c['iso-3166'] == country_code:
                return country_code
        raise NoStateRegion
    except NoStateRegion:
        print('error, No country matches the provided country code,try again!\n')
        return None
    

def req_countries():
    """ Call countries API """
    try:
        query = {'api_key': api_key}
        res = requests.get(url_countries,params=query).json()
        return res
    except requests.RequestException as e:
        res.raise_for_status()
        print(e)
            

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

    
def extract_holiday(holiday):
    """ extract holiday data and add it to a list.
    :param: holiday api response
    :returns: list of holiday data to render to the user.  """
    user_data = []
    for hol in holiday:
        print()
        holiday_datetime = hol['date']['datetime']        
        holiday_dict={
            'name':hol['name'],
            'description':hol['description'],
            'country':hol['country']['name'],
            'datetime':{
                'year':holiday_datetime['year'],
                'month':holiday_datetime['month'],
                'day': holiday_datetime['day']
            }
        }
        user_data.append(holiday_dict)
        send_json(user_data)
    return user_data


def display_holiday_data(holiday):
    """ displays all holidays with the provided data """
    try:
        user_list = extract_holiday(holiday)
        if user_list is None:
            return None
        for item in user_list:
            print(f'Holiday Name:',item['name'])
            print(f'Description:',item['description'])
            print(f'Country Name:',item['country'])
            print(f"Date:{item['datetime']['month']}/{item['datetime']['day']}/{item['datetime']['year']}") #TODO fix date format
            print()
    except Exception:
        print('This data is not in the format expected')
        return 'Unknown'       

def send_json(user_data):
    """ To check the type of data holiday api returns. """
    # NOTE verifying purposes 
    with open("scratch.json", "w") as f:
        json.dump(user_data,f, indent=2)