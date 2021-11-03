""" Performs all of the API calls and generates holidays celebrated in a given country,year and month. """
# NOTE: Ed was running into an import error for this module when running the app as a whole. combined contents of this module into holiday_api.py
import os
import requests
import json
import redis
from datetime import timedelta
from functools import lru_cache

api_key = os.environ.get('CALENDAR_KEY')
redi = redis.Redis(host='localhost', port=6379, db=0)
#countries endpoint
def is_country_supported(country_name):
    """ Verifies country is supported by the api using country code. """
    country_list = req_res_country()
    if country_list != None:
        for c in country_list:
            if c['country_name'] == country_name.title():
                country_code = c['country_code']
                return country_code
    else:
        return None
        
def req_res_country():
    """ check for cached entries, if list of countries in cache, if not get from the API. """
    country_res = redi.get('country_test') #stored key=countries, value=[{country_name:'',country_code:''}]
    
    if country_res is None:
        print('Could not find country list in cache, retrieving from the API.')
        res = req_countries()
        if res != None:
            results = lis_of_countries(res)
            return results
    else:
        print('Found country codes in cache, retrieving from the redis server.')
        return json.loads(country_res)
        # return None
        

@lru_cache(maxsize=1)
def req_countries():
    """ Call countries API """
    url_countries = 'https://calendarific.com/api/v2/countries'
    query = {'api_key': api_key}
    req = requests.get(url_countries,params=query)
    res = req.json()
    response = res['response']
    if len(response) == 0:
        return None
    else:
        return res['response']['countries']


#USE FOR DROP DOWN
def lis_of_countries(countries):
    """ returns all of the countries and countr code (ISO) supported by api """
    # country_res = redi.get('countries') #stored key=countries, value=[{country_name:'',country_code:''}]
    results = []
    for c in countries:
        name_code = {
            'country_name':c['country_name'],
            'country_code':c['iso-3166']
        }
        results.append(name_code)
        redi.set('country_test',json.dumps(results), timedelta(seconds=360)) #prevent cache staleness
    return results    
        
           
 #holiday endpoint
@lru_cache(maxsize=1)          
def get_holiday_data(country,year,month):
    """ call holiday api with the provided data.
    :params:  user data to request holiday.
    :returns: holiday data if there is a holiday, otherwise returns None """
    query = {'country': country, 'year': year, 'month': month, 'type':'national','api_key':api_key}
    req = req_holiday(query)
    return req
 

def req_holiday(query):
    """ make a api request with the provided data. """
    url_holiday = 'https://calendarific.com/api/v2/holidays'
    req = requests.get(url_holiday,params=query).json()
    res = req['response']['holidays']
    return None if res == [] else res 
  

def display_holiday(holiday):
    """ displays all holidays with the provided data.
    :returns: holiday_data dictionary to display in the template.  """
    holiday_data = extract_country_holiday(holiday)
    return holiday_data

    
def extract_country_holiday(holiday_data):
    """ extract holiday data.
    :param: holiday api response
    :returns: dictionary of the holiday data to render to the user.  """
    for hol in holiday_data:
        holiday_name = hol['name']
        description = hol['description']
        holiday_date = hol['date']['iso']
        holiday_dict = {
            'holiday_name':holiday_name,
            'description':description,
            'date':holiday_date
        }
    return holiday_dict



