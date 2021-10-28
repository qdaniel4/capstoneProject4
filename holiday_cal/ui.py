""" Performs API requests and generates holidays celebrated in a given country during that month. """
import os
from credentials import api_key,url_holiday
import requests
from exceptions import NoStateRegion
import country_api
import json
#countries endpoint
def get_country_code(country_code):
    """ Verifies country is supported by the api using country code. """
    country_list = country_api.country_code_handler()
    try:
        for c in country_list:
            if c['iso-3166'] == country_code:
                return country_code    
        raise NoStateRegion
    except NoStateRegion:
        print('error, No country matches the provided country code,try again!\n')
        return None
        
    
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
        holiday_dict = {
            'holiday_name':holiday_name,
            'description':description,
            'country':country_name,
            'date':holiday_date
        }
        send_json(holiday_data)
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
    """checking that return is correct. """
    #NOTE this is for testing purposes but could also be useful
    # when rendering climate from troposphere api.
    with open("scratch.json", "w") as f:
        json.dump(user_data,f, indent=2)