""" Performs all of the API calls and generates holidays celebrated in a given country,year and month. """
import os
import requests
from custom_exceptions import NoStateRegion
import json
import redis
from functools import lru_cache,cache

api_key = os.environ.get('MY_KEY')
redi = redis.Redis(host='localhost', port=6379, db=0)

#countries endpoint
def is_country_supported(country_code):
    """ Verifies country is supported by the api using country code. """
    country_list = req_res_country()
    try:
        for c in country_list:
            if c['country_code'] == country_code.upper():
                return True   
        raise NoStateRegion
    except NoStateRegion:
        print('error, No country matches the provided country code,try again!\n')
        return False
        
def req_res_country():
    country_res = redi.get('countries')
    if country_res is None: #if list of countries not in cache get it from api
        print('Could not find country list in cache, retrieving from the API.')
        req = req_countries()
        res = extract_countries(req)
        results = lis_of_countries(res)
        return results
    else:
        print('Found country codes in cache, retrieving from the redis server.')
        return json.loads(country_res)        


@lru_cache(maxsize=50) # start clearing the least recently used items after 50 entries 
def req_countries():
    """ Call countries API """
    url_countries = 'https://calendarific.com/api/v2/countries'
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
    
    
#USE FOR DROP DOWN
def lis_of_countries(countries):
    """ returns all of the countries and countr code (ISO) supported by api """
    results = []
    for c in countries:
        name_code = {
            'country_name':c['country_name'],
            'country_code':c['iso-3166']
        }
        results.append(name_code)
        redi.set('countries',json.dumps(results))
    return results    
        
           
 #holiday endpoint         
@lru_cache(maxsize=1)  #TODO Fix unhashable type error
def get_holiday_data(country,year,month):
    """ call holiday api with the provided data.
    :params:  user data to request holiday.
    :returns: holiday data if there is a holiday, otherwise returns None """
    try:
        query = {'country': country, 'year': year, 'month': month, 'type':'national','api_key':api_key}
        req = req_holiday(query)
        return req
    except requests.exceptions.HTTPError as err:
        req.raise_for_status()
        print(err.response.text)
  
        
def req_holiday(query):
    """ make a api request with the provided data. """
    url_holiday = 'https://calendarific.com/api/v2/holidays'
    try:
        req = requests.get(url_holiday,params=query).json()
        res = check_holiday_data_not_null(req)
        return res
    except requests.RequestException as e:
        req.raise_for_status()
        print(e.response.text)
    

def check_holiday_data_not_null(res):
    """ check if there is a holiday with the provided data from the API response
    :returns: none if there is no holiday """
    holiday_json = res['response']['holidays']
    return None if holiday_json == [] else holiday_json 

def display_holiday(holiday):
    """ displays all holidays with the provided data.
    :returns: holiday_data dictionary to display in the template.  """
    try:
        holiday_data = extract_country_holiday(holiday)
        return holiday_data
    except Exception as e:
        print(e)
        print('This data is not in the format expected')
        return 'Unknown'

    
def extract_country_holiday(holiday_data):
    """ extract holiday data.
    :param: holiday api response
    :returns: dictionary of the holiday data to render to the user.  """
    for hol in holiday_data:
        print()
        holiday_name = hol['name']
        description = hol['description']
        holiday_date = hol['date']['iso']
        holiday_dict = {
            'holiday_name':holiday_name,
            'description':description,
            'date':holiday_date
        }
    return holiday_dict



