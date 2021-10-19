""" Makes API calls and generets holidays observed in a country during that month """
import os
from credentials import api_key,url_countries, url_holiday
import requests
import json
import logging as log
from exceptions import NoStateRegion
import time 

# log config
log.basicConfig(filename='country.log', level=log.DEBUG,format='%(funcName)s')


        
def valid_country_code(country_code):
    """ check if a country with that country code exists """
    query = {'api_key': api_key}
    req = requests.get(url_countries,params=query)
    res_con = req.json()
    time.sleep(req.elapsed.total_seconds()) #sleep if server is slow. buffering to wait response
    
    for c in res_con['response']['countries']:
        # code(iso) match user input
        if c['iso-3166'] == country_code:
            return True
            
    raise NoStateRegion
  
    
def req_holiday(query):
    """ get holiday with the given data 
    :param query. user data"""
    try:
        query['api_key'] = api_key
        req = requests.get(url_holiday,params=query)
        res_hol = req.json()
        time.sleep(req.elapsed.total_seconds()) #sleep if server is slow. buffering to wait response
        
        # ssl ver
        if req.ok:
            response = check_holiday_data_not_null(res_hol)

        return response
    except requests.exceptions.HTTPError as err:
        print(err)
    
    


def check_holiday_data_not_null(res):
    """ :param response from api
        :return none if there is no holiday """
    holiday_json =res['response']['holidays']

    if holiday_json == []:
        return None
    else:
        return holiday_json



def get_holiday_data(holiday):
    user_list = extract_holiday(holiday)
    if user_list is None:
        return None
    for item in user_list:
        print(f'Holiday Name:',item['name'])
        print(f'Description:',item['description'])
        print(f'Country Name:',item['country'])
        print(f"Date:{item['datetime']['month']}/{item['datetime']['day']}/{item['datetime']['year']}") #TODO fix date format
        print(f'Type:',item['type'])
        print(f'Location:',item['locations']) #TODO ask this to the user
        print()
    
   
        
        

def extract_holiday(holiday):
    """ extracts holiday data from json """
    user_data = []
    for hol in holiday:
        print()
        holiday_name =  hol['name']
        holiday_description = hol['description']
        country_name = hol['country']['name']
        holiday_type = hol['type'][0]
        holiday_location = hol['locations']
        
        holiday_datetime = hol['date']['datetime']
        holiday_year = holiday_datetime['year']
        holiday_month = holiday_datetime['month']
        holiday_day = holiday_datetime['day']
            
        holiday_dict={
            'name':holiday_name,
            'description':holiday_description,
            'country':country_name,
            'datetime':{
                'year':holiday_year,
                'month': holiday_month,
                'day': holiday_day
            },
            'type':holiday_type,
            'locations':holiday_location
        }
        
        user_data.append(holiday_dict)
        send_json(user_data)
    return user_data
        
        
        
        
def send_json(user_data):
    """checking that return is correct. """
    #NOTE this is for testing purposes but could also be useful
    # when rendering climate from troposphere api.
    with open("scratch.json", "w") as f:
        json.dump(user_data,f, indent=2)






#NOTE this function for testing, using countries_scratch.json file instead of making api calls
# def get_country(self,country):
#     """ returns all of the countries and ISO supported by api """
#     while True:
#         try:
#             query = {'api_key': api_key,'country':'US','year':'2021'}
#             res_con = requests.get(url_countries,params=query).json()
            
#             results = []
#             for c in res_con['response']['countries']:
#                 country_name = c['country_name']
#                 country_code = c['iso-3166']
#                 print(country_name,country_code)
#                 name_code = {
#                     'country_name':country_name,
#                     'country_code':country_code
#                 }
#                 results.append(name_code)
#                 with open('countries_scratch.json','w') as f:
#                     json.dump(results, f,indent=2)
#         except Exception:
#             print('error')
            
            
